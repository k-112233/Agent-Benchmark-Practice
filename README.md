# Agent Benchmark Task Design & Evaluation Practice

一个围绕 **Agent Benchmark 任务设计、环境执行、测试验证、结果评测与质量控制** 的公开学习项目。

本仓库不复刻内部生产流程，也不提供真实商业任务；内容来自公开资料、个人学习与独立练习。

## Repository Structure

```text
Agent-Benchmark-Practice/
├── README.md
├── 01-benchmark-fundamentals/
├── 02-task-design/
├── 03-prompt-engineering/
├── 04-environment-and-execution/
├── 05-testing-and-evaluation/
├── 06-quality-assurance/
├── tools/
│   ├── task-package-checker/
│   └── evaluation-summary/
└── references/
    └── open-source-projects.md
```

## Learning Path

1. **Benchmark Fundamentals** — Benchmark、Task、Agent、Environment、Trial、Job、Verifier 与基础评测指标。
2. **Task Design** — 任务抽象、任务规范、可解性与难度设计。
3. **Prompt Engineering** — 目标表达、约束表达、信息边界、歧义控制与迭代修正。
4. **Environment & Execution** — Docker、依赖管理、环境隔离与可复现执行。
5. **Testing & Evaluation** — Test Design、Verifier Design、Model Evaluation 与 Failure Analysis。
6. **Quality Assurance** — 任务描述、文件结构、环境、测试、Verifier、缺陷分级和交付检查。

## Practice Tools

### Task Package Checker

```powershell
python .\tools\task-package-checker\checker.py .\tools\task-package-checker\sample-task
python -m unittest discover -s .\tools\task-package-checker\tests -v
```

这是自定义练习任务包的静态结构检查工具，不执行 Agent、不构建 Docker，也不代表官方任务格式。

### Evaluation Summary

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv
python -m unittest discover -s .\tools\evaluation-summary\tests -v
```

生成 Markdown 报告：

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv --output .\tools\evaluation-summary\sample-report.md
```

当前练习中的通过率：

```text
Pass Rate = Passed Trials / Total Trials
```

## Environment

工具部分仅使用 Python 标准库，建议 Python 3.9+。

## Public Repository Boundary

- 不包含实习单位内部文件
- 不包含客户或平台内部任务包
- 不包含真实商业任务描述
- 不包含内部 Prompt 模板
- 不包含内部验收记录、工作日志或执行轨迹
- 不包含未授权的数据、代码或测试文件
- 示例任务和评测数据使用独立设计或合成数据

本仓库中的 schema、示例与工具均为学习用途，不应被解释为 Terminal-Bench、Harbor 或其他项目的官方实现。

## References

公开项目和资料统一整理在：

```text
references/open-source-projects.md
```

## Status

- [x] Benchmark fundamentals
- [x] Task design
- [x] Prompt engineering
- [x] Environment and execution
- [x] Testing and evaluation
- [x] Quality assurance
- [x] Task Package Checker
- [x] Evaluation Summary
- [ ] Final repository audit
- [ ] Public GitHub release
