# Evaluation Summary

这个小工具读取一份 Trial 结果 CSV，然后做最基础的汇总统计。

主要用来练习：

- `csv.DictReader`；
- 数据合法性检查；
- `Counter`；
- Mean / Median；
- Markdown 报告生成；
- `unittest`。

## CSV 格式

必须有这些列：

```text
task_id,agent,trial,status,runtime_seconds,failure_type
```

`status` 只接受：

```text
passed
failed
error
timeout
```

示例数据在：

```text
sample-data/sample-results.csv
```

## 运行

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv
```

保存成 Markdown：

```powershell
python .\tools\evaluation-summary\summary.py .\tools\evaluation-summary\sample-data\sample-results.csv --output .\tools\evaluation-summary\sample-report.md
```

## 单元测试

```powershell
python -m unittest discover -s .\tools\evaluation-summary\tests -v
```

## 当前的 Pass Rate 定义

```text
pass_rate = passed_trials / total_trials
```

也就是说 `failed`、`error`、`timeout` 都保留在分母中。

这个口径只是为了让练习工具简单清楚。真实 Benchmark 的统计口径可能不同，使用时要先看对应项目的定义。
