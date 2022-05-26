#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import uuid, time, hashlib
from sched.models import Sched_Node,Sched_Job_Config,Sched_Job_Logs
from utils.logger import logger
from django.http import QueryDict, Http404
from .assets import AssetsBase
from libs.request import http_request
from django.db.models import Q
from apps.tasks.celery_notice import apsched_notice

class ApschedBase(object):
    def __init__(self):
        super(ApschedBase, self).__init__()  
    
    def get_nodes_count(self):
        return Sched_Node.objects.all().count()   
    
    def get_jobs_count(self):
        return Sched_Job_Config.objects.all().count()  
    
    def get_jobs_status_count(self,status=0):
        return Sched_Job_Logs.objects.filter(status=status).count()
    
    def get_jobs_status_falied(self):
        return Sched_Job_Logs.objects.filter(~Q(status=0)).count()
        
class ApschedNodeManage(AssetsBase):
    
    def __init__(self):
        super(ApschedNodeManage, self).__init__()  

    def _sig(self, content_md5, date, ak, sk):
        sha1 = hashlib.sha1(sk.encode("utf-8"))
        sha1.update(content_md5)
        sha1.update("application/json".encode("utf-8"))
        sha1.update(date)
        return "OPS-2:%s:%s" % (ak, sha1.hexdigest())
    
    def schedNode(self,request):
        if request.method == 'GET':cid = request.GET.get('sched_node')
        elif request.method == 'POST':cid = request.POST.get('sched_node')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('sched_node')
        try:
            sched = Sched_Node.objects.get(sched_node=cid)
            return sched
        except Exception as ex:
            logger.warn(msg="获取计划任务节点失败: {ex}".format(ex=ex))
            raise Http404   
    
    def get_node_jobs_by_token(self,request):
        #判断header信息
        try:
            r_auth = request.META.get("HTTP_AUTHORIZATION")
            ak = r_auth.split(":")[1]       
            content_md5 = hashlib.md5(request.get_full_path().encode("utf-8")).hexdigest().encode("utf-8")
        except:
            return {"data":[],"msg":"header信息不正确","code":500} 
        
        #检查header里面的authorization信息，判断节点是否注册
        try:
            node = Sched_Node.objects.get(ak=ak)
        except Exception as ex:
            logger.warn(msg="获取计划任务节点失败: {ex}".format(ex=ex))
            return {"data":[],"msg":"节点未注册","code":404}  

        jobsList = []
        
        #通过如果AK信息正确则对比SK信息签名是否一致
        if r_auth == self._sig(content_md5, request.META.get("HTTP_DATE").encode("utf-8"),ak,node.sk):
            try:
                node.save() #签名一致就更新数据库
            except Exception as ex:
                logger.warn(msg="获取计划任务节点失败: {ex}".format(ex=ex))            
        else:    
            return {"data":[],"msg":"节点认证失败","code":403} 
            
        if node.enable == 0: return {"data":[],"msg":"节点未激活","code":500} 
        
        #如果节点激活就返回节点任务列表
        for job in node.node_jobs.all():
            if job.status == "running":
                if job.sched_type == "date":data = job.to_date_json()
                elif job.sched_type == "interval":data = job.to_interval_json()
                else:data = job.to_cron_json()
                jobsList.append(data)
                
        return {"data":jobsList,"msg":"success","code":200}             
    
    def create_node(self,request):   
        assets = self.assets(request.POST.get("sched_server"))
        if assets:  
            try:
                sched = Sched_Node.objects.create(
                                            sched_server = assets,
                                            port = request.POST.get('port'),
                                            ak = request.POST.get('ak'),
                                            sk = request.POST.get('sk'),
                                            enable = request.POST.get('enable',1),
                                        )
                return sched
            except Exception as ex:
                logger.warn(msg="添加节点失败: {ex}".format(ex=ex)) 
                return  "添加节点失败: {ex}".format(ex=ex) 
        else:          
            return "节点资产不存在"
        
    def update_node(self,request):   
        node = self.schedNode(request)
        try:
            query_params = dict()
            for ds in QueryDict(request.body).keys():
                query_params[ds] = QueryDict(request.body).get(ds)                
            return Sched_Node.objects.filter(sched_node=node.sched_node).update(**query_params)
        except Exception as ex:
            logger.warn(msg="修改节点信息失败: {ex}".format(ex=ex))
            return str(ex)   
        
    def delete_node(self,request):   
        node = self.schedNode(request)
        try:          
            node.delete()
        except Exception as ex:
            logger.warn(msg="修改节点信息失败: {ex}".format(ex=ex))
            return str(ex)   
 
        
class ApschedNodeJobsManage(ApschedNodeManage):
    def __init__(self):
        self.jobs_sched_field = ["second","minute","hour","week","day","day_of_week","month","start_date","end_date","run_date"]
        self.jobs_notice_field = ["notice_number","notice_interval"]
        super(ApschedNodeJobsManage, self).__init__()                
    
    
    def queryJobs(self,jobs):
        
        if jobs.sched_type == "cron":
            return jobs.to_cron_json()
        
        elif jobs.sched_type == "interval":
            return jobs.to_interval_json()
        
        elif jobs.sched_type == "date":
            return jobs.to_date_json()  
        
        else:
            return {}      
    
    def schedJobs(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        elif request.method == 'POST':cid = request.POST.get('id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        try:
            jobs = Sched_Job_Config.objects.get(id=cid)
            return jobs
        except Exception as ex:
            logger.warn(msg="获取计划任务失败: {ex}".format(ex=ex))
            raise Http404   
    
    def insert_jobs_logs_by_jid(self,data):
        try:
            jobs = Sched_Job_Config.objects.get(job_id=data.get("jid"))
        except Exception as ex:
            logger.warn(msg="get jobs failed: {ex}".format(ex=ex))
            return "job does not exist"
        
        try:
            data["job_id"] = jobs
            data.pop("jid")
            jobLogs = Sched_Job_Logs.objects.create(**data)
            self.judge_notice(jobs, jobLogs)
            return jobLogs.to_json()
        except Exception as ex:
            msg = "record jobs logs error {ex}".format(ex=str(ex))
            logger.warn(msg)
            return msg               
    
    def judge_notice(self,jobs, jobLogs):
        try:
            if jobs.is_alert > 0 and int(time.time()) - jobs.atime > jobs.notice_interval:
                apsched_notice.apply_async((jobs.to_alert_json(), jobLogs.to_json()), queue='default', retry=True)
                jobs.atime = int(time.time())
                jobs.save()
        except Exception as ex:
            msg = "notice jobs status failed {ex}".format(ex=str(ex))
            logger.warn(msg)            
                
    def create_jobs(self,request):   
        node = self.schedNode(request)
        if node.enable == 0: return "创建任务失败，节点已下线"
        try:
            sched_jobs = Sched_Job_Config.objects.create(
                                        job_node = node,
                                        job_id = uuid.uuid4(),
                                        job_name = request.POST.get('job_name'),
                                        second = request.POST.get('second'),
                                        minute = request.POST.get('minute'),
                                        hour = request.POST.get('hour'),
                                        week = request.POST.get('week'),
                                        day = request.POST.get('day'),
                                        day_of_week = request.POST.get('day_of_week'),
                                        month = request.POST.get('month'),
                                        job_command = request.POST.get('job_command'),
                                        start_date = request.POST.get('start_date'),
                                        end_date = request.POST.get('end_date'),
                                        run_date = request.POST.get('run_date'),
                                        sched_type = request.POST.get('sched_type'),
                                        status = request.POST.get('status',"remove"),
                                        is_alert = request.POST.get('is_alert'),
                                        notice_type =  request.POST.get('notice_type'),
                                        notice_interval =  request.POST.get('notice_interval',3600),
                                        notice_trigger = request.POST.get('notice_interval',0),
                                        notice_number = request.POST.get('notice_number'),
                                    )
            return sched_jobs
        except Exception as ex:
            logger.error(msg="添加任务失败: {ex}".format(ex=ex)) 
            return  "添加任务失败: {ex}".format(ex=ex) 

           
    def update_jobs(self,request):   
        jobs = self.schedJobs(request)

        if jobs.job_node.enable == 0: return "更新任务失败，节点已下线"       
        try:
            query_params = dict()
            if "status" in QueryDict(request.body).keys():
                for ds in QueryDict(request.body).keys():
                    query_params[ds] = QueryDict(request.body).get(ds) 
                    
            elif "is_alert" in QueryDict(request.body).keys():
                for ds in QueryDict(request.body).keys():
                    query_params[ds] = QueryDict(request.body).get(ds)                     
            else:     
                for keys in self.jobs_sched_field:
                    if keys in QueryDict(request.body).keys():
                        query_params[keys] = QueryDict(request.body).get(keys) 
                    else:
                        query_params[keys] = None
            Sched_Job_Config.objects.filter(id=jobs.id).update(**query_params)
        except Exception as ex:
            logger.error(msg="修改任务失败: {ex}".format(ex=ex)) 
            return  "修改任务失败: {ex}".format(ex=ex) 
        
        jobs = Sched_Job_Config.objects.get(id=jobs.id)
        
        if query_params.get("status") == "running": 
            return self.rpc_update_jobs(jobs,"add")
        
        elif query_params.get("status") == "remove": 
            return self.rpc_update_jobs(jobs,"remove")    
                
        if jobs.status == "running" and "is_alert" not in QueryDict(request.body).keys():
            return self.rpc_update_jobs(jobs,"edit")
   
    
    def delete_jobs(self,request):   
        jobs = self.schedJobs(request)
    
        try:
            self.rpc_update_jobs(jobs,"remove")   
            jobs.delete()
        except Exception as ex:
            logger.error(msg="删除任务失败: {ex}".format(ex=ex)) 
            return  "删除任务失败: {ex}".format(ex=ex)       
    
      
    def rpc_update_jobs(self,jobs,uri):
        data = self.queryJobs(jobs) #要修改这里               
        result = http_request._sig_auth(method="post", endpoint="{ip}:{port}".format(ip=jobs.job_node.sched_server.server_assets.ip,port=jobs.job_node.port),uri=uri, body=data,node=jobs.job_node)
        jobs.status = "stopped"
        if isinstance(result, str):
            jobs.save()                     
            return "更新节点任务失败:{result}".format(result=result)                  
        else:           
            if result.get("code") == 200:
                return jobs
            else:
                jobs.save()
                return result.get("msg")       
