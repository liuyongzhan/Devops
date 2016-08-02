#!/usr/bin/env python
#coding=utf-8
from flask import Flask, render_template,request,redirect,session
app=Flask(__name__)
import dbutil
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import config
db = dbutil.DB(config.db,config.db_host,config.db_user,config.db_passwd)
from functools import wraps
import os
#app.secret_key = os.urandom(32)
app.secret_key = 'j32132sadfadsfash3inrsaui7yp32iwjkskl'

def login_required(func):
    @wraps(func)
    def wraper_function(*args,**kwargs):
        if session.get('user') is None:
            return redirect('/login')
        return func(*args,**kwargs)
    return wraper_function

@app.route('/login',methods=['get','post'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        user = request.form.get('ur')
        pwd = request.form.get('pw')
        if user=='admin' and pwd=='admin':
            session['user']='admin'
            return 'ok'
        else:
            sql = 'select * from user where username="%s" and password="%s"'%(user,pwd)
            res = db.execute(sql)
            if len(res)>0:
                session['user'] = user
                print session
                return 'ok'
            else:
                return 'error'

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/login')

@app.route('/')
@login_required
def index():
   # print session
    if session['user']=='admin':
        res = 'select * from user'
        username = session['user']
        return render_template('index.html',userlist=res,username=username)
    else:
        return redirect('/zichan') 

@app.route('/adduser',methods=['POST'])
@login_required
def adduser():
    user = request.form.get('user')
    pwd = request.form.get('pwd')
   # print request.method
    print user,pwd
    if user != '' and pwd != '' and ' ' not in user and ' ' not in pwd:
        sql='insert into user (username,password) values ("%s","%s")' %(user,pwd)
       # print sql
        try:
            db.execute(sql)
        except:
            return 'error'
        else:
            return 'ok'
    else:
        return 'error'

@app.route('/deluser')
@login_required
def deluser():
    ida = request.args.get('id')
    sql= 'delete from user where id=%s' %(ida)
    db.execute(sql)
    return 'ok'

@app.route('/updateuser',methods=['POST'])
@login_required
def updateuser():
    ida = request.form.get('id')
    pwd = request.form.get('pwd')
    sql = 'update user set password="%s" where id=%s'%(pwd,ida)
   # print sql
   # print id
    db.execute(sql)
    return 'ok'

@app.route('/log')
@login_required
def log():
    user = session['user']
    sql = 'select * from log'
    res = db.execute(sql)
    return render_template('log.html',logs=res,username=user)

@app.route('/ksh')
@login_required
def ksh():
    user = session['user']
    return render_template('ksh.html',username=user)
@app.route('/nglog')
@login_required
def nglog():
    sql = 'select * from log'
    log_data = db.execute(sql)
    log_pre = {}
    for log in log_data:
        log_pre[log[2]] = log_pre.get(log[2],0)+log[3]
    res = {'legend':[],'data':[]}
    for status,count in log_pre.items():
        status = str(status)
        res['legend'].append(status)
        res['data'].append({'name':status,'value':count})
    return json.dumps(res)

@app.route('/meminfo')
@login_required
def meminfo():
    user = session['user']
    return render_template('/meminfo.html',username=user)
@app.route('/memdata')
@login_required
def memdata():
    sql = 'select * from mem'
    res = db.execute(sql)
    data = {'x':[],'data':[]}
    for mem in res:
        data['x'].append(mem[1])
        data['data'].append({'name':mem[1],'value':[mem[1]*1000,mem[0]]})
    #data['min'] = 15
    #data['min'] = min(data['data'])
    return json.dumps(data)


@app.route('/lianxifs')
@login_required
def lianxifs():
    return render_template('lianxifs.html')

@app.route('/gettable')
@login_required
def gettable():
    sql = 'select * from user order by id'
    res = json.dumps(db.execute(sql))
    #print res
    return res

@app.route('/zichan')
@login_required
def zichan():
    username=session['user']
    return render_template('zichan.html',username=username)
@app.route('/getzichan')
@login_required
def getzichan():
    sql = 'select * from zichan order by id'
    res = json.dumps(db.execute(sql))
    #print res
    return res

@app.route('/addhost',methods=['POST'])
@login_required
def addhost():
    '''
    hostname = request.form.get('hostname')
    cpu = request.form.get('cpu')
    mem = request.form.get('mem')
    exdate = request.form.get('exdate')
    author = request.form.get('author')
    note = request.form.get('note')
    sql='insert into zichan (hostname,cpu,mem,exdate,author,note) values ("%s","%s","%s","%s","%s","%s")' %(hostname,cpu,mem,exdate,author,note)
    '''
    #注释的这7行同等以下的3行
    data = dict(request.form)
    ZiChan = ['hostname','cpu','mem','exdate','author','note']
    sql='insert into zichan (%s) values (%s)'%(','.join(ZiChan),','.join(['"%s"'%data[x][0] for x in ZiChan]))
    try:
        db.execute(sql)
    except:
        return 'error'
    else:
        return 'ok'

@app.route('/delhost')
@login_required
def delhost():
    ida = request.args.get('id')
    sql= 'delete from zichan where id=%s' %(ida)
    db.execute(sql)
    return 'ok'

@app.route('/updatehost',methods=['POST'])
@login_required
def updatehost():
    '''
    ida = request.form.get('id')
    hostname = request.form.get('hostname')
    cpu = request.form.get('cpu')
    mem = request.form.get('mem')
    exdate = request.form.get('exdate')
    author = request.form.get('author')
    note = request.form.get('note')
    sql = 'update zichan set hostname ="%s",cpu ="%s",mem ="%s",exdate ="%s",author ="%s",note ="%s" where id=%s'%(hostname,cpu,mem,exdate,author,note,ida)
    '''
    #注释的8行代码同等以下5行
    data = dict(request.form)
    #ida = data.get('id',None)
    #data = data.get('data',None)
    ida = data.get('id',None)[0]
    ZiChan = ['hostname','cpu','mem','exdate','author','note']
    conditions = ["%s='%s'" %(k,data[k][0]) for k in ZiChan]
    sql = 'update zichan set %s where id=%s'%(','.join(conditions),ida)
    db.execute(sql)
    return 'ok'

@app.route('/dl')
@login_required
def dl():
    user = session['user']
    return render_template('dl.html',username=user)
@app.route('/mapdata')
@login_required
def mapdata():
    sql = 'select province from log_map'
    map_data = db.execute(sql)
    res = {'data':[]}
    tmpdict = {}
    for m in map_data:
        tmpdict[m[0]] = tmpdict.get(m[0],0)+1
    res['max'] = max([v for k,v in tmpdict.items()])
    res['min'] = min([v for k,v in tmpdict.items()])
    for k,v in tmpdict.items():
        res['data'].append({
            'name':k.rstrip('省市回维吾尔壮族自治区'),
            'value':v
        })
    return json.dumps(res)
@app.route('/pandata')
@login_required
def pandata():
    sql = 'select province from log_map'
    pan_data = db.execute(sql)
    pan_dict = {}
    for log in pan_data:
        pan_dict[log[0]] = pan_dict.get(log[0],0)+1
    res = {'legend':[],'data':[]}
    for province,count in sorted(pan_dict.items(),key=lambda x:-x[1])[:5]:
        res['legend'].append(province)
        res['data'].append({'name':province,'value':count})
    return json.dumps(res)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=1212,debug=True)
