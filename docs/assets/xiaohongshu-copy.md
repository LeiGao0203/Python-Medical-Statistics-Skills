# 小红书封面与发布文案

封面图：`docs/assets/xiaohongshu-cover.png`

## 标题

我把医学统计分析整理成了一套 AI Agent 可用的 Python 技能库

## 备选标题

1. 医学统计不想每次从零写？我做了一个 Python 开源技能库
2. 让 AI Agent 帮你做 Table 1、logistic 回归和 ROC 分析
3. 给医学科研数据分析用的 Python Agent 技能库，开源了

## 正文

做医学科研数据分析时，最消耗人的往往不是某一行 Python 代码，而是整套流程：

- 数据该先检查什么？
- 连续变量、分类变量分别怎么汇总？
- Table 1 怎么按结局或分组生成？
- 卡方、t 检验、非参数检验什么时候用？
- logistic 回归、OR、95% CI、ROC/AUC 怎么整理成可以汇报的结果？
- 让 AI 写代码时，怎么避免每次都重新解释一遍统计分析规范？

所以我把常见的医学统计 Python 工作流整理成了一个开源项目：

`Python Medical Statistics Skills`

它不是一个普通代码片段合集，而是一套给 AI coding agent 读取和执行的 `SKILL.md` 技能库。你可以把它理解成：把“医学统计分析经验 + Python 实现模板 + 结果汇报习惯”沉淀成一组可复用的 agent 技能。

目前项目里包括这些内容：

- 基础统计：t 检验、卡方检验、ANOVA、相关分析、非参数检验、ROC、样本量估计
- 高级模型：logistic 回归、多元回归、生存分析、PCA
- 研究设计：倾向评分匹配、亚组分析
- 工作流：纯 Python 脚本分析、Jupyter notebook 分析
- 可运行示例：肺癌问卷数据分析案例

我放了一个完整示例：`example/lung-cancer`。

这个例子使用 309 条肺癌问卷数据，演示从数据清洗到结果导出的完整流程，包括：

- 变量名清洗和二分类变量重编码
- 按肺癌状态分层的 Table 1
- 分类变量的卡方检验 / Fisher 精确检验
- 年龄的 Welch t 检验和 Mann-Whitney U 检验
- 多变量 logistic 回归
- OR 和 95% CI 表格
- ROC 曲线、AUC、最佳阈值和 PNG 图形输出

也就是说，它不是只告诉 agent “帮我分析一下”，而是让 agent 按一个相对规范的医学统计工作流去做：先检查数据，再选方法，再输出表格和图，最后留下可复现的脚本或 notebook。

安装也尽量做成 agent 友好的一行命令：

```bash
curl -fsSL https://raw.githubusercontent.com/LeiGao0203/Python-Medical-Statistics-Skills/main/install.sh | bash
```

如果你用的不是 Codex，也可以通过 `AGENT_SKILLS_DIR` 指定技能目录，把它装到其他支持技能目录的 coding agent 里。

我觉得它比较适合这些人：

- 医学生、研究生、临床科研同学，想让 AI 辅助做常见统计分析
- 已经在用 Python 做医学数据分析，但想把流程规范化
- 想让 agent 自动生成 Table 1、回归结果表、ROC 图
- 想把常用分析方法沉淀成可复用工作流，而不是每次重新写 prompt
- 对 AI agent、技能库、可复现科研分析感兴趣的开发者

现在还是一个持续补充中的开源项目，后面我会继续加更多真实研究场景、报告模板和分析示例。

如果你也经常让 AI 帮你做科研数据分析，真的建议试试“把方法工作流做成技能库”这件事。它比一次性 prompt 稳定得多，也更适合长期维护。

## 互动引导

如果你想看具体示例，我后面可以单独拆一篇：用 AI Agent 跑完整肺癌问卷数据分析，从 Table 1 到 logistic 回归和 ROC 图。

也欢迎医学统计 / 临床科研 / Python 数据分析方向的朋友一起提建议，看看还应该补哪些常用方法。

## 标签

#Python #医学统计 #科研数据分析 #AI编程 #开源项目 #JupyterNotebook #统计建模 #Logistic回归 #ROC曲线 #Table1 #CodingAgent #医学科研
