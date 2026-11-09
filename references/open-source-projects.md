# Open Source References

本文件只收录公开资料，用于本项目学习与延伸阅读。

## Terminal-Bench

Repository:

https://github.com/harbor-framework/terminal-bench

README:

https://github.com/harbor-framework/terminal-bench/blob/main/README.md

Tasks overview:

https://github.com/harbor-framework/terminal-bench/blob/main/tasks/README.md

Contribution guide:

https://github.com/harbor-framework/terminal-bench/blob/main/CONTRIBUTING.md

Task proposal / review guidance:

https://github.com/harbor-framework/terminal-bench/blob/main/docs/prompts/task-proposal.md

Terminal-Bench 将任务质量强调为可解、可验证、说明充分，并通过公开贡献与审查流程持续迭代。本文档仅把这些公开原则作为学习参考，不复制任何内部任务。

## Harbor

Repository:

https://github.com/harbor-framework/harbor

Harbor 是 Terminal-Bench 所使用的公开 Agent evaluation framework 之一，可用于理解 Task、Agent、Environment、Trial、Job 等工程对象之间的关系。

## 本项目与上述项目的关系

`Agent-Benchmark-Practice`：

- 不是 Terminal-Bench 的 fork；
- 不是 Harbor 的实现替代；
- 不使用任何私有任务；
- 不宣称自定义 schema 是官方 schema；
- 只基于公开资料总结通用任务设计、测试、评测和 QA 方法；
- 所有练习数据与示例任务均应保持独立设计或合成。

## 使用建议

阅读顺序可以是：

```text
Terminal-Bench README
        ↓
Terminal-Bench task / contribution docs
        ↓
Harbor repository and documentation
        ↓
本仓库 01–06 学习模块
        ↓
本仓库 tools/
```
