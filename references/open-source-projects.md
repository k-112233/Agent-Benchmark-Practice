# 公开资料入口

这个仓库主要根据下面这些公开项目和文档学习。官方项目更新很快，如果本仓库的某个命令、目录结构或术语与最新官方文档不一致，以官方内容为准。

## Terminal-Bench

仓库：

https://github.com/harbor-framework/terminal-bench

README：

https://github.com/harbor-framework/terminal-bench/blob/main/README.md

当前任务指南：

https://github.com/harbor-framework/terminal-bench/blob/main/docs/task-guidelines.md

贡献说明：

https://github.com/harbor-framework/terminal-bench/blob/main/CONTRIBUTING.md

我在学习任务设计时主要关注 task guidelines 里的几个原则：

- Verifiable；
- Well specified；
- Solvable；
- Difficult for a good reason；
- Realistic / valuable / interesting；
- Outcome-verified。

这些原则适合用来理解“为什么一个任务能成为 Benchmark”，但具体任务文件格式仍然要看官方当前版本。

## Harbor

仓库：

https://github.com/harbor-framework/harbor

官网与文档入口：

https://www.harborframework.com/

Harbor 是一个用于构建、运行和分析 Agent / Language Model 评测的框架，也是理解 Task、Trial、Job、环境和评测运行流程的重要参考。

## Docker

Docker overview：

https://docs.docker.com/get-started/docker-overview/

Dockerfile reference：

https://docs.docker.com/reference/dockerfile/

## GitHub

GitHub Docs：

https://docs.github.com/

主要用于学习仓库管理、README、Git 操作和公开仓库的基本安全检查。

## 本仓库自己的部分

`tools/task-package-checker/` 使用自定义的简化 `task.json`，目的是练习 Python 文件检查，不是 Terminal-Bench task schema。

`tools/evaluation-summary/` 使用合成 CSV，目的是练习最基础的 Trial 结果汇总，也不是 Harbor 的结果解析器。
