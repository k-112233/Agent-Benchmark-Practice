# Project Audit Script

在项目根目录运行：

```powershell
python .\scripts\project_audit.py
```

它会检查：

1. 六个知识模块和两个工具的预期目录/文件是否存在；
2. 两个工具的单元测试是否通过；
3. 两个工具的示例命令是否能运行；
4. 仓库中是否存在需要人工复核的压缩包、Office/PDF/SPSS 文件或带有内部/客户/验收等关键词的文件。

最后一项仅用于提醒，不会自动判断某个文件是否泄密。GitHub 发布前仍需人工检查公开边界。
