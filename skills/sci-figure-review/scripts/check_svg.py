#!/usr/bin/env python3
"""Non-mutating SVG mechanical inventory. No scientific or visual pass/fail claim."""
import argparse, base64, json, math, re, struct, sys
from pathlib import Path
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

NUM=r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?'
LENGTH=re.compile(r'^\s*('+NUM+r')\s*([a-zA-Z%]*)\s*$')
PX={'':1.,'px':1.,'pt':96/72,'pc':16.,'in':96.,'cm':96/2.54,'mm':96/25.4,'q':96/101.6}
IDENTITY=(1.,0.,0.,1.,0.,0.)
def tag(e):return e.tag.rsplit('}',1)[-1]
def style(e):
    out={}
    for item in e.get('style','').split(';'):
        if ':' in item:
            k,v=item.split(':',1);out[k.strip()]=v.strip()
    return out
def length_px(s,relative=None):
    if s is None:return None
    m=LENGTH.fullmatch(s)
    if not m:return None
    val=float(m[1]);unit=m[2].lower()
    if unit in PX:return val*PX[unit]
    if relative is not None and unit in ['em','%']:return val*relative/(100 if unit=='%' else 1)
    return None
def multiply(a,b):
    if a is None or b is None:return None
    A,B,C,D,E,F=a;g,h,i,j,k,l=b
    return (A*g+C*h,B*g+D*h,A*i+C*j,B*i+D*j,A*k+C*l+E,B*k+D*l+F)
def transform(s):
    if not s:return IDENTITY
    out=IDENTITY;end=0
    for m in re.finditer(r'([A-Za-z]+)\s*\(([^)]*)\)',s):
        if s[end:m.start()].strip(' ,\t\n'):raise ValueError('unparsed transform')
        end=m.end();name=m[1];v=[float(x) for x in re.findall(NUM,m[2])]
        if name=='matrix' and len(v)==6:t=tuple(v)
        elif name=='translate' and len(v) in [1,2]:t=(1,0,0,1,v[0],v[1] if len(v)>1 else 0)
        elif name=='scale' and len(v) in [1,2]:t=(v[0],0,0,v[-1],0,0)
        elif name=='rotate' and len(v) in [1,3]:
            rad=math.radians(v[0]);c=math.cos(rad);sn=math.sin(rad);t=(c,sn,-sn,c,0,0)
            if len(v)==3:t=multiply(multiply((1,0,0,1,v[1],v[2]),t),(1,0,0,1,-v[1],-v[2]))
        elif name=='skewX' and len(v)==1:t=(1,0,math.tan(math.radians(v[0])),1,0,0)
        elif name=='skewY' and len(v)==1:t=(1,math.tan(math.radians(v[0])),0,1,0,0)
        else:raise ValueError('unsupported transform '+name)
        out=multiply(out,t)
    if s[end:].strip(' ,\t\n'):raise ValueError('unparsed transform')
    return out

def pixels(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>=24:return {'format':'PNG','width_px':struct.unpack('>I',data[16:20])[0],'height_px':struct.unpack('>I',data[20:24])[0]}
    if data[:6] in [b'GIF87a',b'GIF89a'] and len(data)>=10:
        w,h=struct.unpack('<HH',data[6:10]);return {'format':'GIF','width_px':w,'height_px':h}
    if data.startswith(b'\xff\xd8'):
        p=2
        while p+4<=len(data):
            if data[p]!=255:p+=1;continue
            while p<len(data) and data[p]==255:p+=1
            if p>=len(data):break
            marker=data[p];p+=1
            if marker in [0xd8,0xd9] or 0xd0<=marker<=0xd7:continue
            if p+2>len(data):break
            n=struct.unpack('>H',data[p:p+2])[0]
            if n<2 or p+n>len(data):break
            if marker in [0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf] and n>=7:
                h,w=struct.unpack('>HH',data[p+3:p+7]);return {'format':'JPEG','width_px':w,'height_px':h}
            p+=n
    return {'format':'unrecognized; no pixel dimensions inferred'}

def scan(path,min_label_pt=None):
    path=Path(path).resolve();root=ET.parse(path).getroot()
    findings=[];uncertainties=[];texts=[];images=[]
    def note(level,code,location,detail):findings.append({'level':level,'code':code,'location':location,'detail':detail})
    if tag(root)!='svg':raise ValueError('Root element is not SVG')
    wp=length_px(root.get('width'));hp=length_px(root.get('height'))
    wpt=wp*72/96 if wp is not None else None;hpt=hp*72/96 if hp is not None else None
    vb=None
    try:
        a=[float(x) for x in re.findall(NUM,root.get('viewBox',''))]
        if len(a)==4 and a[2]>0 and a[3]>0:vb=a
    except ValueError:pass
    if wp is not None and wp<=0 or hp is not None and hp<=0:note('error','nonpositive_canvas','root','Physical canvas dimensions must be positive.')
    sx=sy=None
    if wpt and hpt and wpt>0 and hpt>0:
        sx=wpt/(vb[2] if vb else wp);sy=hpt/(vb[3] if vb else hp)
        if vb and root.get('preserveAspectRatio','xMidYMid meet').strip()!='none':
            uniform=max(sx,sy) if 'slice' in root.get('preserveAspectRatio','') else min(sx,sy);sx=sy=uniform
    else:uncertainties.append('Physical root size missing/relative; final font points and placed PPI cannot be computed.')
    if not vb:note('info','viewbox_absent_or_invalid','root','No valid viewBox; coordinates treated as default SVG px when physical size is known.')
    if any(tag(e)=='style' for e in root.iter()) or any(tag(e)=='link' for e in root.iter()) or b'<?xml-stylesheet' in path.read_bytes():
        uncertainties.append('Stylesheets are not resolved; font/visibility estimates include only attributes, inline style and inheritance.')
    ids={}
    for e in root.iter():
        id=e.get('id')
        if id:
            if id in ids:note('error','duplicate_id',id,'The same id occurs more than once.')
            ids[id]=e
    def vector_pt(ctm,x,y):
        if ctm is None or sx is None or sy is None:return None
        return math.hypot((ctm[0]*x+ctm[2]*y)*sx,(ctm[1]*x+ctm[3]*y)*sy)
    def visit(e,ctm,font=16.,font_explicit=False,family=None,display_hidden=False,visibility='visible'):
        st=style(e);loc=e.get('id') or tag(e)
        try:ctm=multiply(ctm,transform(e.get('transform')))
        except ValueError as ex:ctm=None;uncertainties.append(loc+': '+str(ex))
        if e is not root and tag(e)=='svg':
            ctm=None;uncertainties.append(loc+': nested SVG viewport not solved.')
        if 'transform' in st:ctm=None;uncertainties.append(loc+': CSS transform not solved.')
        fs=st.get('font-size',e.get('font-size'))
        if fs:
            newfont=length_px(fs,font)
            if newfont is None:font=None;uncertainties.append(loc+': unsupported font size '+fs)
            else:font=newfont
            font_explicit=True
        family=st.get('font-family',e.get('font-family',family))
        hidden=display_hidden or st.get('display',e.get('display'))=='none'
        visibility=st.get('visibility',e.get('visibility',visibility))
        if tag(e) in ['text','tspan','textPath'] and not hidden and visibility not in ['hidden','collapse']:
            own=(e.text or '')+''.join(c.tail or '' for c in e)
            if own.strip():
                pt=vector_pt(ctm,0,font) if font is not None else None
                t={'element':loc,'text':own.strip()[:100],'font_size_declared':fs,'estimated_em_height_pt':round(pt,4) if pt is not None else None,'font_family':family,'font_size_explicit_or_inherited':font_explicit}
                texts.append(t)
                if not font_explicit:note('info','default_font_size',loc,'Font size is undeclared; the SVG default is used only as an estimate.')
                if min_label_pt is not None and pt is not None and pt<min_label_pt:note('warning','font_below_requested_min',loc,f'Estimated final em height {pt:.3f} pt < requested {min_label_pt:g} pt; verify rendered text.')
        href=e.get('href') or e.get('{http://www.w3.org/1999/xlink}href')
        asset=None
        if href:
            if href.startswith('#'):
                if href[1:] not in ids:note('error','missing_fragment',loc,href)
            elif href.startswith('data:'):
                if tag(e)=='image':
                    try:
                        head,body=href.split(',',1)
                        # SVG exporters may wrap base64; XML normalizes attribute
                        # line breaks to spaces. Tolerate ASCII whitespace only,
                        # while retaining strict validation of all other bytes.
                        asset=base64.b64decode(re.sub(r'[\t\n\r\f ]','',body),validate=True) if ';base64' in head else unquote(body).encode()
                        ref={'reference':'embedded data URI','bytes':len(asset)}
                    except Exception as ex:note('error','invalid_data_uri',loc,str(ex));ref={'reference':'invalid data URI'}
            else:
                u=urlparse(href)
                if u.scheme in ['http','https']:ref={'reference':href,'status':'remote; not fetched'}
                elif u.scheme and u.scheme!='file':ref={'reference':href,'status':'unsupported URI scheme'}
                else:
                    file=Path(unquote(u.path)) if u.scheme=='file' else path.parent/unquote(u.path)
                    exists=file.is_file();ref={'reference':href,'resolved_path':str(file.resolve()),'exists':exists}
                    if not exists:note('error','missing_local_asset',loc,href)
                    elif tag(e)=='image':asset=file.read_bytes()
            if tag(e)=='image':
                if href.startswith('#'):ref={'reference':href,'status':'fragment image; pixel metadata not inferred'}
                im={'element':loc,**ref}
                if asset is not None:im.update(pixels(asset))
                iw=length_px(e.get('width'));ih=length_px(e.get('height'))
                placed_w=vector_pt(ctm,iw,0) if iw is not None else None;placed_h=vector_pt(ctm,0,ih) if ih is not None else None
                im['placed_width_mm']=round(placed_w*25.4/72,4) if placed_w is not None else None
                im['placed_height_mm']=round(placed_h*25.4/72,4) if placed_h is not None else None
                if im.get('width_px') and placed_w and placed_h:
                    im['effective_ppi_xy']=[round(im['width_px']/(placed_w/72),2),round(im['height_px']/(placed_h/72),2)]
                    im['ppi_note']='Image box estimate; preserveAspectRatio cropping/letterboxing can change actual rendered pixel scale.'
                images.append(im)
        elif tag(e)=='image':note('error','image_without_href',loc,'Image element has no href asset.')
        if tag(e)=='foreignObject':uncertainties.append(loc+': foreignObject rendering/export not checked.')
        for c in e:visit(c,ctm,font,font_explicit,family,hidden,visibility)
    visit(root,IDENTITY)
    if not texts:note('warning','no_live_text_detected','document','No visible live text detected; this may be intentional for a label-free panel. Outlined labels cannot be identified.')
    return {'file':str(path),'scan':'mechanical inventory only; no scientific or visual approval','canvas':{'width':root.get('width'),'height':root.get('height'),'width_mm':round(wpt*25.4/72,4) if wpt is not None else None,'height_mm':round(hpt*25.4/72,4) if hpt is not None else None,'viewBox':vb},'metadata_element_present':any(tag(e)=='metadata' for e in root.iter()),'live_text_nodes':texts,'images':images,'findings':findings,'uncertainties':list(dict.fromkeys(uncertainties))}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('svg');ap.add_argument('--min-label-pt',type=float);a=ap.parse_args()
    if a.min_label_pt is not None and a.min_label_pt<=0:ap.error('--min-label-pt must be positive')
    try:report=scan(a.svg,a.min_label_pt)
    except (ET.ParseError,OSError,ValueError) as ex:
        print(json.dumps({'file':a.svg,'scan_error':str(ex),'scope':'No SVG scan completed.'},ensure_ascii=False,indent=2));return 2
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':sys.exit(main())
