# BSE3125 照明设计作业

2026-11-16 已完成严格复审后的修订版。最终入口：[BSE3125_Lighting_Design_Report.pdf](00_Submit/BSE3125_Lighting_Design_Report.pdf)。正文连独立 A2 CAD 图共 9 页，含原生模拟附录共 192 页，5,978,804 字节。没有代为提交课程平台。

最终采用 186 盏 Philips PowerBalance 40S（910505103638，4000 lm / 23 W）。112 张桌面的最低平均照度 593 lx、最低均匀度 0.80、最大采样方向 UGR 18.1；补充柱面、周边、背景、墙面和天花指标也通过选定阈值。两份原生模型均保存重开核对，112 行核心桌面结果、288 行补充结果及全部灯具坐标保持一致。

逐项验收：[assignment-acceptance-v3.json](05_Calculations/Final_v03/assignment-acceptance-v3.json)。统一数据绑定：data/final-design-v2.json。正文可编辑源码：Final_v03/report-content-v3.json；排版/合并：scripts/build_review_report.py、scripts/assemble_review_submission.py。正式 CAD：Final_v03/cad-native-v5/layout.dwg。

原生项目在本机 models/office-review-40s-native-v4.evo、models/office-review-brightness-native-v4.evo。大体积完整计算文件保留本机，Git 保存哈希和原生摘页证据。原始题目与 DWG 未改动。Final_v01/Final_v02 为历史版本，当前交付以 Final_v03 为准。

报告明确家具、表面、维护和立面假设，区分原生结果与解析容差分析，并说明待安装调试的控制功能及显示屏亮度筛查范围。这些学术设计结果不等于安装系统的法定认证。

仓库：https://github.com/LYUml/polyu_bse3125 。课程个人资料、分组名单和录音转写没有公开上传。
