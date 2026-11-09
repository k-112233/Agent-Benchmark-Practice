# Task Specification

## 1. 任务规范的目的

Task Specification 用于把已经抽象出的任务转化为稳定、可检查的文字和元数据。

一个合格的规范应尽量做到：

- 信息完整；
- 成功条件明确；
- 约束一致；
- 不依赖隐含知识；
- 可映射到测试或 Verifier。

## 2. 一个自定义练习 Schema

下面是本项目为了学习自行设计的示例，**不是 Terminal-Bench、Harbor 或其他项目的官方 schema**：

```yaml
id: file-transform-001
title: Normalize configuration file
description: >
  Normalize the provided configuration while preserving
  the required public fields.
difficulty: medium
timeout_seconds: 120

inputs:
  - config/input.json

constraints:
  - Do not rename required public keys.
  - Do not modify files outside the working directory.

success_criteria:
  - output/config.json exists
  - output file is valid JSON
  - required keys and values pass tests
```

本项目的 `task-package-checker` 使用了更小的 `task.json` 元数据集合进行练习。

## 3. Specification 应回答什么

### What

到底要完成什么？

### Where

在哪些文件、目录或环境中完成？

### Allowed

允许使用什么资源和操作？

### Forbidden

哪些操作明确禁止？

### Success

什么结果才算完成？

### Time / Resource

是否存在超时、调用次数或资源限制？

## 4. 避免隐含约束

不推荐：

> “按照正常方式处理。”

因为“正常”无法稳定解释。

更好：

> “保持 `id`、`name` 和 `version` 字段不变，仅修改 `settings` 中的指定值。”

## 5. Specification 与 Verifier 对齐

理想关系：

```text
Task Requirement
      ↓
Success Criterion
      ↓
Test / Verifier Check
```

如果任务说明要求 A、B、C，而 Verifier 只检查 A，那么 B、C 实际上无法被可靠评测。

反过来，如果 Verifier 检查了任务说明没有要求的 D，也可能造成不公平失败。

## 6. 完整性检查

在提交任务前，可以逐项确认：

- [ ] 输入是否存在；
- [ ] 目标是否明确；
- [ ] 成功条件是否可验证；
- [ ] 约束是否必要；
- [ ] 说明和测试是否一致；
- [ ] 是否存在多种合理答案；
- [ ] 多种合理答案是否都能通过；
- [ ] 是否依赖未说明的外部信息。

## 7. 学习项目边界

本项目不会复制实际商业任务规范。

公开仓库中的示例：

- 使用自定义结构；
- 使用合成数据；
- 仅用于展示任务工程方法；
- 不代表任何外部 Benchmark 的官方格式。
