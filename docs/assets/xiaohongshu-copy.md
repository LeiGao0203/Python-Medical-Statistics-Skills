# 小红书封面与发布文案

封面图：`docs/assets/xiaohongshu-cover.png`

## 标题

用 Python 做医学统计分析：我整理了一套给 AI Agent 用的开源技能库

## 正文

最近把医学统计分析里最常用的一批 Python 工作流整理成了一个开源项目：`Python Medical Statistics Skills`。

它不是单纯的代码模板，而是一组可以交给 coding agent 读取和执行的 `SKILL.md` 技能目录。目标很简单：让 agent 在做医学研究数据分析时，不只是“会写 Python”，还知道应该怎样检查数据、选择统计方法、输出结果表格，并把分析过程做得可复现。

目前包含：

- 基础统计：t 检验、卡方检验、ANOVA、相关分析、非参数检验、ROC、样本量估计
- 高级模型：logistic 回归、多元回归、生存分析、PCA
- 文献与研究设计：倾向评分匹配、亚组分析
- 工作流：纯 Python 脚本分析、Jupyter notebook 分析
- 示例：肺癌问卷数据分析，包含 Table 1、检验、logistic 回归、ROC/AUC 和图形输出

安装也尽量做成 agent 友好的一行命令。你可以直接把安装命令丢给 Codex 或其他支持技能目录的 coding agent，让它自己装到技能目录里。

这个项目适合这些场景：

- 想让 agent 帮你搭建医学统计分析脚本
- 想把探索性分析整理成可复现 workflow
- 想给研究项目快速生成 Table 1、模型结果和 ROC 图
- 想把常见医学统计方法沉淀成可复用技能

项目还在持续补充中，后面会继续增加更完整的示例、报告模板和更多真实研究场景。

## 互动引导

如果你也在用 AI agent 做数据分析，可以试试把这类方法工作流沉淀成技能库。比起每次重新提示，长期维护一组可复用技能会稳定很多。

## 标签

#Python #医学统计 #数据分析 #AI编程 #开源项目 #JupyterNotebook #统计建模 #科研工具 #CodingAgent #Logistic回归
