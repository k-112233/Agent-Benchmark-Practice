# Agent-Benchmark-Practice

这是一个用于学习 **Agent Benchmark（智能体评测）** 的练习仓库。

我主要参考 Terminal-Bench 和 Harbor 的公开仓库与文档，把看到的概念按自己的理解重新整理，并配了两个可以直接运行的小工具。可以试着把任务设计、环境、测试、评测结果和质量检查这条链路弄明白。

## 这个仓库适合谁

如果你已经会一点 Python、Git 和命令行，但刚接触 Agent 评测，可以按顺序阅读。

## 目录

```text
Agent-Benchmark-Practice/
├── 01-benchmark-fundamentals/      # Benchmark、Task、Trial 等基础概念
├── 02-task-design/                 # 怎样把一个想法整理成可评测任务
├── 03-prompt-engineering/          # 任务指令与约束怎么写清楚
├── 04-environment-and-execution/   # Docker 与可复现运行环境
├── 05-testing-and-evaluation/      # 测试、Verifier、评测结果与失败分析
├── 06-quality-assurance/           # 任务验证与交付前检查
├── tools/
│   ├── task-package-checker/       # 练习任务包的静态检查器
│   └── evaluation-summary/         # 评测结果 CSV 汇总工具
├── scripts/                        # 整个仓库的自检脚本
└── references/                     # 公开资料入口
```

## 推荐阅读顺序

第一次看时可以按下面的顺序：

```text
01 基础概念
   ↓
02 任务设计
   ↓
04 环境与执行
   ↓
05 测试与评测
   ↓
03 Prompt 与约束
   ↓
06 质量检查
   ↓
tools/ 动手运行
```

我把 Docker 放在 Prompt 前面，是因为先理解“任务到底在哪运行、最后怎么判定”，再看 Prompt 会更直观。

## 两个可以直接运行的小工具

### 1. Task Package Checker

位置：`tools/task-package-checker/`

它检查一个自定义练习任务包有没有缺文件、元数据字段是否正确等。这里使用的是本仓库自己定义的简化格式，不是 Terminal-Bench 的官方 task schema。

```powershell
python .\tools\task-package-checker\checker.py .\tools\task-package-checker\sample-task
```

运行单元测试：

```powershell
python -m unittest discover -s .\tools\task-package-checker\tests -v
```

### 2. Evaluation Summary

位置：`tools/evaluation-summary/`

它读取一份合成的 Trial 结果 CSV，计算通过率、运行时间和失败类型分布。

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv
```

生成 Markdown 报告：

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv --output .\tools\evaluation-summary\sample-report.md
```

运行单元测试：

```powershell
python -m unittest discover -s .\tools\evaluation-summary\tests -v
```

## 整个仓库自检

```powershell
python .\scripts\project_audit.py
```

这个脚本会检查目录、两个工具的测试和示例命令，同时提醒是否出现了不适合直接提交到公开仓库的文件类型。

## 资料来源和项目边界

本仓库的概念学习主要参考 Terminal-Bench、Harbor 以及它们的公开文档。示例任务、示例数据和两个 Python 工具是为了练习而单独编写的。

公开项目中的规则会更新，因此涉及官方格式、命令或贡献要求时，应以对应项目当前文档为准。参考入口见 [`references/open-source-projects.md`](references/open-source-projects.md)。

## 环境

两个 Python 工具只使用标准库，建议使用 Python 3.9 或更高版本。

Docker 只用于第 04 部分的环境学习和示例；运行两个 Python 工具本身不要求安装 Docker。

## License

MIT License，见 [LICENSE](LICENSE)。
