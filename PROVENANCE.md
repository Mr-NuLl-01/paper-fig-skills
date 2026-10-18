# 来源与版本范围 / Provenance

## v1.1.0 · 2026-10-18

本版以既有九技能为基础，补英文入口、复杂视图规程和用户已审阅的模拟案例，并恢复原完整归档的配套资料。完整导入说明见[ARCHIVE_IMPORT.md](docs/ARCHIVE_IMPORT.md)。

原包为151文件、12,462,322字节，SHA-256为`51fe54cd16dba5d17d931995e7a42349c5ee723f2a0dbf3fa90c63c9fd222553`。其中150项逐文件大小与SHA核验通过；原归档清单和首次71文件技能导入清单都保留在docs/history。本版不假装当前修改仍与初次导入逐字节相同。

- [SKILL-MANIFEST.json](SKILL-MANIFEST.json)：当前技能源文件。
- [RELEASE-MANIFEST.json](RELEASE-MANIFEST.json)：当前全仓库交付文件，不包含其自身。
- [原技能清单](docs/history/skill-manifest-20261017.json)：首次导入历史。
- [原归档清单](docs/history/archive-manifest-20261017.json)：151文件来源。

## 证据与制作边界

89论文、178图及66/23阅读层级是原项目记录，不是本轮重新审读。没有重新核查全部Methods/SI或复现实验。外部来源只以链接和分析保留，不分发第三方论文全文或原始期刊图片。

本轮gallery实际读取本仓库技能并用代码/Blender生成，模型ID和推理档位未暴露，已明确记为未知。原增强器件案例有脚本/原生几何/检查记录，但没有独立技能调用或型号日志；不将它冒称指定模型的新测试。数据均为模拟或概念结构，用户参考截图不再分发。

已运行新例生成器、数值/导出检查、原SVG扫描器7个测试、中英文技能导出、123个新增/主要导航文档本地链接检查；新三维源重新打开检查，最终图已由用户审阅。论文图谱从交付JSON重建成功；原手册仅检查显式字体参数入口，未重排。未进行Windows/macOS安装或全部编辑器兼容性验证。原已知扫描/配色限制仍见KNOWN_ISSUES.md。

## 核对当前技能文件

```python
import hashlib, json
from pathlib import Path
root = Path('.')
m = json.loads((root / 'SKILL-MANIFEST.json').read_text())
for entry in m['files']:
    data = (root / entry['path']).read_bytes()
    assert len(data) == entry['bytes'], entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
print('Verified skill files:', len(m['files']))
```

The current manifests describe this release. Historical manifests describe their original snapshots. Hashes establish file identity, not scientific validity. MIT licensing for repository content does not override third-party rights.
