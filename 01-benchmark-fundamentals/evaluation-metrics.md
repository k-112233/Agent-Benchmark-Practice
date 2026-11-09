# Evaluation Metrics

## 1. 为什么需要指标

单个 Trial 只能说明一次运行结果。Benchmark 通常需要把多次结果压缩为可比较指标。

本项目采用最基础、最容易解释的指标。

## 2. Pass Rate

设：

- 总 Trial 数为 `N`；
- 成功 Trial 数为 `P`。

则：

```text
Pass Rate = P / N
```

例如：

```text
10 trials
6 passed
4 non-passed
```

则：

```text
Pass Rate = 6 / 10 = 60%
```

本项目工具 `evaluation-summary` 中：

- `failed`
- `error`
- `timeout`

均保留在总 Trial 分母中。

这是一种明确、简单的工程定义，但并不意味着所有 Benchmark 都采用完全相同的口径。

## 3. Runtime

常见运行时间描述包括：

### Mean Runtime

```text
Mean Runtime = sum(runtime_i) / N
```

对极端长时间运行较敏感。

### Median Runtime

将运行时间排序后取中间位置。

Median 对极端值更稳健，因此同时报告 Mean 和 Median 往往更有解释力。

## 4. Status Distribution

除通过率外，应保留各状态数量，例如：

| Status | Meaning |
| --- | --- |
| passed | 达到成功判据 |
| failed | 执行完成但未达到目标 |
| error | 执行或环境发生错误 |
| timeout | 超过时间限制 |

这些状态有助于区分不同类型的问题。

## 5. Failure Categories

进一步可记录：

```text
wrong_output
environment_error
timeout
verification_failure
dependency_error
```

Failure Type 应当服务于诊断，而不是为了增加分类复杂度。

## 6. 指标解释注意事项

同一个 Pass Rate 可能来自完全不同的失败结构。

例如：

```text
Agent A:
50% pass
50% wrong output

Agent B:
50% pass
50% environment error
```

两者的能力问题并不相同。

因此，一个完整报告至少应同时关注：

- Pass Rate；
- Status Distribution；
- Failure Categories；
- Runtime。

## 7. 不应过度解读

本项目的小型工具只做描述性统计，不进行：

- 显著性检验；
- 置信区间估计；
- 模型能力因果推断；
- Benchmark 排名有效性分析。

更严谨的模型比较还应考虑：

- Task 数量；
- Trial 数量；
- Task 难度结构；
- 随机性；
- 环境一致性；
- 评价指标设计。

> 本文中的指标定义服务于本项目练习，不代表任何外部 Benchmark 的完整官方指标体系。
