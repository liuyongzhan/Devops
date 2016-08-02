# Devops

cmbd：
cmbd是我的第一个项目。项目大部分数据来自于nginx的log，即目录下的log.log。

### 1. 首先，必须安装好mysql，并创建cmbd数据库和用户名密码：

- create database cmbd character set utf8 collate utf8_bin;
- grant all privileges on cmbd.* to cmbd@localhost identified by '123456';
- flush privileges;

### 2. 然后编辑目录下的config.py文件：
```python
  db = 'cmbd'  #数据库名
  db_user = 'cmbd'  #数据库的用户名
  db_passwd = '123456'  #数据库的密码
  db_host = 'localhost'  #数据库的地址
```
### 3. 创建表，执行createtables.py文件即可：

python createtables.py

### 4. 启动flask：

python flask_web.py

### 5. 打开浏览器，输入http://ip:1212
用户名、密码均为admin


### 6. 数据入库：

  - 日志表格化、日志可视化的数据均由log_col.py收集
  - 用户地理分布的数据由log_map_col.py收集
  - 内存监控的数据由mem_get.py收集


