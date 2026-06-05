# Python Medical Statistics Skills

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

`example/lung-cancer` 提供一个完全合成的肺癌风险分析示例。该示例覆盖数据检查、Table 1、t 检验、logistic 回归、ROC/AUC 和图形生成，适合用来验证本项目的医学统计分析工作流。

从仓库根目录运行：

```bash
python3 example/lung-cancer/analysis/analysis.py
```

如需安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

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
