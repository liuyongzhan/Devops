import dbutil
import config
db = dbutil.DB(config.db,config.db_host,config.db_user,config.db_passwd)

res = {}
for line in open('log.log'):
    tmp = line.split(' ')
    ip,status = tmp[0] ,tmp[8]
    res[(ip,status)] = res.get((ip,status),0)+1
for l in sorted(res.items(),key=lambda x:-x[1])[:100]:
    sql = 'insert into log (ip,status,count) values ("%s",%s,%s)'%(l[0][0],l[0][1],l[1])
    print sql
    db.execute(sql)
