# Dify 文件自动化与文档转换服务

本项目是一个多功能的 **Docker Compose 软件包**，旨在为 **Dify 项目**提供强大的文件自动化上传、Markdown 文档转换以及静态文件托管服务。通过简单的配置，您可以轻松地将服务部署到任何支持 Docker 的环境中。

---

## 📂 项目结构

```

.
├── docker-compose.yml       # Docker Compose 配置文件
├── supervisor.conf          # Supervisor 进程管理配置文件
├── md.py                    # Dify Markdown 文档服务
├── md2docx\_server.py        # Markdown 到 Word 文档转换服务
├── Dockerfile               # Docker 镜像构建文件
├── requirements.txt         # Python 依赖库列表
├── nginx                    # Nginx 配置文件目录
│   └── nginx.conf
├── picture                  # 静态图片托管文件夹
└── logs                     # 日志文件目录

````

---

## 🚀 主要功能

- **Dify 文档服务 (`md.py`)**  
  - 根据指定的场景名称，自动从本地 Markdown 文件中查找并返回相关内容  
  - 支持模糊匹配  

- **Markdown 转 Word 服务 (`md2docx_server.py`)**  
  - 接收 Markdown 内容，通过 Pandoc 转换为 `.docx` 格式的 Word 文档  
  - 提供文档下载链接  

- **静态文件托管 (`nginx-static`)**  
  - 使用 Nginx 容器托管 `picture` 文件夹中的所有静态文件  
  - 可通过公网访问  

---

## ⚙️ 使用方法

### 1. 克隆项目

```bash
git clone <你的项目仓库地址>
cd <你的项目目录>
````

### 2. 配置环境变量

修改 `docker-compose.yml` 文件，根据服务器信息和 Dify 配置填写环境变量：

```yaml
environment:
  - DIFY_SERVER_URL=http://<你的Dify服务器IP或域名>:20000
  - API_KEY=<你的API Key>
  - DATASET_ID=<你的数据集ID>
  - DOWNLOAD_HOST=http://<你的服务器IP或域名>:5000
```

### 3. 添加文件

* **Markdown 文档**：将 `.md` 文件放入 `md_files` 文件夹
* **Word 模板**：如需自定义 Word 样式，放置 `reference.docx` 于项目根目录
* **公开图片**：放入 `picture` 文件夹，通过公网访问

### 4. 运行服务

确保服务器已安装 **Docker** 和 **Docker Compose**，然后运行：

```bash
docker-compose up -d --build
```

---

## 🌐 服务访问

* **Dify 文档服务**：
  `http://<服务器IP>:7000/get_doc`

* **Markdown 转 Word 服务**：
  `http://<服务器IP>:5000/convert`

* **静态图片服务**：
  `http://<服务器IP>:10000/`
  （例如：`http://<服务器IP>:10000/文件名.jpg`）

---

## ⚠️ 注意事项

* **端口占用**：若 `7000`、`5000` 或 `10000` 已被占用，请修改 `docker-compose.yml` 中的 `ports` 配置
* **防火墙设置**：请确保服务器防火墙或云服务商的安全组已开放相应端口（`7000`、`5000`、`10000`），否则外部无法访问

---
