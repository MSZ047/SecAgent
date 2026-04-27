# 文件上传漏洞

## 概述
文件上传漏洞是指攻击者通过恶意上传木马文件获取服务器权限的安全漏洞。


## 攻击技术

### 一句话木马
```php
<?php @eval($_POST['cmd']);?>
```
- **<?php**：PHP语言起始标记
- **@**：错误抑制符，避免信息暴露
- **eval()**：执行传入的字符串作为PHP代码
- **$_POST['cmd']**：接收HTTP POST传递的cmd参数

### 文件后缀绕过
常见绕过方法：
1. 修改文件后缀：php → phtml
2. 修改Content-Type绕过MIME检测
3. 创建图片马：结合图片文件与木马
4. 利用大小写混合

### 连接工具
- 中国蚁剑（antsword）：Webshell管理工具

## 防御策略

### 限制文件后缀
- 仅允许特定后缀如jpg、png上传
- 建立白名单机制

### MIME类型校验
- 检测文件content-type
- 验证文件真实类型

### 文件内容检查
- 分析文件头内容
- 使用图像处理库验证

### 权限控制
- 上传目录不给执行权限
- 文件存储与Web目录分离

## 相关工具
- Nmap：端口扫描
- Dirb：目录扫描
- 中国蚁剑：Webshell管理
- Burp Suite：抓包改包

## 参考文档
- [端口与服务扫描](./port_service_scan.md)
- [横向越权测试](./horizontal_privilege_escalation.md)