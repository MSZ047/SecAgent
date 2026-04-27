# 好靶场SQL注入练习平台测试记录

## 目标信息
- **URL**: http://xy7bc4j.haobachang2.loveli.com.cn:8888
- **端口**: 8888
- **平台类型**: SQL 注入练习平台

## 页面结构分析
页面包含 3 个可交互元素：
1. **链接元素 (e0)**: 指向"数据库语句学习可以参考：菜鸟教程 MySQL 查询语句"
2. **文本框 (e1)**: "请输入需要执行的数据库语句" - 用于输入 SQL 查询
3. **按钮 (e2)**: "🔍执行" - 执行输入的 SQL 语句

## 漏洞分析
这是一个 SQL 注入靶场平台，专门用于练习 SQL 注入攻击。平台功能：
- 用户可以在文本框中输入 SQL 语句
- 点击执行按钮后，后端会执行输入的 SQL 语句
- 存在明显的 SQL 注入漏洞（这是靶场的设计目的）

## 测试限制
- 浏览器工具执行动作时出现 API 错误 (缺少 kind 字段)
- 无法进行进一步的交互测试

## 结论
这是一个合法的 SQL 注入练习靶场，设计用于安全研究和教学目的。非恶意用途。

## 测试时间
2026-04-23

### 补充更新

## 补充测试记录 (2026-04-23)

### 新增目标
- **URL**: http://4q8sa3z.haobachang2.loveli.com.cn:8888/
- **端口**: 8888
- **平台类型**: SQL 注入练习平台（好靶场）

### 测试结果
- **状态**: 受限于浏览器服务连接问题，无法完成实际漏洞测试

### 技术问题
浏览器服务在测试期间持续返回错误：
- `navigate_to_url`: "cannot switch to a different thread (which happens to have exited)"
- `get_snapshot_interactive`: "Snapshot error: cannot switch to a different thread"

### 平台分析
根据 Wiki 历史记录，该目标属于"好靶场SQL注入练习平台"系列，同系列目标包括：
- http://xy7bc4j.haobachang2.loveli.com.cn:8888
- http://hq4zqkb.haobachang1.loveli.com.cn:8888

这些平台为合法的 SQL 注入练习靶场，用于安全研究和教学目的。

### 已知页面结构
1. **链接元素**: 指向"数据库语句学习可以参考：菜鸟教程 MySQL 查询语句"
2. **文本框**: "请输入需要执行的数据库语句" - 用于输入 SQL 查询
3. **按钮**: "🔍执行" - 执行输入的 SQL 语句

### 结论
- 目标为合法 SQL 注入练习靶场
- 由于浏览器服务问题，无法完成实际的漏洞测试
- 需要等待浏览器服务恢复后重新测试

### 补充更新

---

## 漏洞详情补充

- **漏洞类型**: SQL注入
- **严重级别**: Critical
- **CVSS评分**: 9.8

### 漏洞位置
- 页面：首页
- 参数：testInput（SQL语句输入框）

### 成功Payload
```sql
SELECT * FROM flag
```

### 漏洞利用过程
1. 访问目标网站，发现页面提示"flag 在 flag 表中"
2. 在 SQL 语句输入框中输入 `SELECT * FROM flag`
3. 点击执行按钮
4. 成功获取 flag 表数据：
   - id: 1
   - flag: flag{0eff4eef1df44ed8bd89c50c88a4cfb1}
   - description: flag

### 修复建议
1. 使用参数化查询（Prepared Statements）替代字符串拼接
2. 对用户输入进行严格的白名单校验
3. 以最小权限原则配置数据库账户

来源地址：http://rk3k6yz.haobachang1.loveli.com.cn:8888
