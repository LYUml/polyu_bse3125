# BSE3125 作业文件导航

最新交付以 `00_Submit` 为准。报告正文含 CAD 共 9 页，连附录共 20 页，3,714,013 字节。2026-11-16 已完成目录整理和重新生成核对。

| 文件夹 | 内容 |
|---|---|
| `00_Submit` | 最终 PDF；`DIALux/Final` 两份最终方案工程；`DIALux/Comparisons` 四份对比工程 |
| `01_Assignment_Brief` | 原始题目 PDF 和原始 DWG，保持不变 |
| `02_References` | 标准、厂家资料及原始光度文件 |
| `03_Engineering` | 当前 DIALux 工程、CAD、完整原生计算报告及文件索引 |
| `04_Report` | 当前报告文字、图表源资料、私人组员信息及生成输出 |
| `05_Calculations` | 共用设计数据、计算结果、验证证据及迁移索引 |
| `06_Tools` | 当前报告生成程序、工程工具和依赖 |
| `99_Archive` | 历史草稿、旧工程、试验、截图和旧说明；不作为最终交付入口 |

## 打开哪些文件

- 阅读报告：`00_Submit/BSE3125_Lighting_Design_Report.pdf`。
- 查看主要 DIALux 方案：`00_Submit/DIALux/Final/Office_Workstations.evo`，包含桌面照度、均匀度和眩光计算。
- 查看辅助照明评价：同目录 `Office_Visual_Environment.evo`，包含柱面、周边、背景、墙面和天花计算。
- 查看正式 CAD：`03_Engineering/CAD/Lighting_Layout.dwg`；同名 PDF 为 A2、1:100 原生出图。
- 修改报告文字：`04_Report/content.json`；生成程序：`06_Tools/report`。

6 份提交目录中的 evo 文件均与已保存、重开验证的工程逐字节一致。它们合计约 622 MB；PDF 本身仍为 3.71 MB。组员信息、含学号的报告和大型 evo 文件只保留本机，不推送 Git。没有代为提交 Blackboard。

## 重新生成

在工作区根目录运行：

```powershell
& ../dialux-agent-toolkit/.venv/Scripts/python.exe -X utf8 06_Tools/rebuild_report.py 04_Report/Build_Check
```

输出目录必须是新的；不会覆盖最终交付 PDF。报告生成只依赖当前目录，不依赖 `99_Archive`。迁移后重建的 20 页已逐页核对文字、尺寸及 72/150 dpi 像素，与提交 PDF 一致。

当前数据绑定：`05_Calculations/data/final-design.json`。目录验收：`05_Calculations/workspace-verification.json`。旧证据中的路径保持原样以保留历史，可通过 `06_Tools/resolve_evidence_path.py` 或迁移索引定位。

2026-11-17: Native DIALux projects, full calculation reports, group metadata and historical coursework are now tracked and uploaded; large files use Git LFS. Generated previews, caches and runtime dependencies are excluded. Archive directory: `99_Archive`. Clone with Git LFS installed and run `git lfs pull` to retrieve native files.
