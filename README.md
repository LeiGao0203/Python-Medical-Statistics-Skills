# Python Medical Statistics Skills

![Python Medical Statistics Skills banner](docs/assets/readme-banner.png)

[English](README.en.md)

Python Medical Statistics Skills 是一组面向 AI coding agent 的医学统计与 Python 数据分析技能。项目采用通用 `SKILL.md` 结构，既可用于 Codex，也可被其他支持技能目录的 coding agents 读取和执行。

## 项目定位

本项目提供面向医学研究场景的统计方法指导、Python 分析工作流、脚本模板和 Jupyter notebook 工作流。它适合让 agent 辅助完成数据检查、统计建模、结果表格、可视化和可复现分析。

推荐 Python 技术栈包括：

- `pandas`
- `numpy`
- `scipy`
- `statsmodels`
- `scikit-learn`
- `lifelines`
- `matplotlib`
- `seaborn`

## 内容

- `basic-stats`: 基础统计方法技能，包括 t 检验、卡方检验、ANOVA、相关分析、非参数检验、ROC 和样本量估计。
- `advanced-stats`: 高级统计方法技能，包括 logistic 回归、多元回归、生存分析和 PCA。
- `literature-stats`: 文献与研究设计相关技能，包括倾向评分匹配和亚组分析。
- `python-script`: 面向可复现医学统计分析的纯 Python 脚本工作流。
- `jupyter-notebook`: 面向探索、教学和报告的 Jupyter notebook 工作流。
- `example`: 可运行示例项目。

## 推荐工作流

- 使用 `python-script` 创建可复现的纯 Python 分析脚本，适合正式分析、批处理和版本控制。
- 使用 `jupyter-notebook` 创建探索性分析、教程式 notebook 或实验记录。
- 按研究问题调用具体方法技能，例如 `basic-stats/ttest`、`advanced-stats/logistic-reg` 或 `advanced-stats/survival`。

## 示例

`example/lung-cancer` 是一个可直接运行的肺癌问卷数据分析案例，使用 Kaggle Lung Cancer Survey 风格数据（309 条记录，16 个变量，结局变量为 `LUNG_CANCER`）。它展示了 agent 如何把医学统计技能串成一条完整的 Python 分析工作流：

- 数据读取、变量名清洗、二分类变量重编码和缺失值检查。
- 按肺癌状态分层的 Table 1。
- 分类变量的卡方检验 / Fisher 精确检验。
- 年龄的 Welch t 检验与 Mann-Whitney U 检验。
- 多变量 logistic 回归、OR 与 95% CI 输出。
- ROC/AUC、5 折交叉验证 AUC、最佳阈值和图形导出。
- 预测因子相关性热图、PCA 风险模式图、分层 OR 森林图。
- 校准曲线、风险分位表、症状聚类图、模型比较和 permutation importance。

从仓库根目录先安装示例依赖，再运行分析：

```bash
python3 -m pip install -r requirements.txt
python3 example/lung-cancer/analysis/lung_cancer_analysis.py
```

分析结果会写入 `example/lung-cancer/analysis/outputs/kaggle_survey/`。当前示例输出包括 Table 1、检验结果、logistic 回归 OR 表、ROC 阈值表、相关性矩阵、PCA 载荷、校准表、风险分位表、分层 OR 表、模型比较表、置换重要性表和 9 张 PNG 图。

一次示例运行得到的 5 折交叉验证 logistic AUC 为 `0.9397`，表观 logistic AUC 为 `0.9674`，随机森林 5 折交叉验证 AUC 为 `0.9168`。显著的多变量 logistic 回归预测因子包括 smoking、peer pressure、chronic disease、fatigue、allergy、coughing 和 swallowing difficulty。PCA 前两个主成分解释约 `32.0%` 的预测因子方差；随机森林置换重要性最高的变量包括 allergy、swallowing difficulty、peer pressure、alcohol consuming 和 fatigue。

代表性输出图：

![Adjusted odds ratio forest plot](docs/assets/example-figures/fig2_forest_plot_OR.png)

![ROC curve](docs/assets/example-figures/fig3_roc_curve.png)

## 安装

Codex 默认安装到 `${CODEX_HOME:-$HOME/.codex}/skills`：

```bash
curl -fsSL https://raw.githubusercontent.com/LeiGao0203/Python-Medical-Statistics-Skills/main/install.sh | bash
```

其他 coding agent 可通过 `AGENT_SKILLS_DIR` 指定技能目录：

```bash
curl -fsSL https://raw.githubusercontent.com/LeiGao0203/Python-Medical-Statistics-Skills/main/install.sh | AGENT_SKILLS_DIR=/path/to/agent/skills bash
```

## 许可

本项目原创工作流、工具、示例和文档采用 [Apache-2.0](LICENSE) 许可。改编的方法指导内容在适用情况下采用 CC BY-SA 4.0 授权；详情见 [NOTICE](NOTICE)。

## 贡献

欢迎阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献方式。
