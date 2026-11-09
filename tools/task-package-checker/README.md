# Task Package Checker

一个使用 Python 标准库编写的任务包基础检查器，用于检查学习项目中自定义任务包的结构与必要字段。

> **格式边界：** 本工具使用本仓库自定义的 `task.json` 示例格式，仅用于练习文件检查与元数据校验。它不是 Terminal-Bench、Harbor 或其他平台的官方任务格式，也不代表其完整规范。

## 检查内容

- 必需文件：`task.json`、`instruction.md`、`environment/Dockerfile`
- 必需目录：`tests/`，且至少包含一个 `.py` 文件
- `task.json` 必须是合法 JSON 对象，包含 `id`、`title`、`description`（非空字符串）、`difficulty`（easy/medium/hard）和 `timeout_seconds`（正整数）
- `instruction.md` 不得为空
- 缺少可选字段 `tags` 时只产生警告

## 示例结构

```text
sample-task/
├── task.json
├── instruction.md
├── environment/
│   └── Dockerfile
└── tests/
    └── test_outputs.py
```

## 运行（在仓库根目录）

```powershell
python .\\tools\\task-package-checker\\checker.py .\\tools\\task-package-checker\\sample-task
```

通过时退出码为 `0`；发现错误时退出码为 `1`。

## 运行单元测试

```powershell
python -m unittest discover -s .\\tools\\task-package-checker\\tests -v
```

本工具只检查基础结构和元数据，不验证任务逻辑、Docker 镜像是否成功构建、测试是否真实有效，也不代表任何平台的官方合规检查。仅使用自建或已获授权的练习材料。
