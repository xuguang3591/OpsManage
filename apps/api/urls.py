from django.conf.urls import url
from api.views import (assets_api,deploy_api,mysql_api,
                       orders_api,cron_api,celery_api,
                       cicd_api,monitor_api,nav_api,
                       wiki_api,apscehd_api,ipvs_api,
                       account_api, redis_api, apply_api)
urlpatterns = [
  
            #用户管理模块API
            url(r'^account/user/$', account_api.user_list), 
            url(r'^account/user/(?P<id>[0-9]+)/$',account_api.user_detail), 
            url(r'^account/user/superior/$',account_api.UserSuperior.as_view()),    
            url(r'^account/user/task/$',account_api.UserTask.as_view()),    
            url(r'^account/user/task/(?P<pk>[0-9]+)/$',account_api.UserTaskDetail.as_view()), 
            url(r'^account/user/task/(?P<pk>[0-9]+)/download/$',account_api.UserTaskDownload.as_view()), 
            url(r'^account/group/$',account_api.GROUP_LIST.as_view()),       
            url(r'^account/role/$', account_api.role_list), 
            url(r'^account/role/(?P<id>[0-9]+)/$',account_api.role_detail), 
            url(r'^account/structure/$',account_api.STRUCTURE_TREE_LIST.as_view()), 
            url(r'^account/structure/nodes/$',account_api.STRUCTURE_LIST.as_view()), 
            url(r'^account/structure/nodes/(?P<pk>[0-9]+)/$',account_api.STRUCTURE_NODE_DETAIL.as_view()), 
            url(r'^account/structure/nodes/member/(?P<pk>[0-9]+)/$', account_api.NODES_MEMBER_DETAIL.as_view()), 
            
            #资产管理模块API
            url(r'^assets/$', assets_api.AssetList.as_view()),   
            url(r'^assets/(?P<id>[0-9]+)/$', assets_api.asset_detail),
            url(r'^assets/info/(?P<id>[0-9]+)/$', assets_api.asset_info),     
            url(r'^assets/count/$', assets_api.asset_count),     
            url(r'^assets/tags/(?P<id>[0-9]+)/$',assets_api.assets_tags),             
            url(r'^business/last/$', assets_api.business_list),            
            url(r'^business/env/$', assets_api.env_list), 
            url(r'^business/env/(?P<id>[0-9]+)/$',assets_api.env_detail),      
            url(r'^business/tree/$', assets_api.BUSINESS_TREE_LIST.as_view()), 
            url(r'^business/nodes/$',assets_api.NODE_LIST.as_view()), 
            url(r'^business/nodes/(?P<pk>[0-9]+)/$',assets_api.NODE_DETAIL.as_view()), 
            url(r'^business/nodes/assets/(?P<pk>[0-9]+)/$', assets_api.NODES_ASSERS_DETAIL.as_view()),                                           
            url(r'^tags/$', assets_api.tags_list), 
            url(r'^tags/(?P<id>[0-9]+)/$',assets_api.tags_detail),    
            url(r'^tags/assets/(?P<id>[0-9]+)/$',assets_api.tags_assets),                                         
            url(r'^idc/$', assets_api.idc_list), 
            url(r'^idc/(?P<id>[0-9]+)/$',assets_api.idc_detail),    
            url(r'^idc/idle/$', assets_api.idle_list), 
            url(r'^idc/idle/(?P<id>[0-9]+)/$',assets_api.idle_detail),                      
            url(r'^zone/$', assets_api.zone_list), 
            url(r'^zone/(?P<id>[0-9]+)/$',assets_api.zone_detail),   
            url(r'^raid/$', assets_api.raid_list), 
            url(r'^raid/(?P<id>[0-9]+)/$',assets_api.raid_detail),     
            url(r'^cabinet/$', assets_api.cabinet_list), 
            url(r'^cabinet/(?P<id>[0-9]+)/$',assets_api.cabinet_detail),   
            url(r'^line/$', assets_api.line_list), 
            url(r'^line/(?P<id>[0-9]+)/$',assets_api.line_detail),                         
            url(r'^server/$', assets_api.asset_server_list), 
            url(r'^server/(?P<id>[0-9]+)/$', assets_api.asset_server_detail), 
            url(r'^net/$', assets_api.asset_net_list), 
            url(r'^net/(?P<id>[0-9]+)/$', assets_api.asset_net_detail), 
                      
            #部署模块API
            url(r'^deploy/scripts/$', deploy_api.DeployScriptList.as_view()),   
            url(r'^deploy/playbook/$', deploy_api.DeployPlayBookList.as_view()),   
            url(r'^inventory/$', deploy_api.inventory_list),
            url(r'^inventory/(?P<id>[0-9]+)/$', deploy_api.inventory_detail),
            url(r'^inventory/groups/(?P<id>[0-9]+)/$', deploy_api.deploy_inventory_groups),
            url(r'^inventory/groups/query/(?P<id>[0-9]+)/$', deploy_api.deploy_inventory_groups_query),
            url(r'^host/vars/(?P<id>[0-9]+)/$', deploy_api.deploy_host_vars),
            url(r'^logs/ansible/model/$', deploy_api.DeployModelLogPaginator.as_view()),
            url(r'^logs/ansible/model/(?P<id>[0-9]+)/$', deploy_api.modelLogsdetail),
            url(r'^logs/ansible/playbook/$', deploy_api.DeployPlaybookLogPaginator.as_view()),            
            url(r'^logs/ansible/playbook/(?P<id>[0-9]+)/$', deploy_api.playbookLogsdetail), 
            
            #任务调度模块API
            url(r'^sched/cron/$', cron_api.cron_list),
            url(r'^sched/cron/(?P<id>[0-9]+)/$', cron_api.cron_detail),
            url(r'^sched/apsched/node/$', apscehd_api.node_list),
            url(r'^sched/apsched/count/$', apscehd_api.ApschedCount.as_view()), 
            url(r'^sched/apsched/jobs/$', apscehd_api.ApschedNodeJobs.as_view()),  
            url(r'^sched/apsched/logs/$', apscehd_api.ApschedNodeJobsLogs.as_view()), 
            url(r'^v1/sched/apsched/jobs/$', apscehd_api.ApschedNodeJobsQuery.as_view()), 
            url(r'^v1/sched/apsched/logs/$', apscehd_api.ApschedNodeJobsRecord.as_view()),
            url(r'^sched/intervals/$', celery_api.celery_intervals_list),
            url(r'^sched/intervals/(?P<id>[0-9]+)/$', celery_api.celery_intervals_detail),
            url(r'^sched/crontab/$', celery_api.celery_crontab_list),
            url(r'^sched/crontab/(?P<id>[0-9]+)/$', celery_api.celery_crontab_detail),    
            url(r'^sched/celery/$', celery_api.celery_task_list),
            url(r'^sched/celery/(?P<id>[0-9]+)/$', celery_api.celery_task_detail),    
            url(r'^sched/celery/result/$', celery_api.CeleryTaskResultList.as_view()),  
            url(r'^sched/celery/result/(?P<id>[0-9]+)/$', celery_api.celery_task_result_detail),                
                       
            #MySQL管理模块API接口
            url(r'db/mysql/list/$', mysql_api.DB_SERVER_LIST.as_view()),
            url(r'db/mysql/custom/sql/$', mysql_api.DB_CUSTOM_SQL.as_view()),
            url(r'db/mysql/tree/$', mysql_api.db_tree),
            url(r'db/mysql/config/(?P<id>[0-9]+)/$', mysql_api.db_detail),
            url(r'db/mysql/status/(?P<id>[0-9]+)/$', mysql_api.db_status),
            url(r'db/mysql/org/(?P<id>[0-9]+)/$', mysql_api.db_org),
            url(r'db/mysql/server/(?P<pk>[0-9]+)/list/$', mysql_api.DB_SERVER_DETAIL.as_view()),
            url(r'db/mysql/server/(?P<pk>[0-9]+)/tables/$', mysql_api.DB_SERVER_TABLES.as_view()),
            url(r'db/mysql/server/(?P<sid>[0-9]+)/db/(?P<id>[0-9]+)/$', mysql_api.db_server_db_detail),
            url(r'db/mysql/server/(?P<sid>[0-9]+)/db/(?P<did>[0-9]+)/dict/$', mysql_api.DB_DATA_DICT.as_view()),
            url(r'db/mysql/user/list/$', mysql_api.DB_USER_DB_LIST.as_view()),
            url(r'db/mysql/user/(?P<uid>[0-9]+)/$', mysql_api.DB_USER_DB.as_view()),
            url(r'db/mysql/user/(?P<uid>[0-9]+)/server/(?P<sid>[0-9]+)/db/$', mysql_api.DB_USER_SERVER_DBLIST.as_view()),
            url(r'db/mysql/user/(?P<uid>[0-9]+)/db/(?P<did>[0-9]+)/table/$', mysql_api.db_user_db_table_list),
            url(r'db/mysql/user/(?P<uid>[0-9]+)/db/(?P<did>[0-9]+)/sql/$', mysql_api.DB_USER_SERVER_DBSQL.as_view()),
            url(r'^logs/sql/$', mysql_api.DatabaseExecuteHistory.as_view()),   
            url(r'^logs/sql/(?P<id>[0-9]+)/$', mysql_api.DatabaseExecuteHistoryDetail.as_view()),             
            
            #Redis管理模块API接口
            url(r'db/redis/list/$', redis_api.REDIS_SERVER_LIST.as_view()),
            url(r'db/redis/custom/sql/$', redis_api.REDIS_SERVER_LIST.as_view()),
            url(r'db/redis/tree/$', redis_api.db_tree),
            url(r'db/redis/org/(?P<id>[0-9]+)/$', redis_api.db_org),
            url(r'db/redis/config/(?P<id>[0-9]+)/$', redis_api.db_detail),
            url(r'db/redis/status/(?P<id>[0-9]+)/$', redis_api.db_status),
            url(r'db/redis/server/(?P<pk>[0-9]+)/list/$', redis_api.REDIS_SERVER_DETAIL.as_view()),
            url(r'db/redis/server/(?P<sid>[0-9]+)/db/(?P<id>[0-9]+)/$', redis_api.db_server_db_detail),
            url(r'db/redis/user/list/$', redis_api.REDIS_USER_REDIS_LIST.as_view()),
            url(r'db/redis/user/(?P<uid>[0-9]+)/$', redis_api.REDIS_USER_DB.as_view()),
            url(r'db/redis/user/(?P<uid>[0-9]+)/server/(?P<sid>[0-9]+)/db/$', redis_api.REDIS_USER_SERVER_DBLIST.as_view()),
            url(r'db/redis/user/(?P<uid>[0-9]+)/db/(?P<did>[0-9]+)/cmds/$', redis_api.REDIS_USER_SERVER_DBCMDS.as_view()),
                                    
            #工单管理模块API
            url(r'^orders/list/$', orders_api.OrdersPaginator.as_view()),
            url(r'^orders/(?P<pk>[0-9]+)/$', orders_api.OrderDetail.as_view()),
            url(r'^orders/logs/(?P<pk>[0-9]+)/$', orders_api.OrderLogsDetail.as_view()),
            url(r'^orders/count/$', orders_api.order_count),
            url(r'^orders/notice/$', orders_api.notice_config),
            url(r'^orders/notice/(?P<id>[0-9]+)/$', orders_api.notice_config_detail),
            
            #代码部署模块
            url(r'^apps/list/$', cicd_api.project_list),   
            url(r'^apps/list/(?P<id>[0-9]+)/$', cicd_api.project_detail), 
            url(r'^apps/logs/$', cicd_api.AppsLogPaginator.as_view()),  
            url(r'^apps/log/(?P<id>.+)/$', cicd_api.project_log_detail), 
            url(r'^apps/logs/detail/(?P<id>.+)/$', cicd_api.AppsLogRecord.as_view()),  
            url(r'^apps/count/$', cicd_api.AppsCounts.as_view()), 
            url(r'^apps/roles/$', cicd_api.apps_roles_list),    
            url(r'^apps/roles/(?P<id>[0-9]+)/$', cicd_api.apps_roles_detail),                                  
            url(r'^monitor/assets/(?P<id>.+)/$', monitor_api.AssetsMonitor.as_view()),  
            url(r'^monitor/apps/(?P<id>.+)/$', monitor_api.AppsMonitor.as_view()), 
            
            #站内导航模块API
            url(r'^nav/type/$', nav_api.navtype_list), 
            url(r'^nav/type/(?P<id>[0-9]+)/$', nav_api.navtype_detail),     
            url(r'^nav/number/$', nav_api.navnumber_list), 
            url(r'^nav/number/(?P<id>[0-9]+)/$', nav_api.navnumber_detail),               
            url(r'^nav/third/$', nav_api.navthird_list), 
            url(r'^nav/third/(?P<id>[0-9]+)/$', nav_api.navthird_detail),     
            url(r'^nav/third/number/$', nav_api.navthird_number_list), 
            url(r'^nav/third/number/(?P<id>[0-9]+)/$', nav_api.navthird_number_detail),
            
            #站内WIKI API             
            url(r'^wiki/tag/$', wiki_api.tag_list),
            url(r'^wiki/tag/(?P<id>[0-9]+)/$', wiki_api.tag_detail),
            url(r'^wiki/category/$', wiki_api.category_list),
            url(r'^wiki/category/(?P<id>[0-9]+)/$', wiki_api.category_detail),   
            url(r'^wiki/archive/(?P<id>[0-9]+)/$', wiki_api.archive_detail), 
            
            #应用管理API      
            url(r'^apply/ipvs/$', ipvs_api.IPVSLIST.as_view()),  
            url(r'^apply/ipvs/(?P<pk>[0-9]+)/$', ipvs_api.IPVSLIST_DETAIL.as_view()), 
            url(r'^apply/ipvs/rs/$', ipvs_api.IPVS_RS_LIST.as_view()),     
            url(r'^apply/ipvs/rs/(?P<pk>[0-9]+)/$', ipvs_api.IPVS_RS_LIST_DETAIL.as_view()),   
            url(r'^apply/ipvs/tree/$', ipvs_api.ipvs_tree),  
            url(r'^apply/ipvs/tree/business/(?P<id>[0-9]+)/$', ipvs_api.ipvs_tree_business),
            url(r'^apply/ipvs/rs/assets/$', ipvs_api.ipvs_assets),                 
            url(r'^apply/ipvs/ns/$', ipvs_api.IPVS_NS_LIST.as_view()),     
            url(r'^apply/ipvs/ns/(?P<pk>[0-9]+)/$', ipvs_api.IPVS_NS_LIST_DETAIL.as_view()),   
            url(r'^apply/config/$', apply_api.ApplyCenterConfig.as_view()),    
            url(r'^apply/config/(?P<pk>[0-9]+)/$', apply_api.ApplyConfigDetail.as_view()),       
            url(r'^apply/tasks/$', apply_api.ApplyTasks.as_view()),    
            url(r'^apply/task/(?P<pk>[0-9]+)/$', apply_api.ApplyTasksDetail.as_view()),    
            url(r'^apply/task/detail/(?P<pk>[0-9]+)/$', apply_api.ApplyTasksLogDetail.as_view()),          
            url(r'^apply/sync/tag/(?P<pk>[0-9]+)/$', apply_api.ApplyTasksSyncTagsDetail.as_view()),     
            url(r'^apply/tasks/count/$', apply_api.ApplyTasksCount.as_view()),                                                   
                                                                          
    ]    