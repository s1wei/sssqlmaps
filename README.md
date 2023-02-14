# sssqlmaps
sssqlmaps(GUI)  - 利用python和sqlmap实现的SQL注入批量检测工具

![image](https://www.denceun.com/wp-content/uploads/2023/02/WX20230214-141315@2x.png)

我们在进行进行漏洞扫描时候，sqlmap往往是最常使用的工具之一了

SQLMap 是一个自动化的SQL注入工具，其主要功能是扫描、发现并利用给定URL的SQL注入漏洞，内置了很多绕过插件，支持的数据库是MySQL 、Oracle 、PostgreSQL 、Microsoft SQL Server、Microsoft Access 、IBM DB2, SQ Lite 、Firebird 、Sybase和SAPMaxDB 。

但是在使用中，我们往往得一个个扫描，如果是单个网站还好，若是多个网站（我们往往在挖洞过程中，在资产检索平台导出的一堆数据），所以本次利用python开发出了sssqlmaps工具，很大效率的增加了我们漏洞扫描的效率。

本软件的原理还是利用 subprocess 运行命令行的sqlmap程序，所以使用时候确认本机已有sqlmap并且加入环境变量可以直接运行，例如我在Mac环境或者kali中直接可以运行，而在win中需要在sqlmap.py 所在路径下 将77行注释掉，78行注释取消掉，也就是运行本段：


result = subprocess.run(['python', 'sqlmap.py', '-u', url] + params.split() + ['--batch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
