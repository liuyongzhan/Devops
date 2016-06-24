import dbutil
import config
db = dbutil.DB(config.db,config.db_host,config.db_user,config.db_passwd)

def createtables():
    user_table = 'create table if not exists user (id int not null auto_increment primary key,username varchar(255) not null,password varchar(255) not null) charset=utf8;'
    zichan_table = 'create table if not exists zichan (id int not null auto_increment primary key,hostname varchar(50) not null,cpu varchar(50) not null,mem int not null,exdate varchar(50) not null,author varchar(50) not null,note varchar(400) not null) charset=utf8;'
    log_table = 'create table if not exists log (id int not null auto_increment primary key,ip varchar(20) not null,status int not null,count int not null) charset=utf8;'
    mem_table = 'create table if not exists mem (mem float not null,time int not null) charset=utf8;'
    log_map_table = 'create table if not exists log_map (id int not null auto_increment primary key,ip varchar(20) not null,province varchar(200),geox varchar(200),geoy varchar(200),count int) charset=utf8;'
    db.execute(user_table)
    db.execute(zichan_table)
    db.execute(log_table)
    db.execute(mem_table)
    db.execute(log_map_table)

if __name__=="__main__" :
    create = createtables()
