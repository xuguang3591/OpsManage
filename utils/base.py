#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
'''版本控制方法'''
import magic
from random import choice
import string, hashlib, calendar
import subprocess,os,time,smtplib
from datetime import datetime,timedelta,date
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart
from django.core.serializers.json import DjangoJSONEncoder
from .logger import logger
from functools import wraps
import ply.lex as lex, re

def method_decorator_adaptor(adapt_to, *decorator_args, **decorator_kwargs):
    def decorator_outer(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            @adapt_to(*decorator_args, **decorator_kwargs)
            def adaptor(*args, **kwargs):
                return func(self, *args, **kwargs)
            return adaptor(*args, **kwargs)
        return decorator
    return decorator_outer


def file_iterator(file_name, chunk_size=512):
    f = open(file_name, "rb")
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break 
    f.close()

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)  
    d, m = divmod(h, 24) 
    if d > 1:
        return "%02d 天" % d
    return "%02d:%02d:%02d" % (h, m, s)
  
def radString(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def exec_command(cmd, timeout=None):
    '''执行shell命令函数'''
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        stdout, stderr = result.communicate(timeout=timeout)
    except Exception as ex:
        result.kill()
        return (256, str(ex).replace(cmd,""))
    code = result.returncode
    if code != 0 and stderr:
        return code, stderr.decode('utf-8')
    return code, stdout.decode('utf-8')

def rsync(sourceDir,destDir,exclude=None):
    if exclude:cmd = "rsync -au --delete {exclude} {sourceDir} {destDir}".format(sourceDir=sourceDir,destDir=destDir,exclude=exclude)
    else:cmd = "rsync -au --delete {sourceDir} {destDir}".format(sourceDir=sourceDir,destDir=destDir)
    return exec_command(cmd)
    
def mkdir(dirPath):
    mkDir = "mkdir -p {dirPath}".format(dirPath=dirPath)
    return exec_command(mkDir)    
    
    
def cd(localDir):
    os.chdir(localDir)
    
def pwd():
    return os.getcwd()   

def cmds(cmds):
    status,result = subprocess.getstatusoutput(cmds)
    if status > 0:
        return {"status":"failed","msg":result}
    return {"status":"succeed","msg":result}

def chown(user,path):
    cmd = "chown -R {user}:{user} {path}".format(user=user,path=path)
    return exec_command(cmd)

def makeToken(strs):
    m = hashlib.md5()   
    m.update(strs)
    return m.hexdigest()  

def lns(spath,dpath):
    if spath and dpath:
        mkLn = "ln -s {spath} {dpath}".format(spath=spath,dpath=dpath)
        return exec_command(mkLn)
    else:
        return (1,"缺少路径")    

def getDaysAgo(num,fmt="%Y%m%d"):
    threeDayAgo = (datetime.now() - timedelta(days = num))
    timeStamp = int(time.mktime(threeDayAgo .timetuple()))
    otherStyleTime = threeDayAgo .strftime(fmt)
    return otherStyleTime

def changeTotimestamp(dt,fmt='%Y-%m-%d %H:%M:%S'):
    time.strptime(dt, fmt)
    s = time.mktime(time.strptime(dt, fmt))
    return int(s)

def changeTimestampTodatetime(value,format='%Y-%m-%d %H:%M:%S'):
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def getSQLAdvisor(host,port,user,passwd,dbname,sql):
    cmd = """/usr/bin/sqladvisor -h {host}  -P {port}  -u {user} -p '{passwd}' -d {dbname} -q '{sql}' -v 1""".format(host=host,port=port,user=user,passwd=passwd,dbname=dbname,sql=sql)
    return exec_command(cmd)

def getDayAfter(num,format=None):
    #获取今天多少天以后的日期
    if format:
        return time.strftime(format ,time.localtime(time.time()+(num*86400)))
    else:
        return time.strftime('%Y-%m-%d' ,time.localtime(time.time()+(num*86400)))
    
def calcDays(startDate,endDate):
    #对比两个日期的时间差
    startDate=time.strptime(startDate,"%Y-%m-%d %H:%M:%S")
    endDate=time.strptime(endDate,"%Y-%m-%d %H:%M:%S")
    startDate=datetime(startDate[0],startDate[1],startDate[2],startDate[3],startDate[4],startDate[5])
    endDate=datetime(endDate[0],endDate[1],endDate[2],endDate[3],endDate[4],endDate[5])
    return (endDate-startDate).days
    
def getMonthFirstDayAndLastDay(year=None, month=None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year
    if month:
        month = int(month)
    else:
        month = datetime.date.today().month
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    firstDay = date(year=year, month=month, day=1)
    lastDay = date(year=year, month=month, day=monthRange)
    return firstDay, lastDay

def getFileType(filePath):
    try:
        files = magic.Magic(uncompress=True,mime=True)
        file_type = files.from_file(filePath)
    except Exception as ex:
        file_type = '未知'
        logger.error("获取文件类型失败: {ex}".format(ex=ex))
    return file_type

def get_file_md5sum(file):
    m = hashlib.md5()
    with open(file,'rb') as f:
        for line in f:
            m.update(line)
    return m.hexdigest()
   
def get_date_list(begin_date, end_date,fmt="%Y-%m-%d %H:%M"):
    dates = []
    try:
        dt = datetime.strptime(begin_date, fmt)
        date = begin_date[:]
        while date <= end_date:
            dates.append(date)
            dt += timedelta(seconds=300) #五分钟
            date = dt.strftime(fmt)
    except Exception as ex:
        logger.error("获取时间列表失败: {ex}".format(ex=ex))
    return dates   

def mysql_bakcup_tables(db, table, path, task_id , where_claus=None, timeout=None):
    if where_claus is None:
        where_claus = ''
    else:
        where_claus = '--where="{where}"'.format(where=where_claus)
    
    if not os.path.exists(path):
        os.makedirs(path)    
        
    cmd = '''/usr/bin/mysqldump --host={host} --port={port} --user={user} --password={pwd} {database} {table} {where} |gzip > {path}{task_id}.sql.gz'''.format(host=db.get('ip'), port=db.get('db_port'),
                                                                                  user=db.get('db_user'), pwd=db.get('db_passwd'),
                                                                                  database=db.get("db_name"), table=table, 
                                                                                  where=where_claus, path=path, task_id=task_id)
    return exec_command(cmd,timeout)    