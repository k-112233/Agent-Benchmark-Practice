# Task Package Checker

这是一个很小的 Python 练习工具，用来检查“自定义练习任务包”的基础结构。

它适合用来练习：

- `pathlib` 路径操作；
- 读取 JSON；
- 字段类型检查；
- 错误和警告的区别；
- `unittest`。

## 先说明格式

这里的 `task.json` 是本仓库自己设计的简化格式，不是 Terminal-Bench 或 Harbor 的官方任务格式。

## 它会检查什么

必须存在：

```text
task.json
instruction.md
environment/Dockerfile
tests/
```

其中 `tests/` 至少需要一个 `.py` 文件。

`task.json` 必须包含：

```text
id
title
description
difficulty
timeout_seconds
```

`difficulty` 只允许：

```text
easy
medium
hard
```

`tags` 是可选字段，缺少时只提示 warning。

## 示例目录

```text
sample-task/
├── task.json
├── instruction.md
├── environment/
│   └── Dockerfile
└── tests/
    └── test_outputs.py
```

## 运行

在仓库根目录执行：

```powershell
python .\tools\task-package-checker\checker.py .\tools\task-package-checker\sample-task
```

如果发现错误，程序退出码为 `1`；结构通过则为 `0`。

## 单元测试

```powershell
python -m unittest discover -s .\tools\task-package-checker\tests -v
```

测试覆盖四种情况：正常任务包、缺少 `instruction.md`、非法 difficulty、把布尔值错误地当成 timeout。

## 它没有做什么

这个工具不会：

- 构建 Docker 镜像；
- 真正执行任务；
- 判断测试逻辑是否正确；
- 判断 Task 是否有价值或难度是否合理。

这些属于后续 Task Validation 的范围。
