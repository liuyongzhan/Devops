import dbutil
import time
import config
db = dbutil.DB(config.db,config.db_host,config.db_user,config.db_passwd)

def getMem():
    f = open('/proc/meminfo')
    TotalMem = int(f.readline().split()[1])
    FreeMem = int(f.readline().split()[1])
    BufferMem = int(f.readline().split()[1])
    CacheMem = int(f.readline().split()[1])
   # print TotalMem
    used = round((TotalMem-FreeMem-BufferMem-CacheMem)/round(TotalMem,4)*100,2)
   # print used
    sql = 'insert into mem values (%s,%s)'%(used,int(time.time()))
   # print sql
    db.execute(sql)

while True:
    getMem()
    time.sleep(1)
