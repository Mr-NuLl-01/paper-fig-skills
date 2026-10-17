# 可编辑合成与实际尺寸

## 主文件和证据对象

推荐保留一个任务适配的主SVG，其`width`/`height`为明确物理单位，并有`viewBox`。这不是要求每个任务必须使用SVG；用户已有AI/PPTX/其他工程时保留其格式及编辑性。

把每个可独立修改的科学对象组织为有稳定ID的组，如`device-channel`、`nerve`、`data-response`、`photo-chip`、`annotations`。组名只是编辑导航，不是必须照抄的层模板。文字保留`text`/`tspan`而不统一转路径；出版必须转曲时，另保留live-text主文件。数据点和曲线可以是路径，但保留其数据文件、生成脚本、单位、拟合与原始数据区别。

真实资产的最低清单可写入JSON/CSV或已有项目记录：

```json
{
  "asset": "assets/chip_photo.tif",
  "role": "measured photograph",
  "source": "user supplied acquisition file",
  "crop": "panel b region; original unchanged",
  "pixel_size": [3600, 2400],
  "scale_bar": "from acquisition calibration",
  "permission": "as supplied by user"
}
```

不需要为一幅简单图额外制造整套文档。已有元数据足够时直接引用；不猜缺失的采集参数、许可或比例尺。

## 点数和分辨率

在最终版面量字，而非只看SVG中的`font-size`数字。SVG的viewBox、嵌套缩放和导出尺寸会改变最终字体点数；1 pt = 1/72 inch，1 inch = 25.4 mm。不同要求由用户或当前官方期刊规范确定，不强制统一字号或300 dpi门槛。

栅格图的有效分辨率由像素数除以最终放置的英寸数计算。显微图比例尺只从采集标定或有凭据的已知尺度获得。等比缩放应连同比例尺一起变化；非等比拉伸改变结构比例，未经理由不要使用。透明图有白底/深底的不同边缘表现，需在最终底色检查。

## 合成顺序

1. 先锁定数据轴、原图裁切与关键结构的真实占位，再安排标签和连线。
2. 连线和文字放独立层，端点落到具体对象；交叉线可换路由、断桥或编号，不靠模糊渐变掩饰。
3. 用统一阅读基线和适当留白组织组间关系；不要求每组同宽同高。
4. 渲染最终物理尺寸和足以看清细节的预览，实际查看两种尺度。导出不应丢字、缺图、改变线型或重排结构。
5. 保留主文件、真实资产、数据与脚本之间的相对路径；如需完全自包含SVG，嵌入图像后再检查最终文件，同时保留独立原图。

相邻`sci-figure-review`模块的[check_svg.py](../../sci-figure-review/scripts/check_svg.py)可检查部分机械属性，但不能识别图中对象是否科学正确，也不能替代实际渲染。
