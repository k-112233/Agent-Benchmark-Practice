# Docker 基础：先理解任务为什么要放进环境里运行

## 1. Docker 在 Agent 评测里解决什么问题

一个任务能不能跑起来，不只由代码决定，还和操作系统、Python 版本、依赖、文件路径、环境变量等有关。

如果每个人都直接在自己的电脑上运行，同一个 Task 很容易出现不同结果。Docker 的作用之一，就是把这些运行条件尽量固定下来。

先认识四个词：

- **Dockerfile**：写“镜像怎么构建”的文本文件；
- **Image（镜像）**：构建出来的环境模板；
- **Container（容器）**：镜像真正启动后的运行实例；
- **Build context（构建上下文）**：`docker build` 时能被构建器看到的文件集合。

可以先这样记：

```text
Dockerfile → build → Image → run → Container
```

## 2. 先确认 Docker 能用

```bash
docker --version
docker info
```

`docker --version` 能看到 Docker CLI 版本；`docker info` 还能帮助确认 Docker Engine 是否正常工作。

## 3. 一个最小 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "--version"]
```

逐行看：

| 指令 | 作用 |
|---|---|
| `FROM` | 选择基础镜像 |
| `WORKDIR` | 设置后续命令的工作目录 |
| `COPY` | 把本地构建上下文中的文件复制进去 |
| `RUN` | 构建镜像时执行命令 |
| `CMD` | 容器启动时的默认命令 |

## 4. 构建和运行

构建：

```bash
docker build -t practice-env:0.1 .
```

运行：

```bash
docker run --rm practice-env:0.1
```

这里：

- `-t` 给镜像起名字和标签；
- `.` 表示当前目录是构建上下文；
- `--rm` 表示容器退出后自动删除这个容器实例。

## 5. 文件挂载

容器默认看不到主机上的全部文件。需要把目录交给容器时，可以使用 bind mount：

```bash
docker run --rm \
  -v /host/project:/workspace \
  -w /workspace \
  practice-env:0.1
```

左边是主机路径，右边是容器内路径。

Windows PowerShell、macOS 和 Linux 的路径写法可能不同。遇到“容器里找不到文件”，先检查挂载路径，而不是马上改代码。

## 6. 环境变量和端口

传入一个普通环境变量：

```bash
docker run --rm -e APP_MODE=test practice-env:0.1
```

端口映射：

```bash
docker run --rm -p 8000:8000 practice-env:0.1
```

不要把密码或 API Key 直接写进 Dockerfile 并提交到公开仓库。

## 7. 常见报错先查什么

| 现象 | 先检查 |
|---|---|
| 找不到 `docker` 命令 | Docker 是否安装、PATH 是否正确 |
| 无法连接 daemon | Docker Engine 是否启动 |
| `COPY` 找不到文件 | 构建上下文和 `.dockerignore` |
| 容器启动就退出 | `CMD` / `ENTRYPOINT` 和日志 |
| 容器看不到输入文件 | volume 挂载路径 |
| 本机能跑、容器不能跑 | 隐式依赖、权限、路径、环境变量 |

常用排查命令：

```bash
docker ps -a
docker images
docker logs <container-id>
docker inspect <container-id>
```

## 8. 为什么这和 Benchmark 有关

在 Agent 评测里，Environment 本身就是实验条件。至少应知道：

- 任务从什么镜像启动；
- 一开始有哪些文件；
- Agent 能访问什么；
- 是否允许联网；
- 任务运行多久会超时；
- 最后由什么测试检查结果。

容器只能帮助隔离环境，并不会自动保证任务公平或可复现，后面还需要固定依赖、输入和验证方式。

## 9. 动手练习

1. 用公开基础镜像构建一个最小 Python 容器；
2. 把一个自己创建的文本文件挂载进去；
3. 在容器内读取这个文件；
4. 故意写错一个 `COPY` 路径，看报错发生在哪一步；
5. 把构建命令和运行命令记录下来。

## 参考

- Docker overview: https://docs.docker.com/get-started/docker-overview/
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- `docker run`: https://docs.docker.com/reference/cli/docker/container/run/
