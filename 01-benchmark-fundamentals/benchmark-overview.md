# Benchmark Overview

## 1. Benchmark 是什么

在 Agent Evaluation 场景中，Benchmark 可以理解为一组结构化的评测任务及其执行与判定规则。它的作用不是单纯“出题”，而是尽可能稳定地回答：

> 一个 Agent 在给定环境、约束和资源条件下，能否完成指定任务？

一个完整的评测过程通常至少涉及：

- **Task**：需要完成的具体任务；
- **Agent**：执行任务的模型或智能体；
- **Environment**：Agent 可以操作的执行环境；
- **Trial**：某个 Agent 对某个 Task 的一次独立执行；
- **Verifier / Tests**：用于判断结果是否满足目标；
- **Metrics**：对多个 Trial 的结果进行汇总。

## 2. 从“问答”到“任务执行”

普通语言模型评测常关注“回答是否正确”，而 Agent Benchmark 更关注一个完整执行过程，例如：

```text
读取任务要求
    ↓
理解环境与约束
    ↓
执行命令 / 修改文件 / 调用工具
    ↓
产生可观察结果
    ↓
Verifier / Tests 检查结果
    ↓
形成 Trial 结果
```

因此，Agent Benchmark 的关键不只是题目难度，还包括：

- 环境是否可复现；
- 任务是否可完成；
- 目标是否清楚；
- 结果是否可验证；
- 失败原因是否能够区分。

## 3. 基本对象

### Task

Task 描述一个可执行问题。一个适合评测的 Task 通常需要明确：

- 初始状态；
- 目标状态；
- 可用资源；
- 操作限制；
- 成功判据。

### Agent

Agent 是执行任务的主体。它可能调用：

- Shell；
- 文件系统；
- 浏览器；
- 编程工具；
- 其他受控工具。

### Environment

Environment 提供任务执行条件，例如：

- 操作系统；
- 文件；
- 软件依赖；
- 网络条件；
- 容器；
- 权限。

### Trial

Trial 是一次具体运行。相同 Task 和 Agent 可以运行多次，因为执行结果可能存在随机性。

### Job

在工程系统中，一次批量评测通常包含多个 Task × Agent × Trial 的组合，可视为一个 Job。

## 4. 一个最小评测闭环

```text
Task
  ↓
Environment
  ↓
Agent Execution
  ↓
Observable Result
  ↓
Verifier / Tests
  ↓
Trial Result
  ↓
Metrics
```

如果其中任何一环设计不稳定，最终指标就可能失去解释力。

## 5. 学习重点

本项目后续模块围绕以下问题展开：

1. 怎样把模糊需求抽象成可执行 Task；
2. 怎样写清任务和约束；
3. 怎样构建可复现 Environment；
4. 怎样设计 Tests / Verifier；
5. 怎样汇总多次 Trial；
6. 怎样在交付前进行质量检查。

> 本文用于公开学习，不代表 Terminal-Bench、Harbor 或其他项目的官方定义。
