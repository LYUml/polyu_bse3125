# BSE3125 — 照明设计作业

**2026-11-16 已完成交付验收。** 最终文件为 [BSE3125_Lighting_Design_Report.pdf](00_Submit/BSE3125_Lighting_Design_Report.pdf)：主报告连正式 CAD 图共 8 页，含原生模拟附录共 191 页，5,859,608 字节。没有代为提交到课程平台。

逐项验收及原生/可编辑文件位置见 [assignment-acceptance-v1.json](05_Calculations/Final_v02/assignment-acceptance-v1.json)。正文源码在 Final_v02/report-content-v1.json，排版脚本在 scripts/build_main_report.py；正式 CAD 在 Final_v01/cad-native-v3/layout.dwg。两份保存重开的实际计算 evo 留在 models 中；大体积原生计算缓存和完整原始输出保留本机，仓库保存哈希和未经重绘的原生输出摘页。

| 文件夹 | 用途 |
| --- | --- |
| 01_Assignment_Brief | 原始题目；Building_Drawings 内保留原始 DWG |
| 02_References | 规范、厂家资料及开源复用来源 |
| 05_Calculations | data 保存统一数据；models 保存 DIALux 版本；scripts 保存计算与校核；Final_v02 保存报告源码和验收，Final_v01 保留正式 CAD |
| 06_Tools | 外部 toolkit 接入说明及操作证据包装脚本 |
| 00_Submit | 唯一最终交付入口，只有最终合并 PDF |

执行依据及历史试验见 PROJECT_SPEC.md。最终 112 个桌面的最低平均照度 504 lx、最低均匀度 0.80、最大采样方向 UGR 17.5；附加柱面、周边、背景、墙面和天花数值检查也已通过并保存重开核实。报告明确家具、表面、维护与控制假设，以及 DSE 角度筛查的范围；这些设计结果不等于实际安装系统的法定认证。

仓库：https://github.com/LYUml/polyu_bse3125 。提交采用“日期 + 变更”。课程个人资料、分组名单和录音转写不公开上传。
