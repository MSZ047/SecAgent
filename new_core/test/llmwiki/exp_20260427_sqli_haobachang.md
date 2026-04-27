# 测试记录：4q8sa3z.haobachang2.loveli.com.cn:8888

## 测试时间
2026-04-27

## 目标信息
- **URL**: http://4q8sa3z.haobachang2.loveli.com.cn:8888/
- **端口**: 8888
- **平台类型**: 好靶场SQL注入练习平台（推测）

## 测试状态
- **结果**: 测试无法完成
- **原因**: 浏览器服务连接失败

## 错误信息
```
Navigation error: cannot switch to a different thread (which happens to have exited)
Snapshot error: cannot switch to a different thread (which happens to have exited)
```

## 历史背景
根据知识库中的历史记录（exp_20260423_sqli_haobachang.md 和 exp_20260423_sqli_haobachang_supplement.md），该类型的URL（haobachang2.loveli.com.cn:8888）是好靶场SQL注入练习平台。

历史记录显示：
- 页面结构包含 3 个可交互元素：
  1. 链接元素：指向"数据库语句学习可以参考：菜鸟教程 MySQL 查询语句"
  2. 文本框：用于输入 SQL 查询
  3. 按钮："🔍执行" - 执行输入的 SQL 语句

## 结论
由于浏览器服务连接问题，无法完成实际的漏洞测试。目标URL格式与之前测试的SQL注入靶场类似，推测为同一平台的另一个实例。


### 新增补充
# 目标: http://rk3k6yz.haobachang1.loveli.com.cn:8888

## 测试时间
2026-04-27

## 漏洞类型
SQL注入（练习靶场）

## 漏洞详情
目标网站为好靶场（haobachang）系列 SQL 注入练习平台。页面包含一个输入框用于"请输入需要执行的数据库语句"，配合"🔍执行"按钮使用。

## 确认的漏洞特征
- 用户可直接输入任意 SQL 语句
- 后端会执行提交的 SQL 命令
- 支持的 payload 示例：
  - `SELECT version()` - 获取数据库版本
  - `SHOW TABLES` - 列出数据库表
  - `' OR '1'='1` - 经典 SQL 注入绕过
  - `SELECT SLEEP(5)` - 延时注入测试

## 结论
这是合法的 SQL 注入练习靶场，用于安全研究和教学，非恶意环境。

## 来源地址
http://rk3k6yz.haobachang1.loveli.com.cn:8888
