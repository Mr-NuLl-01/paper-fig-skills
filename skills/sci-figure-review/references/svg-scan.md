# SVG机械扫描的能力与边界

运行`python scripts/check_svg.py figure.svg`，可加`--min-label-pt N`指定用户/期刊实际字号下限。输出JSON，包含画布毫米尺寸、viewBox、文字节点、图像资产和逐项发现。它不修改文件、不访问网络。异常XML或本地缺失引用属于机械错误；扫描报告不构成科学或视觉通过证书。

## 实际计算

- 根SVG物理尺寸支持mm/cm/in/pt/px及unitless SVG px；百分比尺寸无法从文件单独确定。1 px按96/in换算。仅有viewBox没有物理尺寸时，明确不能计算最终字号和PPI。
- 字号支持presentation属性与inline style、继承、em/%及常见绝对单位，结合根viewBox和可识别transform估算最终em高度点数。子tspan覆盖单独报告。字体形状、字符实际边界、基线、外部/复杂CSS和文本路径不由此验证。
- 支持matrix/translate/scale/rotate/skewX/skewY的仿射变换。嵌套SVG视口、百分比font-size的复杂级联、CSS transform与滤镜不完整求解，报告限制后需渲染确认。
- 本地和base64栅格资产读取PNG/GIF/JPEG像素元数据；允许导出器在base64正文中插入的ASCII空白，其余字符仍严格验证。无法识别或远程图像不猜像素。最终放置尺寸可求时估算有效PPI。脚本不规定固定PPI门槛，不检测显微图真实性、锐度、裁切科学含义或比例尺标定。
- 检查本地文件引用、`#id`、重复ID、live text与`metadata`存在。存在metadata不代表内容完整/真实；有text不代表所有标签都是live text；没有text也可能是合理的无文字面板，需按请求解释。

## 报告中的限制

`uncertainties`是需人工查看的范围，不能当作已通过。若`style`节点/外部样式存在，脚本仍可报告独立的本地资源和画布问题，但文字估计需要回到实际CSS及渲染。若使用复杂变换，优先在最终尺寸渲染后用编辑器测字高。导出后的缺字、裁切、透明效果和字体替换必须实际打开导出文件检查。

最小单元验证见`test_check_svg.py`，使用临时SVG和微型PNG验证物理点数、嵌套变换、缺失资产、重复ID以及不解析CSS的限制标记。这些测试只验证扫描器契约，不验证科学图的科学性。
