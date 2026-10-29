# 观星哥·拆公司

**从招股书，看懂一家公司怎么赚钱。**

输入公司名，生成有数据、有比较、有来源的商业模式报告。

一家公司卖什么，谁愿意付钱，收入为什么增长，钱又花到了哪里？“观星哥·拆公司”查找招股书等正式披露，结合财务数据、同行资料和市场文章，把这些问题讲清楚。适合财经内容研究、理解公司业务、商科案例和面试准备。

## 能得到什么

- 看清增长来自哪些客户或业务，成本和研发投入怎样变化。
- 解释利润、现金、预收款及融资之间的关系。
- 拆开“唯一”“领先”“市场空间巨大”的限定条件，回到真实竞争。
- 比较同行卖什么、怎么收费、承担什么投入与权益。
- 交付HTML阅读版、Markdown、实际取得的正式原件、全文TXT和来源/计算记录。

HTML正文易读、引用轻量可点，来源附录可展开；作者栏高亮显示联系方式，欢迎交流反馈。不同公司按实际披露选择可分析项目。

## 试试这样说

- 帮我分析泡泡玛特，它靠什么赚钱？先让我选择报告深度。
- 用招股书拆解小米的收入、成本和现金流。
- 分析 Iambic，做 L3 数据与同行对照。

## 四档深度

| 档位 | 内容 |
|---|---|
| L1 快速看懂 | 卖什么、谁付钱、赚钱逻辑，约500字 |
| L2 拆开生意 | 完整商业模式与关键数据，约2500字 |
| L3 数据与同行对照 | 增长归因、费用与现金、定语剥离、市场核验、同行量化，约5000–8000字 |
| L4 深入研究 | 完整财务、资本需求、估值与情景，约8000字以上 |

先核实主体，再选择深度。可附市场、代码、分析时点或已有文件。篇幅按实际问题调整。

## WorkBuddy上手

1. 取得名称包含workbuddy的完整ZIP包。
2. 在WorkBuddy技能板块选择“添加技能→上传技能”，导入ZIP。
3. 在对话中说：“用观星哥·拆公司分析Iambic，先让我选择深度。”

WorkBuddy包包含中英文展示名、简介和示例。ZIP上传、触发及完整运行以实际客户端测试结果为准。

## Codex与其他平台

完整解压发布包，在目录中运行：

```bash
python3 scripts/install_skill.py --platform codex
python3 scripts/install_skill.py --platform claude-code
python3 scripts/install_skill.py --target /your/skills/gxg-company-decoder
python3 scripts/install_skill.py --check
```

Windows可使用py -3。明确选择平台，避免多平台同时安装时猜错目标。技术标识统一为gxg-company-decoder；Codex可用$gxg-company-decoder显式选择，其他平台采用其实际支持的入口。

## 更新旧版

解压新包后运行相同安装命令，或附加--update。旧安装与本地修改先整体备份；识别到prospectus-decoder旧目录时迁移到扫描目录之外，避免重复生效。压缩包安装同样支持此本地更新，不要求存在Git仓库。详见[跨平台使用](references/platforms.md)。

## 环境与资料

这是Agent执行的工作流，需当前平台具备检索、读取和文件工具。HTML需要Python 3及markdown-it-py；PDF优先Poppler，也可用其他提取工具。遇访问限制记录实际取得范围。市场文章保留链接和原创笔记；完整方法见[SKILL.md](SKILL.md)。

品牌：观星哥·拆公司｜技术标识：gxg-company-decoder｜版本：2.2.1。

作者：观星哥｜小红书：观星哥｜微信：guanxingge2025。欢迎交流使用体验、内容补充与改进建议。

## SkillHub

[观星哥·拆公司 SkillHub 页面](https://skillhub.cn/skills/user_d38a8796/prospectus-decoder)沿用旧版链接；新版技术标识为 `gxg-company-decoder`。
