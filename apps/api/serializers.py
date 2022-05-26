#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from rest_framework import serializers
from asset.models import *
from databases.models import *
from deploy.models import *
from orders.models import *
from sched.models import *
from cicd.models import *
from navbar.models import * 
from wiki.models import *
from orders.models import *
from apply.models import *
from account.models import *
from django_celery_beat.models  import CrontabSchedule,IntervalSchedule,PeriodicTask
from django_celery_results.models import TaskResult 
from rest_framework.pagination import CursorPagination

class PageConfig(CursorPagination):
    cursor_query_param  = 'offset'
    page_size = 100     #每页显示2个数据
    ordering = '-id'   #排序
    page_size_query_param = None
    max_page_size = 200

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    superior_name = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = User
        fields = ('id','last_login','is_superuser','username',
                  'first_name','last_name','email','is_staff',
                  'is_active','date_joined',"mobile","name","department",
                  'post','superior','roles','superior_name','avatar'
                  )   
        extra_kwargs = {
                        'department': {'required': False,"read_only":True},
                        'roles':{'required': False,"read_only":True},
                        }  
                        
    def get_superior_name(self,obj):
        return obj.superior_name()
              
        
class BusinessEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Env_Assets
        fields = ('id','name')
        
class BusinessTreeSerializer(serializers.ModelSerializer):
    paths = serializers.SerializerMethodField(read_only=True,required=False)
    icon = serializers.SerializerMethodField(read_only=True,required=False)
    last_node = serializers.SerializerMethodField(read_only=True,required=False)
    manage_name = serializers.SerializerMethodField(read_only=True,required=False)
    env_name = serializers.SerializerMethodField(read_only=True,required=False)
    group_paths = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = Business_Tree_Assets
        fields = ('id','text','env','env_name','manage','manage_name','parent','group','group_paths','desc','icon','paths','last_node','tree_id')          
    
    def get_env_name(self,obj):
        try:
            return Business_Env_Assets.objects.get(id=obj.env).name
        except:
            return "未知"        
    
    def get_manage_name(self,obj):
        try:
            return User.objects.get(id=obj.manage).username
        except:
            return "未知"
        
    def get_paths(self,obj):
        return obj.node_path()
    
    def get_last_node(self,obj):
        return obj.last_node()
    
    def get_icon(self,obj):
        return obj.icon()
    
    def get_group_paths(self,obj):
        return obj.group_path()
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id','name','desc')
        
class StructureSerializer(serializers.ModelSerializer):
    paths = serializers.SerializerMethodField(read_only=True,required=False)
    icon = serializers.SerializerMethodField(read_only=True,required=False)
    last_node = serializers.SerializerMethodField(read_only=True,required=False) 
    manage_name = serializers.SerializerMethodField(read_only=True,required=False)    
    class Meta:
        model = Structure
        fields = ('id','text','desc', 'type', 'parent', 'mail_group','manage','manage_name','wechat_webhook_url', 'dingding_webhook_url','icon','paths','last_node','tree_id')     
           
    def get_paths(self,obj):
        return obj.node_path()
    
    def get_last_node(self,obj):
        return obj.last_node()
    
    def get_icon(self,obj):
        return obj.icon()
    
    def get_manage_name(self,obj):
        return obj.manage_name()   

class UserTaskSerializer(serializers.ModelSerializer):
    ctime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    etime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False) 
    user = serializers.SerializerMethodField(read_only=True,required=False)
    file = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = User_Async_Task
        fields = ('id','task_id', 'task_name', 'extra_id', 'user', 'type', 'status', 'args', 'file', 'msg', 'token', 'ctk', 'ctime','etime')     
           
    def get_file(self,obj):
        return str(obj.file).split('/')[-1]
    
    def get_user(self,obj):
        try:  
            return User.objects.get(id=obj.user).name
        except Exception as ex:
            return "未知"
    
          
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags_Assets
        fields = ('id','tags_name')          

class CabinetSerializer(serializers.ModelSerializer):
    idc_name = serializers.CharField(source='idc.idc_name', read_only=True)
    class Meta:
        model = Cabinet_Assets
        fields = ('id','cabinet_name','idc_name') 
          
    def create(self,  validated_data):
        return Cabinet_Assets.objects.create(idc=self.context["idc"], **validated_data)

class IdcSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source='zone.zone_name', read_only=True)
    cabinet_assets = CabinetSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Idc_Assets
        fields = ('id','zone_name','idc_name','idc_bandwidth','idc_linkman','idc_phone','idc_address','idc_network','idc_operator','idc_desc','cabinet_assets')      

    def create(self,  validated_data):
        return Idc_Assets.objects.create(zone=self.context["zone"], **validated_data)

class IdleAssetsSerializer(serializers.ModelSerializer): 
    idc_name = serializers.CharField(source='idc.idc_name', read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    idle_username = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model =  Idle_Assets
        fields = ('id','idc_name','idle_name','idle_number','idle_user','idle_desc','update_time','idle_username')             

    def create(self,  validated_data):
        return Idle_Assets.objects.create(idc=self.context["idc"], **validated_data)        
    
    def get_idle_username(self,obj):
        return obj.get_username()
    
class ZoneSerializer(serializers.ModelSerializer):
    idc_assets = IdcSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Zone_Assets
        fields = ('id','zone_name','idc_assets')  

class LineSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    class Meta:
        model = Line_Assets
        fields = ('id','line_name','line_price','update_time')          

class RaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid_Assets
        fields = ('id','raid_name')         
       
class AssetsSerializer(serializers.ModelSerializer):
    crontab_total = serializers.SerializerMethodField(read_only=True,required=False)
    database_total = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = Assets
        fields = ('id','assets_type','name','sn','buy_time','expire_date',
                  'buy_user','management_ip','manufacturer','provider','mark',
                  'model','status','put_zone','group','project',
                  'crontab_total','cabinet','database_total',)  

    def get_crontab_total(self, obj):
        return [ cron.id for cron in obj.crontab_total.all() ]  #返回列表          
    
    def get_database_total(self,obj):
        return [ db.id for db in obj.database_total.all() ]  #返回列表          

class ServerSerializer(serializers.ModelSerializer): 
    assets = AssetsSerializer(required=False)
    class Meta:
        model = Server_Assets
        fields = ('id','ip','hostname','username','port','passwd',
                  'line','cpu','cpu_number','vcpu_number','keyfile',
                  'cpu_core','disk_total','ram_total','kernel',
                  'selinux','swap','raid','system','assets',
                  'sudo_passwd','keyfile_path') 
    def create(self, data):
        if(data.get('assets')):
            assets_data = data.pop('assets')
            assets = Assets.objects.create(**assets_data)
        else:
            assets = Assets()
        data['assets'] = assets;
        server = Server_Assets.objects.create(**data)  
        return server 


class DeployScriptSerializer(serializers.ModelSerializer): 
    detail = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model =  Deploy_Script
        fields = ('id','detail') 
        
    def get_detail(self,obj):
        return obj.to_json()  

class DeployPlaybookSerializer(serializers.ModelSerializer): 
    detail = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model =  Deploy_Playbook
        fields = ('id','detail')   
    def get_detail(self,obj):
        return obj.to_json()         
        
class DeployModelLogsSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Log_Deploy_Model
        fields = ('id','ans_user','ans_model','ans_args',
                  'ans_server','create_time') 

class DeployModelLogsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploy_CallBack_Model_Result
        fields = ('id','logId','content')
        
class DeployPlaybookLogsSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Log_Deploy_Playbook
        fields = ('id','ans_user','ans_name','ans_content','ans_id',
                  'ans_server','ans_content','create_time') 
        
class DeployPlaybookLogsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploy_CallBack_PlayBook_Result
        fields = ('id','logId','content') 
         
class NetworkSerializer(serializers.ModelSerializer): 
    assets = AssetsSerializer(required=False)
    class Meta:
        model = Network_Assets
        fields = ('id','ip','bandwidth','port_number','firmware',
                  'cpu','stone','configure_detail','assets',
                  'port','passwd','sudo_passwd','username')  
          
    def create(self, data):
        if(data.get('assets')):
            assets_data = data.pop('assets')
            assets = Assets.objects.create(**assets_data)
        else:
            assets = Assets()
        data['assets'] = assets;
        server = Network_Assets.objects.create(**data)  
        return server   
    

class OrderSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    modify_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False)  
    expire = serializers.SerializerMethodField(read_only=True,required=False)  
    user_info = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = Order_System
        fields = ('id','order_subject','order_user','order_audit_status','order_mark',
                  'order_type','order_level','create_time','modify_time','order_executor',
                  'end_time','start_time',"expire","order_execute_status","user_info")
        extra_kwargs = {
                        'order_subject': {'required': False},
                        'order_user':{'required': False},
                        'order_cancel':{'required': False},
                        'order_type':{'required': False},
                        'order_executor':{'required': False},
                        }                 
    
    def get_expire(self,obj):
        if obj.is_expired() and obj.is_unexpired():#未到期
            return 1
        
        elif obj.is_unexpired() == 0 and obj.is_expired(): #还未到期，而且还未到工单执行时间
            return 2

        elif obj.is_expired() == 0: #过期
            return 0             
 
    def get_user_info(self,obj):
        try:  
            return User.objects.get(id=obj.order_user).to_avatar()
        except Exception as ex:
            return "未知"   
        
class DataBaseServerSerializer(serializers.ModelSerializer):
    db_passwd = serializers.SerializerMethodField(read_only=True,required=False)
    detail = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = DataBase_MySQL_Server_Config
        fields = ('id','db_env','db_version','db_assets_id',
                  'db_user','db_port','db_mark','db_type',
                  "db_mode","db_business","db_rw","db_passwd",
                  "detail")  
    
    def get_db_passwd(self,obj):
        return obj.db_passwd[:1]+'****'+obj.db_passwd[-1]
    
    def get_detail(self,obj):
        return obj.to_json()

class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database_MySQL_Detail
        fields = ('id','db_name','db_size',"total_table") 
          
    def create(self,  validated_data):
        return Database_MySQL_Detail.objects.create(db_server=self.context["db_server"], **validated_data)        

class DatabaseTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database_Table_Detail_Record
        fields = ('id','table_size','table_row','table_name','table_engine','collation','format','last_time')       
             

class RedisServerSerializer(serializers.ModelSerializer):
    db_passwd = serializers.SerializerMethodField(read_only=True,required=False)
    detail = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = DataBase_Redis_Server_Config
        fields = ('id','db_env','db_version','db_assets_id',
                  'db_port','db_mark','db_type',"db_mode",
                  "db_business","db_rw","db_passwd","detail")  
    
    def get_db_passwd(self,obj):
        if len(obj.db_passwd) > 0:
            return obj.db_passwd[:1]+'****'+obj.db_passwd[-1]
        else:
            return obj.db_passwd
        
    def get_detail(self,obj):
        return obj.to_json()

class RedisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database_Redis_Detail
        fields = ('id','db_name','expires',"total_keys") 
          
    def create(self,  validated_data):
        return Database_Redis_Detail.objects.create(db_server=self.context["db_server"], **validated_data) 

        
class CustomSQLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_High_Risk_SQL
        fields = ('id','sql')
        
class HistorySQLSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    db_host = serializers.SerializerMethodField(read_only=True,required=False)
    db_name = serializers.SerializerMethodField(read_only=True,required=False)
    db_env = serializers.SerializerMethodField(read_only=True,required=False)
    class Meta:
        model = SQL_Execute_History
        fields = ('id','exe_sql','exe_user','exec_status','exe_result','db_host','db_name','create_time','db_env','exe_db',"exe_time","exe_effect_row","favorite","mark")        
    
    def get_db_env(self,obj):
        return obj.exe_db.db_server.dataMap["env"][obj.exe_db.db_server.db_env]
        
        
    def get_db_host(self,obj):
        try:
            return obj.exe_db.db_server.db_assets.server_assets.ip
        except:
            return "未知"
    
    def get_db_name(self, obj):
        try:
            return obj.exe_db.db_name   
        except:
            return "未知"        
        
class DeployInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploy_Inventory
        fields = ('id','name', 'desc','user') 
        

class DeployInventoryGroupsSerializer(serializers.ModelSerializer):
    inventory_name = serializers.CharField(source='inventory.inventory_name', read_only=True)
    inventory_id = serializers.IntegerField(source='inventory.id', read_only=True)
    class Meta:
        model = Deploy_Inventory_Groups
        fields = ('id','group_name','ext_vars','inventory_name','inventory_id')
        
class TaskCrontabSerializer(serializers.ModelSerializer):
#     timezone = timezone_field.TimeZoneField(default='Asia/Shanghai')
    class  Meta:
        model = CrontabSchedule
        fields = ('id','minute', 'hour','day_of_week','day_of_month','month_of_year') 
 
class TaskIntervalsSerializer(serializers.ModelSerializer):
    class  Meta:
        model = IntervalSchedule
        fields = ('id','every', 'period')  
               
class PeriodicTaskSerializer(serializers.ModelSerializer):
    class  Meta:
        model = PeriodicTask
        fields = ('id','name', 'task', 'kwargs','last_run_at','total_run_count',
                  'enabled','queue','crontab','interval','args','expires')  


class TaskResultSerializer(serializers.ModelSerializer):
    date_done = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class  Meta:
        model = TaskResult
        fields = ('id','task_id', 'status', 'task_name','task_kwargs','date_done',
                  'result','date_done') 
        
class CronSerializer(serializers.ModelSerializer):
    crontab_server = serializers.CharField(source='cron_server.server_assets.ip', read_only=True)
    class  Meta:
        model = Cron_Config
        fields = ('id','cron_minute', 'cron_hour','cron_day','cron_week','cron_month',
                  'cron_user','cron_name','cron_log_path','cron_type','cron_command',
                  'crontab_server','cron_status'
                  ) 
        
class ApschedNodeSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(source='sched_server.server_assets.ip', read_only=True)
    jobs_count = serializers.SerializerMethodField(read_only=True,required=False)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class  Meta:
        model = Sched_Node
        fields = ('sched_node','port', 'ak', 'sk','enable','ip','jobs_count','create_time', 'update_time')         

    def get_jobs_count(self,obj):
        return obj.node_jobs.all().count()      
    
class ApschedNodeJobsSerializer(serializers.ModelSerializer):
    node_detail = serializers.SerializerMethodField(read_only=True,required=False)
    jobs_detail = serializers.SerializerMethodField(read_only=True,required=False)
    alert_detail = serializers.SerializerMethodField(read_only=True,required=False)
    runs = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Sched_Job_Config
        fields = ("id","job_name","jobs_detail","node_detail","alert_detail","runs")         
    
    def get_node_detail(self,obj):
        return obj.job_node.to_json()
    
    def get_jobs_detail(self, obj):
        if obj.sched_type == "date":data = obj.to_date_json()
        elif obj.sched_type == "interval":data = obj.to_interval_json()
        else:data = obj.to_cron_json()
        return data   

    def get_runs(self,obj):
        return obj.node_jobs_log.all().count()

    def get_alert_detail(self, obj):
        return obj.to_alert_json()    
                     
                     
class ApschedNodeJobsLogsSerializer(serializers.ModelSerializer):
    runtime = serializers.SerializerMethodField(read_only=True,required=False)
    jobname = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Sched_Job_Logs
        fields = ("id","status","stime","etime","cmd","result","runtime","jobname") 
    
    def get_jobname(self,obj):
        return obj.job_id.job_name 
          
    def get_runtime(self,obj):
        try:
            return obj.etime - obj.stime
        except:
            return 0                            
         
        
class AppsSerializer(serializers.ModelSerializer):
    project_business_paths = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Project_Config
        fields = ('id','project_env','project_business_paths', 'project_name','project_type','project_local_command','project_repo_dir',
                  'project_exclude','project_address','project_uuid','project_repo_user','project_repo_passwd',
                  'project_repertory','project_status','project_remote_command','project_user','project_model',
                  'project_business',"project_pre_remote_command") 
    
    def get_project_business_paths(self,obj):
        return obj.business_paths()

class AppsRolesSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Project_Roles    
        fields = ('id','project', 'user','role') 
           
class AppsLogsSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    project_env = serializers.CharField(source='project.project_env', read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    package = serializers.SerializerMethodField(read_only=True,required=False)
    git_version = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = Log_Project_Config
        fields = ('id', 'project_name','username','package','status','project_env','create_time','type','task_id','git_version') 
        
    def get_package(self,obj):
        try:
            return obj.package.split("/")[-1]
        except:
            return "未知"  
          
    def get_git_version(self,obj):
        try:
            if obj.project.project_model == "branch":
                return "分支: " + obj.branch + ' 版本: ' + obj.commit_id[0:10]
            else:
                return "标签: " + obj.tag
        except:
            return "未知"              
        
class AppsLogsRecordSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class  Meta:
        model = Log_Project_Record
        fields = ('id', 'key','msg','title','status','task_id','create_time')        
         

        
class NavTypeNumberSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='nav_type.type_name', read_only=True)
    nav_type_id = serializers.IntegerField(source='nav_type.id', read_only=True)
    class Meta:
        model = Nav_Type_Number
        fields = ('id','nav_name','nav_desc','type_name','nav_type_id','nav_url','nav_img')
           


class NavTypeSerializer(serializers.ModelSerializer):
    nav_type_number = NavTypeNumberSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Nav_Type
        fields = ('id','type_name','nav_type_number')

class NavThirdNumberSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='nav_third.type_name', read_only=True)
    nav_third_id = serializers.IntegerField(source='nav_third.id', read_only=True)
    class Meta:
        model = Nav_Third_Number
        fields = ('id','nav_name',"type_name",'url','nav_third_id','height','width')
           


class NavThirdSerializer(serializers.ModelSerializer):
    nav_third_number = NavThirdNumberSerializer(many=True, read_only=True,required=False)
    class Meta:
        model = Nav_Third
        fields = ('id','type_name','icon','nav_third_number')
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')    
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','content','category','author')   
        
class OrdersNoticeConfigSerializer(serializers.ModelSerializer):                        
    class Meta:
        model = Order_Notice_Config
        fields = ('id','order_type','mode')     
           
class IPVSSerializer(serializers.ModelSerializer):
    sip = serializers.CharField(source='ipvs_assets.server_assets.ip', read_only=True)
    rs_count = serializers.SerializerMethodField(read_only=True,required=False)
#     rs_list = serializers.SerializerMethodField(read_only=True,required=False)
    business_paths = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = IPVS_CONFIG
        fields = ('id','vip','port','scheduler','sip','rs_count','persistence','business','business_paths','protocol','line','desc','is_active','ipvs_assets')         
    
        extra_kwargs = {
                        'ipvs_assets': {'required': False},
                        'vip':{'required': False},
                        'port':{'required': False},
                        'scheduler':{'required': False},                   
                        }       
    

    
    def get_rs_count(self,obj):
        return obj.ipvs_rs.all().count()  
    
    def get_rs_list(self,obj):
        return [ x.to_json() for x in obj.ipvs_rs.all() ]     
    
    def get_business_paths(self,obj):
        return obj.business_paths()
    
class IPVSRealServerSerializer(serializers.ModelSerializer):
    sip = serializers.CharField(source='rs_assets.server_assets.ip', read_only=True)
    vip_detail = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = IPVS_RS_CONFIG
        fields = ('id','ipvs_fw_ip','forword','weight','sip','ipvs_vip','rs_assets','is_active','vip_detail')         
        extra_kwargs = {
                        'rs_assets': {'required': False},
                        'ipvs_fw_ip':{'required': False},
                        'ipvs_vip':{'required': False},
                        'forword':{'required': False},
                        }       
    
    def get_vip_detail(self,obj):
        return obj.ipvs_vip.to_json() 

class IPVSNanmeServerSerializer(serializers.ModelSerializer):
    vip = serializers.CharField(source='ipvs_vip.vip', read_only=True)
    class  Meta:
        model = IPVS_NS_CONFIG
        fields = ('id','nameserver','desc','ipvs_vip','vip')         
        extra_kwargs = {
                        'ipvs_vip':{'required': False},
                        }       
        
class ApplyCenterConfigSerializer(serializers.ModelSerializer):
    class  Meta:
        model = APPLY_CENTER_CONFIG
        fields = ('id','apply_name','apply_desc','apply_type','apply_payload','apply_icon','apply_playbook')       
        
        
class ApplyTasksSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user_info = serializers.SerializerMethodField(read_only=True,required=False)
    apply_detail = serializers.SerializerMethodField(read_only=True,required=False)
    class  Meta:
        model = ApplyTasksModel
        fields = ('id','user_info','apply_id','apply_detail','task_id','task_per','status','deploy_type','payload','create_time','update_time','error_msg')
        
    def get_user_info(self,obj):
        try:  
            return User.objects.get(id=obj.user).to_avatar()
        except Exception as ex:
            return "未知"  
        
    def get_apply_detail(self,obj): 
        try:
            return APPLY_CENTER_CONFIG.objects.get(id=obj.apply_id).to_json()
        except:
            return {}  
 
#     def create(self,  validated_data):
#         return ApplyTasksModel.objects.create(
#                                     user=validated_data.get('apply_name'),
#                                     apply_id=validated_data.get('apply_id'),
#                                     task_id=validated_data.get('task_id'),
#                                     task_per=0,
#                                     status='ready',
#                                     deploy_type='playbook',
#                                     payload=validated_data.get('payload')
#                                     )                    