# 来源与发布范围

## 来源

- 来源归档根目录：`science-figure-atlas/`
- 来源归档整理日期：2026-10-17
- 原始 ZIP SHA-256：`51fe54cd16dba5d17d931995e7a42349c5ee723f2a0dbf3fa90c63c9fd222553`
- 本次导入范围：归档内 `science-figure-atlas/skills/` 下的全部 9 个技能、71 个文件。
- 文件映射：移除归档顶层 `science-figure-atlas/` 前缀，保留 `skills/` 内目录结构及全部原始文件字节。

每个技能文件的大小、SHA-256 与 Git blob SHA-1 见 [SKILL-MANIFEST.json](SKILL-MANIFEST.json)。根目录维护文档为本次发布补充；`LICENSE` 沿用目标仓库原有 MIT 文件。

## 未纳入的材料

来源归档的研究手册、额外交付图谱、运行/安装日志、审查工作记录和工具目录不属于本次技能仓库导入范围。未上传第三方论文全文、第三方原图、下载缓存、凭据或其他私人研究文件。

技能内的文献图谱只保存文献元数据、阅读范围、来源链接与绘图分析；其中外部链接可能指向出版商页面或图片，这不表示那些第三方内容已复制进仓库或获得再分发许可。

## 文献证据口径

来源图谱记载 89 个唯一 DOI、178 张已看关键整图、66 篇主文连续阅读与 23 篇目标图定向精读。各条目的 `read_scope`、`sections_read`、`figures_viewed` 和 `read_tier` 保留具体范围。

这些数字描述原始项目所登记的阅读，不是本次发布重新进行的审读；不包含对全部 Methods、SI 或所有图片已读的承诺，也不是对论文结论的独立复现。作者实际绘图软件无确证时仍为 unknown。

## 发布前检查

- 核对源 ZIP 摘要以及全部 71 个拟发布技能文件与归档内文件的字节一致性。
- 检查九个技能结构，解析 JSON、SVG XML 与 Python 语法，检查本地资源与相对文档引用。
- 对文本及可读取的 PNG/Blender 元数据做有限的路径、凭据模式和外部资源检查；未发现需要剔除的用户秘密。保留的 `.blend` 有原生成环境的渲染输出位置设置，使用前需重新选择输出目录。
- 本次没有执行示例脚本、重新渲染图形、重新打开 `.blend` 或完成 Windows/macOS 全流程安装测试。静态检查不保证不存在缺陷；已知限制单列于 [KNOWN_ISSUES.md](KNOWN_ISSUES.md)。

## 本地核验

在仓库根目录使用 Python 核对技能文件：

```python
import hashlib
import json
from pathlib import Path

root = Path('.')
manifest = json.loads((root / 'SKILL-MANIFEST.json').read_text(encoding='utf-8'))
expected = {entry['path'] for entry in manifest['files']}
actual = {p.as_posix() for p in Path('skills').rglob('*') if p.is_file()}
assert actual == expected, 'File set differs from manifest'
for entry in manifest['files']:
    data = (root / entry['path']).read_bytes()
    assert len(data) == entry['bytes'], entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
print('Verified skill files:', len(expected))
```

Git 提交提供仓库整体版本；该清单仅覆盖技能内容，不能单独证明源材料的科学正确性或授权状态。
