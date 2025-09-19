# 使用官方Python 3.10作为基础镜像
FROM python:3.10-slim-bullseye

# 替换apt镜像源为阿里云
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    pandoc \
    supervisor \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# 设置容器内部的工作目录为 /app
WORKDIR /app

# 将本地的 requirements.txt 文件复制到容器的 /app 目录下
COPY requirements.txt ./

# 将项目目录中的所有其他文件复制到容器的 /app 目录下
COPY . .

# 使用 pip 安装所有在 requirements.txt 文件中列出的Python库
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 声明容器会监听哪些端口
EXPOSE 7000 5000

# 这是容器启动时执行的默认命令，运行 supervisord
CMD ["/usr/bin/supervisord", "-c", "supervisor.conf"]