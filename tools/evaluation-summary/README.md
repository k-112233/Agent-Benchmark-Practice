# Evaluation Summary

一个用于练习 Agent Benchmark 评测结果汇总的小型命令行工具。

## 输入字段

```text
task_id,agent,trial,status,runtime_seconds,failure_type
```

允许的 `status`：`passed`、`failed`、`error`、`timeout`。

## 运行

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv
```

生成 Markdown 报告：

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv --output .\tools\evaluation-summary\sample-report.md
```

测试：

```powershell
python -m unittest discover -s .\tools\evaluation-summary\tests -v
```

通过率定义：

```text
pass_rate = passed_trials / total_trials
```

本工具仅使用合成数据，用于公开学习；不连接真实模型，不执行 Agent，也不代表 Terminal-Bench 或 Harbor 官方实现。
