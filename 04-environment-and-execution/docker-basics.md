# Docker 基础：理解任务运行环境

> 本文面向刚接触 Terminal-Bench / Agent 评测工程的学习者。示例用于理解 Docker 的通用工作方式，不代表任何企业内部任务规范。

## 1. 为什么需要容器

Agent 任务通常不只依赖提示词，还依赖可执行环境：操作系统、命令行工具、运行时、依赖包、初始文件和环境变量等。如果不同机器上的环境不一致，同一个任务可能出现不同结果。

Docker 通过镜像（Image）和容器（Container）把应用运行所需的文件系统、依赖和启动配置封装起来，使环境更容易构建、分发和复现。

- **镜像**：用于创建容器的只读模板，通常由多层文件系统组成。
- **容器**：镜像启动后的隔离运行实例。容器可以运行、停止、删除，也可以在同一镜像上创建多个实例。
- **Dockerfile**：描述如何构建镜像的文本文件。
- **构建上下文**：执行 `docker build` 时发送给构建器的文件集合，通常是 Dockerfile 所在目录或指定目录。

可以先记住：Dockerfile 描述构建过程，镜像保存构建结果，容器承载实际运行过程。

## 2. 最小工作流

### 2.1 检查 Docker 是否可用

```bash
docker --version
docker info
```

`docker --version` 主要显示客户端版本；`docker info` 能进一步检查 Docker Engine 是否正常响应。

### 2.2 编写 Dockerfile

下面是一个通用 Python 环境示例：

```dockerfile
FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "--version"]
```

各指令的作用：

| 指令 | 作用 |
|---|---|
| `FROM` | 指定基础镜像 |
| `WORKDIR` | 设置后续指令的工作目录 |
| `COPY` | 将构建上下文中的文件复制到镜像 |
| `RUN` | 构建镜像时执行命令 |
| `CMD` | 容器启动时的默认命令 |

实际项目应根据依赖和运行要求选择基础镜像，并尽可能固定版本。不要为了示例完整而随意安装不必要的软件包。

### 2.3 构建镜像

在包含 Dockerfile 的目录执行：

```bash
docker build -t practice-env:0.1 .
```

参数含义：

- `-t practice-env:0.1`：为镜像设置名称和标签。
- `.`：将当前目录作为构建上下文。

查看镜像：

```bash
docker images
```

### 2.4 启动容器

```bash
docker run --rm practice-env:0.1
```

常见参数：

- `--rm`：容器退出后自动删除容器。
- `-it`：交互式终端，常用于进入命令行环境。
- `-v`：挂载主机目录或 Docker volume。
- `-w`：指定容器内工作目录。
- `-e`：设置环境变量。
- `--name`：指定容器名称。

例如，挂载当前目录并进入容器：

```bash
docker run --rm -it \
  -v "$PWD:/workspace" \
  -w /workspace \
  practice-env:0.1 \
  bash
```

Windows PowerShell 的路径写法与 Linux/macOS shell 不完全相同，使用时应按本机终端调整挂载路径。

## 3. 容器运行时需要关注的配置

### 3.1 文件挂载

容器内部文件系统与主机文件系统默认隔离。需要让容器读取输入文件或保存输出时，可以使用 bind mount：

```bash
docker run --rm \
  -v /host/project:/workspace \
  -w /workspace \
  practice-env:0.1
```

注意检查：

1. 主机源路径是否存在。
2. 容器目标路径是否正确。
3. 容器内进程是否具有读写权限。
4. 是否意外把敏感文件挂载进容器。

### 3.2 端口映射

如果容器中的服务监听 `8000` 端口，可以通过端口映射让主机访问：

```bash
docker run --rm -p 8000:8000 practice-env:0.1
```

左侧是主机端口，右侧是容器端口。端口映射不等于服务一定可访问；还要确认服务监听地址、容器内防火墙和启动状态。

### 3.3 环境变量

```bash
docker run --rm -e APP_MODE=test practice-env:0.1
```

不要把密码、令牌或其他凭据直接写入 Dockerfile、镜像层或公开仓库。敏感配置应通过安全的运行时注入方式提供。

## 4. 常见问题与排查顺序

| 现象 | 优先检查 |
|---|---|
| `docker` 命令不存在 | Docker 是否安装、终端 PATH 是否正确 |
| 无法连接 Docker daemon | Docker Engine 是否启动、当前用户权限 |
| 构建时找不到文件 | 构建上下文、`.dockerignore`、`COPY` 源路径 |
| 容器启动后立即退出 | `CMD` / `ENTRYPOINT`、进程是否前台运行、日志 |
| 容器内找不到输入文件 | volume 挂载源路径和目标路径 |
| 依赖安装失败 | 包版本、网络、系统依赖、基础镜像 |
| 本机能运行、容器不能运行 | 隐式依赖、路径差异、权限、环境变量、架构差异 |

推荐排查命令：

```bash
docker ps -a
docker images
docker logs <container-name-or-id>
docker inspect <container-name-or-id>
```

排查时先收集错误信息，再定位发生阶段：构建阶段、容器启动阶段，还是任务执行阶段。不要在没有证据时同时修改多个配置。

## 5. 清理资源

```bash
docker container ls -a
docker image ls
docker rm <container-id>
docker rmi <image-id>
```

谨慎使用批量清理命令。删除前确认目标资源不再需要，尤其不要在共享环境中随意清理其他人的容器或镜像。

## 6. 与 Agent 任务评测的关系

在 Agent 任务中，容器通常用于提供相对隔离的执行环境。设计和检查环境时，至少应明确：

- 使用什么基础镜像和软件版本；
- 任务开始时有哪些文件和目录；
- Agent 可以访问哪些路径、命令和资源；
- 任务执行后哪些文件或状态会发生变化；
- 测试或 verifier 在什么环境、什么时点执行；
- 是否依赖网络、外部服务或运行时凭据。

容器隔离有助于降低环境差异，但不自动保证任务公平、结果可复现或安全。仍需对输入、依赖、权限、网络和验证过程进行明确设计。

## 7. 本章练习

1. 使用一个公开基础镜像，构建最小镜像并运行。
2. 将一个自建文本文件挂载到容器中，并在容器内读取。
3. 修改 Dockerfile 中的工作目录，观察相对路径行为。
4. 故意写错一个 `COPY` 路径，记录错误发生在哪个构建阶段。
5. 记录镜像标签、启动命令、挂载路径和运行结果。

练习只使用自建文件和公开数据，不要将实习期间接触的任务包、客户数据或内部材料放入公开仓库。

## 参考资料

- Docker Docs — Docker overview: https://docs.docker.com/get-started/docker-overview/
- Docker Docs — Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker Docs — `docker run`: https://docs.docker.com/reference/cli/docker/container/run/
