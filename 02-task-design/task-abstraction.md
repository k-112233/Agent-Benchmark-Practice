# Task Abstraction：把模糊需求拆成可评测任务

## 1. 先看一个不够清楚的需求

> 把这个项目修好。

人看到这句话可能会根据上下文猜，但 Benchmark 不能太依赖猜测。至少还缺这些信息：

- 什么叫“修好”；
- 当前哪里有问题；
- 可以修改哪些内容；
- 最后怎样判断成功。

Task Abstraction 的工作，就是把这些隐含信息摊开。

## 2. 我习惯拆成六项

### Input：给了什么

例如源代码、数据文件、配置文件或题目说明。

### Initial State：开始时是什么状态

```text
project/
├── app.py
├── config.json
└── tests/
```

还要说明已知错误或初始条件。

### Target State：最后要变成什么状态

例如：

- 所有指定测试通过；
- 生成某个输出文件；
- 配置值符合要求。

### Action Space：允许做什么

例如读取文件、修改代码、执行命令、运行测试。

### Constraints：哪些事情不能做

例如：

- 不能改输入文件；
- 不能联网；
- 不能改变公开接口；
- 必须在规定时间内完成。

### Evidence：拿什么证明完成

例如测试结果、输出文件、程序退出码或最终状态。

## 3. 一个最小模板

```text
Input:
    Agent 能看到什么？

Initial State:
    一开始是什么状态？

Target State:
    最后必须达到什么状态？

Allowed Actions:
    允许做什么？

Constraints:
    有哪些限制？

Evidence:
    最后怎么检查？
```

## 4. Evidence 决定任务能不能稳定评测

例如：

> 让代码更优雅。

“优雅”很难稳定判定。

如果改成：

> 不改变公开接口，使给定测试全部通过，并通过指定静态检查。

就有了明确证据。

## 5. 难度不要靠隐藏信息制造

任务可以很难，但必要信息应该给够。真正有价值的难度来自多步骤操作、推理、调试和约束，而不是让 Agent 猜作者没写出来的要求。

Terminal-Bench 当前公开的 task guidelines 也强调任务要 **well specified、solvable、verifiable**。这一点比“看起来复杂”更重要。
