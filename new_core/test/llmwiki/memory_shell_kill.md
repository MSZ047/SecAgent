# 内存马查杀

## 概述
内存马（Memory Shell）是一种运行在 JVM 内存中的后门程序，没有实际文件落地。主要通过反序列化漏洞、文件上传或 RCE 口子植入。

## 常见服务器 - Tomcat

### Tomcat 作用
- 接收浏览器发来的请求
- 运行 Java 代码（Servlet、JSP、SpringBoot 等）
- 返回结果给浏览器

### Tomcat 三种常见内存马
1. **Filter 型内存马**
2. **Servlet 型内存马**
3. **Listener 型内存马**

## Filter 内存马详解

### Filter 工作原理
```
用户请求 → 服务器 → Filter1 → Filter2 → ... → 业务逻辑
```

所有请求到达 Tomcat 后，必须先经过 Filter 才能到达目标接口/页面。

### Filter 功能
- 查看请求内容
- 修改请求
- 直接拦截请求
- 直接返回结果（不交给业务程序）

### 攻击原理
1. 服务器自动加载所有 Filter
2. 写入恶意 Filter 也会被执行
3. 无需文件落地，直接写入内存

## 相关技术概念

### ClassLoader
- `.java` 文件通过 `javac` 编译生成 `.class` 字节码
- ClassLoader 是 JVM 的类加载器，负责加载字节码到内存
- Filter 如同子弹，ClassLoader 如同发射器

### Shiro 框架
- Shiro = Java 项目中专门做「登录、权限、安全」的框架
- Shiro 反序列化漏洞可直接将恶意 Filter 注入内存

### 利用流程
1. 发送数据包利用 Shiro 漏洞
2. 直接在服务器内存执行代码
3. 使用 ClassLoader 加载 Filter 内存马
4. 通过反射+利用链修改值
5. 在 POST 请求体发送字节码数据

> **注意**：数据包可能较长，Tomcat 可能有限制

## 防御/查杀思路

1. 内存马是 JVM 进程内的代码，无文件落地
2. 检测内存中的异常 Filter/Servlet/Listener
3. 分析 ClassLoader 加载的可疑类
4. 检查反序列化入口和利用链
5. 关注异常的网络通信和行为

## 相关资源
- [整数溢出与支付校验漏洞](./int_overflow_payment_bypass.md)
- [SQL注入分类](./sqli_index.md)
- [API 越权测试](./idor_index.md)