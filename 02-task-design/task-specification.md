# Task Specification：把任务写到别人能照着做

## 1. Specification 要解决什么问题

Task Abstraction 是把问题拆开，Task Specification 则是把这些信息真正写进任务说明和元数据。

写完后可以问自己一句：

> 一个第一次看到这个任务的人，能不能只根据现有说明知道该做什么、不能做什么、怎样算完成？

## 2. 本仓库的简化练习格式

下面这个 YAML 只是为了说明“任务元数据可以包含什么”，不是 Terminal-Bench 或 Harbor 的官方 schema。

```yaml
id: file-transform-001
title: Normalize configuration file
description: Normalize the configuration and preserve required fields.
difficulty: medium
timeout_seconds: 120

inputs:
  - config/input.json

constraints:
  - Do not rename required public keys.
  - Do not modify files outside the working directory.

success_criteria:
  - output/config.json exists
  - output/config.json is valid JSON
  - required keys pass tests
```

`tools/task-package-checker/` 使用的是更小的 `task.json` 版本，因为它只想练习“读 JSON + 做静态校验”。

## 3. 一份任务说明至少要回答六个问题

| 问题 | 要写清楚的内容 |
|---|---|
| What | 到底要完成什么 |
| Where | 在哪里操作、输出放哪里 |
| Input | 已经提供哪些文件或数据 |
| Allowed | 允许使用什么资源和工具 |
| Forbidden | 明确禁止哪些操作 |
| Success | 最后怎么判断通过 |

如果还有时间、CPU、网络等限制，也应写明。

## 4. 少用“正常处理”“合理完成”这类词

例如：

> 按正常方式修改配置。

问题是“正常”没有固定含义。

更清楚的写法是：

> 保持 `id`、`name`、`version` 不变，只修改 `settings` 中指定字段。

## 5. 说明和测试必须对得上

可以画成：

```text
任务要求
  ↓
成功条件
  ↓
Test / Verifier
```

如果说明要求 A、B、C，而测试只检查 A，那么 B、C 实际上没有可靠评测。

反过来，如果测试突然要求 D，而说明里从未提到 D，也可能把合理答案误判成失败。

## 6. 写完以后自己检查一遍

- [ ] 输入是否真实存在；
- [ ] 输出路径是否明确；
- [ ] 关键约束有没有冲突；
- [ ] 每个重要要求能不能检查；
- [ ] 多种合理实现是否都允许通过；
- [ ] 有没有依赖没有写出来的背景知识。

官方项目的格式会随版本更新。真正制作 Terminal-Bench / Harbor 任务时，应回到它们当前的公开文档核对文件结构和字段。
