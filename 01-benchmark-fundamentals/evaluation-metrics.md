# Evaluation Metrics：先会看最基本的结果

## 1. 为什么要汇总

一个 Trial 只能说明一次运行。想比较多个 Agent、多个任务或多次重复运行，就需要把结果整理成指标。

这个仓库只实现最基础的描述性统计，不涉及复杂的统计推断。

## 2. Pass Rate

假设一共有 `N` 次 Trial，其中 `P` 次通过：

```text
Pass Rate = P / N
```

例如：

```text
总 Trial 数 = 10
通过 = 6
Pass Rate = 6 / 10 = 60%
```

`tools/evaluation-summary/` 里的练习工具把 `failed`、`error` 和 `timeout` 都保留在分母里。这个定义只是本仓库的练习口径，阅读其他 Benchmark 时要先看它自己的指标定义。

## 3. Runtime

### Mean（平均值）

```text
Mean Runtime = 所有运行时间之和 / Trial 数
```

平均值容易被特别长的一次运行拉高。

### Median（中位数）

先把运行时间排序，再取中间位置。中位数通常不那么容易受极端值影响。

因此我在小工具里同时输出 Mean 和 Median。

## 4. 不要只看通过率

下面两个结果的 Pass Rate 都是 50%，但含义不同：

```text
Agent A
- 50% passed
- 50% wrong_output

Agent B
- 50% passed
- 50% environment_error
```

A 更像是任务本身没有完成；B 则可能有一半运行根本没有进入正常评测。

所以至少还应该一起看：

- status 分布；
- failure type；
- runtime；
- 是否存在大量无效运行。

## 5. 一个简单结果表

| status | 含义 |
|---|---|
| `passed` | 达到当前成功标准 |
| `failed` | 运行完成，但结果不符合要求 |
| `error` | 执行或环境发生错误 |
| `timeout` | 超过时间限制 |

不同框架可能使用不同状态名，不要直接照搬这个表。

## 6. 小样本时不要下太大的结论

如果某个 Agent 只跑了 3 次，结果是 2 次通过、1 次失败，`66.7%` 看起来很精确，但样本其实很少。

因此写评测结论时最好同时写：

```text
2 / 3 passed (66.7%)
```

而不是只写一个百分比。

本仓库的 `evaluation-summary` 正是从这种最基础的结果汇总开始练习。
