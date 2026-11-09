# Model Evaluation：从几次 Trial 得到一个可读结果

## 1. 先把实验条件记下来

一个 Agent 的结果不只受模型影响，还可能受到这些因素影响：

- Agent 框架；
- Prompt；
- 工具权限；
- 环境；
- 超时；
- 任务版本；
- Verifier 版本。

所以比较两个结果之前，先确认条件是否真的可比。

## 2. Trial 和 Job

初学时可以这样理解：

```text
Trial = 某个 Agent 跑某个 Task 的一次记录
Job   = 一批 Trial 组成的评测作业
```

Harbor Hub 的 Jobs 页面也会显示一个 Job 中包含多少 Trials。

## 3. 最基础的指标

### Pass Rate

```text
Pass Rate = passed trials / total trials
```

但必须说明分母包含什么。例如环境错误、取消运行要不要算进去，不同项目可能不同。

### Runtime

至少可以报告：

- Mean；
- Median；
- timeout 数量。

### Failure Type

例如：

```text
wrong_output
environment_error
timeout
verifier_error
```

分类的目的不是显得复杂，而是帮助解释“为什么没通过”。

## 4. 比较 Agent 时尽量控制变量

最好保持：

- 相同 Task 和版本；
- 相同环境；
- 相同工具权限；
- 相同超时；
- 相同 Verifier；
- 相同 Trial 次数。

否则结果差异可能不是模型本身造成的。

## 5. 单次结果很容易误导

例如两个 Agent 各跑一次：

```text
A: pass
B: fail
```

这只能说明这两次运行的结果，不足以说明 A 一定比 B 稳定。

如果条件允许，多运行几次，并同时报告原始数量：

```text
A: 4 / 5 passed
B: 3 / 5 passed
```

样本很少时，不要把小的百分比差异写成确定结论。

## 6. 一个够用的分析结构

写评测结果时可以按：

1. 一共多少 Task / Trial；
2. 通过了多少；
3. 运行时间怎样；
4. 失败主要集中在哪些类型；
5. 实验条件是否一致；
6. 哪些结论目前不能下。

## 7. 配套练习

`tools/evaluation-summary/` 提供了一份合成 CSV：

```text
task_id,agent,trial,status,runtime_seconds,failure_type
```

可以先运行它，看看 Pass Rate、Mean、Median 和 Failure Type 是怎样从原始记录算出来的。
