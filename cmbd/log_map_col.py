import config
import dbutil
import requests
db = dbutil.DB(config.db,config.db_host,config.db_user,config.db_passwd)
 
res = {}
for line in open('log.log'):
    tmp = line.split(' ')
    ip = tmp[0]
    res[ip] = res.get(ip,0)+1
 
token = 'q5mTrTGzCSVq5QmGpI9y18Bo'
 
for key,val in res.items():
    #if val<100:
    #    continue
    url = 'http://api.map.baidu.com/location/ip?ak='+token+'&ip=%s&coor=bd09ll'%(key)
    r = requests.get(url)
    geo_data = r.json()
    if geo_data['status']==0:
        tmp = (key,geo_data['content']['address_detail']['province'],geo_data['content']['point']['x'],geo_data['content']['point']['y'],val)
        sql = 'insert into log_map(ip,province,geox,geoy,count) values ("%s","%s","%s","%s",%s)'%tmp
        print sql
        db.execute(sql)
