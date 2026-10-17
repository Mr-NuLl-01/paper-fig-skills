"""Contract tests using temporary public-free fixtures; no paper images included."""
import base64, tempfile, unittest
from pathlib import Path
from check_svg import scan
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aG9sAAAAASUVORK5CYII=')
class SVGScanContract(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/'figure.svg'
    def tearDown(self):self.tmp.cleanup()
    def put(self,body,width='100mm',height='50mm',vb='0 0 1000 500'):
        self.p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{vb}">{body}</svg>');return self.p
    def test_final_physical_font_after_nested_scale(self):
        r=scan(self.put('<g font-size="10" transform="translate(20 10)"><g transform="scale(2)"><text x="0" y="10">Channel</text></g></g>'),7)
        self.assertAlmostEqual(r['canvas']['width_mm'],100)
        self.assertAlmostEqual(r['live_text_nodes'][0]['estimated_em_height_pt'],5.6693,places=3)
        self.assertIn('font_below_requested_min',[f['code'] for f in r['findings']])
    def test_asset_dimensions_and_missing_link(self):
        (self.p.parent/'real.png').write_bytes(PNG)
        r=scan(self.put('<image id="a" href="real.png" width="100" height="100"/><image id="b" href="missing.png" width="10" height="10"/>'))
        self.assertEqual(r['images'][0]['width_px'],1)
        self.assertAlmostEqual(r['images'][0]['placed_width_mm'],10)
        self.assertIn('missing_local_asset',[f['code'] for f in r['findings']])
    def test_embedded_image_and_metadata(self):
        b64=base64.b64encode(PNG).decode();r=scan(self.put(f'<metadata>source manifest</metadata><image href="data:image/png;base64,{b64}" width="100" height="100"/>'))
        self.assertTrue(r['metadata_element_present']);self.assertEqual(r['images'][0]['format'],'PNG')
        self.assertIn('no_live_text_detected',[f['code'] for f in r['findings']])
    def test_wrapped_base64_export_preserves_image_metadata(self):
        b64=base64.b64encode(PNG).decode();wrapped=' \n'+b64[:40]+'\n\t'+b64[40:]+' '
        r=scan(self.put(f'<image href="data:image/png;base64,{wrapped}" width="100" height="100"/>'))
        self.assertEqual(r['images'][0]['format'],'PNG')
        self.assertEqual(r['images'][0]['width_px'],1)
        self.assertNotIn('invalid_data_uri',[f['code'] for f in r['findings']])
    def test_nonwhitespace_base64_corruption_still_reported(self):
        b64=base64.b64encode(PNG).decode();invalid=b64[:40]+'?'+b64[40:]
        r=scan(self.put(f'<image href="data:image/png;base64,{invalid}" width="100" height="100"/>'))
        self.assertIn('invalid_data_uri',[f['code'] for f in r['findings']])
    def test_css_and_fragment_limits_are_explicit(self):
        r=scan(self.put('<style>.label {font-size:20px}</style><text class="label">A</text><use href="#missing"/><g id="dup"/><g id="dup"/>'))
        codes=[f['code'] for f in r['findings']]
        self.assertIn('duplicate_id',codes);self.assertIn('missing_fragment',codes)
        self.assertTrue(any('Stylesheets' in s for s in r['uncertainties']))
    def test_relative_canvas_does_not_invent_points(self):
        r=scan(self.put('<text font-size="10">B</text>',width='100%',height='100%'))
        self.assertIsNone(r['live_text_nodes'][0]['estimated_em_height_pt'])
        self.assertTrue(r['uncertainties'])
if __name__=='__main__':unittest.main()
