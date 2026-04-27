# CTF常用Payload知识库

本页面汇总了CTF比赛中常用的 Payload 及 bypass 技术。

## 目录
- [命令注入](./command_injection.md)
- [SQL注入](./sqli_payload.md)
- [跨站脚本](./xss_payload.md)
- [文件包含](./lfi_rfi.md)
- [文件上传绕过](./file_upload_bypass.md)
- [服务端模板注入](./ssti.md)
- [反序列化漏洞](./deserialization.md)
- [服务端请求伪造](./ssrf.md)
- [XML外部实体注入](./xxe.md)
- [常用Shell及回连Payload](./shell_payload.md)

## 快速索引

### 命令执行
| 场景 | 关键技术 |
|------|----------|
| 空格过滤 | ${IFS}, $IFS$9, %09, <> |
| 命令黑名单 | base64编码绕过 |
| 反弹shell | bash -c, nc, python, php |

### Web漏洞
| 漏洞类型 | 核心Payload |
|----------|-------------|
| SQL注入 | UNION SELECT, 布尔盲注, 时间盲注, 报错注入 |
| XSS | script标签, img onerror, svg onload |
| 文件上传 | 扩展名绕过, Content-Type绕过, 图片马 |
| SSTI | {{7*7}}, ${7*7} 探测 |
| SSRF | 127.0.0.1, gopher协议, file:// |

### 辅助技术
- [反弹Shell合集](./shell_payload.md)
- [文件包含姿势](./lfi_rfi.md)
- [bypass技巧](./bypass_techniques.md)