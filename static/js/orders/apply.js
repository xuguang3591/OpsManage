var sql_type = 'online';

function AssetsTypeSelect(obj,model){ 
	   var index = obj.selectedIndex;
	   var sId = obj.options[index].value; 
	   if ( sId  > 0){	 
			$.ajax({
				dataType: "JSON",
				url:'/assets/server/query/', //请求地址
				type:"POST",  //提交类似
				data:{
					"query":model,
					"id":sId
				},
				success:function(response){
					var sHtml = '';
					for (var i=0; i <response["data"].length; i++){
						sHtml += '<br>' + response["data"][i]["ip"] + " | " + response["data"][i]["project"] + " | " + response["data"][i]["service"]
					};  
					if ( sHtml.length > 0){
		            	new PNotify({
		                    title: "<strong>发现主机:</strong>",
		                    text: sHtml,
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 	
		            	$("#fileuploadbtn").attr("disabled", false)
					}
					else {
		            	new PNotify({
		                    title: "<strong>Ops：</strong>",
		                    text: "该条件下未发现主机资源~",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                }); 	
		            	$("#fileuploadbtn").attr("disabled", true)
					}
				
						
				},
			});	
	   }
}

function AssetsSelect(name,dataList,selectIds){
	if(!selectIds){selectIds=0}
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:oBtProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="">选择一个进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		if(dataList[i][name+"_name"]){
			var text = dataList[i][name+"_name"]
		}else if(name=="custom"){
			var text = dataList[i]["detail"]["ip"]
		}
		else{
			var text = dataList[i]["name"]
		}
		if(selectIds==dataList[i]["id"]){
			selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>' 	
		}else{
			selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
		} 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("select[name='"+name+"']").html(binlogHtml)
	$("select[name='"+name+"']").selectpicker('refresh');		
}

function requests(method,url,data){
	var ret = '';
	$.ajax({
		async:false,
		url:url, //请求地址
		type:method,  //提交类似
       	success:function(response){
             ret = response;
        },
        error:function(data){
            ret = {};
        }
	});	
	return 	ret
}



function makeUserSelect(ids,dataList){
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="'+ ids +'" id="'+ids+'"  autocomplete="off"><option selected="selected" value="">选择一个用户</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i]["username"] +'</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	document.getElementById(ids).innerHTML= binlogHtml;							
	$('#'+ids).selectpicker('refresh');		
}

function makeDatabaseSelect(ids,response){	
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="db" id="db"  data-size="10" data-selected-text-format="count > 3"  data-width="100%"  id="db"  autocomplete="off"><option  name="db" value="">请选择一个数据库</option>'
	var selectHtml = '';
	for (var i=0; i <response.length; i++){
		selectHtml += '<option name="db" value="'+ response[i]["id"] +'">' + response[i]["detail"]["db_env"] + ' | ' + response[i]["detail"]["ip"] +  ' | ' + response[i]["detail"]["db_name"] +  ' | ' + response[i]["detail"]["db_mark"] + '</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	document.getElementById(ids).innerHTML= binlogHtml;							
	$('#'+ids).selectpicker('refresh');			
}

function setAceEditMode(model) {
	var editor = ace.edit("compile-editor-add");
	require("ace/ext/old_ie");
	var langTools = ace.require("ace/ext/language_tools");
	editor.setTheme("ace/theme/monokai");
	editor.getSession().setMode("ace/mode/" + model);
	editor.setShowPrintMargin(false);
	editor.setOptions({
	    enableBasicAutocompletion: true,
	    enableSnippets: true,
	    enableLiveAutocompletion: true
	}); 
			 
};	

$(document).ready(function() {
	
	$("input[name='order_time']").daterangepicker({
        timePicker: !0,
        timePickerIncrement: 30,
        locale: {
            format: "YYYY-MM-DD HH:mm:ss"
        }
    })	
	
	$("button[name='sql_model_chioce']button[value='"+sql_type+"']").attr('disabled',true);
	
	if($("select[name='custom']").length){
		AssetsSelect("custom",requests('get','/api/assets/'))
	}

	setAceEditMode("mysql");
	
	
    $("button[name='sql_model_chioce']").on('click', function() {
    	var value = $(this).val();
		if (value=='online'){
			document.getElementById("onlineSql").style.display = "";
			document.getElementById("uploadSQL").style.display = "none"; 			
			sql_type = 'online';
		}
		else if (value=='file'){
			document.getElementById("onlineSql").style.display = "none";
			document.getElementById("uploadSQL").style.display = ""; 	
			sql_type = 'file';
		}
		else{
			document.getElementById("onlineSql").style.display = "";
			document.getElementById("uploadSQL").style.display = "none"; 
			sql_type = 'human';			
		}
    	$("button[name='sql_model_chioce']button[value='"+value+"']").attr('disabled',true);
    	$("button[name='sql_model_chioce']button[value!='"+value+"']").attr('disabled',false);
    });		
    
    
	$("#order_file").fileinput({
		language : 'zh',
 		showUpload : false, 
 	    uploadUrl: '#', // you must set a valid URL here else you will get an error 
   	    allowedFileExtensions : [".sql",".txt"], 
   	 	previewFileType:"pdf",
  	  	allowedFileTypes: ["text"],
	    overwriteInitial: false,
	    maxFileSize: 2000,
	    maxFilesNum: 10,
/* 	    dropZoneTitle:"暂不支持拖拽文件上传...", */
	    dropZoneEnabled: false,
	    slugCallback: function(filename) {
	        return filename.replace('(', '_').replace(']', '_');
	    }
	});    
    	    

	$(function() {
		if($('#order_db').length){		
			let response = requests('get','/api/db/mysql/user/list/')
			var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true" name="order_db" id="order_db"  data-size="10" data-selected-text-format="count > 10"  data-width="100%"  autocomplete="off"><option  name="order_db" value="">请选择一个数据库</option>'
			var selectHtml = '';
			for (var i=0; i <response.length; i++){
				selectHtml += '<option name="order_db" value="'+ response[i]["id"] +'">' + response[i]["db_env"] + ' | ' + response[i]["db_mark"] + ' | ' + response[i]["ip"] +  ' | ' + response[i]["db_name"] + '</option>' 					 
			};                        
			binlogHtml =  binlogHtml + selectHtml + '</select>';
			document.getElementById("order_db").innerHTML= binlogHtml;							
			$('#order_db').selectpicker('refresh');	
		}
	})		
	
	var aduitUserList = requests("get","/api/account/user/superior/")
	
	$(function() {
		if($('#order_executor').length){		
			try {
				makeUserSelect("order_executor",aduitUserList)
			}
			catch(err) {
				console.log("请先配置授权组")
			}
		}
	})	
	
	$(function() {
		if($('#fileupload_order_executor').length){		
			try {
				makeUserSelect("fileupload_order_executor",aduitUserList)
			}
			catch(err) {
				console.log("请先配置授权组")
			}
		}
	})		
	
	$(function() {
		if($('#filedownload_order_executor').length){		
			try {
				makeUserSelect("filedownload_order_executor",aduitUserList)
			}
			catch(err) {
				console.log("请先配置授权组")
			}
		}
	})		
	
	$(function() {
		if($('#service_order_executor').length){		
			try {
				makeUserSelect("service_order_executor",aduitUserList)
			}
			catch(err) {
				console.log("请先配置授权组")
			}
		}
	})	
	
    $("button[name='audit_sql_btn']").on('click', function() {
    	var btnObj = $(this)
    	btnObj.attr('disabled',true);
		var required = ["order_db","order_executor","order_desc","order_time"];
		var form = document.getElementById('audit_sql_order');
		for (var i = 0; i < form.length; ++i) {
			var name = form[i].name;
			var value = form[i].value;	
			idx = $.inArray(name, required);						
			if (idx >= 0 && value.length == 0){
				$("[name='"+ name +"']").parent().addClass("has-error");
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 	
            	btnObj.attr('disabled',false);
				return false;
			}else if (value.length > 0){
				$("[name='"+ name +"']").parent().removeClass("has-error");
			}	
			if (name=="order_time"){
				var start_time = value.split(" - ")[0]
				var end_time = value.split(" - ")[1]
			}				
		};				
		var editor = ace.edit("compile-editor-add");
	    var order_sql = editor.getSession().getValue(); 
	    if  (order_sql.length <= 5 && (sql_type=='online' || sql_type=='human')){
        	new PNotify({
                title: 'Warning!',
                text: '请检查SQL文件是否为空~',
                type: 'warning',
                styling: 'bootstrap3'
            }); 
        	btnObj.attr('disabled',false);
			return false;		    	
	    };
	    var formData = new FormData();
	    if (sql_type=='file'){
	    	formData.append('order_file', $('#order_file')[0].files[0]);
	    };
	    
		if (!$('#order_executor option:selected').val().length){
        	new PNotify({
                title: 'Warning!',
                text: '审核人不能为空',
                type: 'warning',
                styling: 'bootstrap3'
            }); 
        	return false
		}		    
	    
	    formData.append('order_desc',$('#order_desc').val());
	    formData.append('order_db',$('#order_db option:selected').val());
	    formData.append('order_executor',$('#order_executor option:selected').val());
	    formData.append('sql_backup',$('#sql_backup option:selected').val());
	    formData.append('order_sql',order_sql);
	    formData.append('sql_type',sql_type);
	    formData.append('type','sql_audit');
	    formData.append('start_time',start_time);
	    formData.append('end_time',end_time);		    
		$.ajax({
			url:'/order/apply/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    contentType: false,				
			data:formData,  //提交参数
			success:function(response){		
				btnObj.attr('disabled',false);
				if (response["code"] == 200){
					var success = true;
					if (sql_type=='online' && $.isArray(response["data"])){
						document.getElementById("auditResultDiv").style.display = ""; 
						var resultHTML =  '<table class="table table-hover" id="auditResult">' +
	                    '<thead>' +
	                        '<tr>' +
	                            '<th>#</th>' +
	                            '<th>SQL</th>' +
	                            '<th>影响行</th>' +
	                            '<th>错误原因</th>' +
	                        '</tr>' +
	                	'</thead>' +
	                	'<tbody>'
					     var trHtml = ''
					     for (var i=0;i< response['data'].length;i++){
					    	 if(response['data'][i]["errlevel"]>0){
					    		 success = false
					    		 console.log(success)
					    	 }
					    	 trHtml +=   '<tr>' + 
					                         '<td>'+ i +'</td>' + 
					                         '<td>'+ response['data'][i]['sqltext'] +'</td>' + 
					                         '<td>'+ response['data'][i]['affectrow'] +'</td>' + 
					                         '<td>'+ response['data'][i]['errormessage'] +'</td>' + 
					                     '</tr>'
					     }
						resultHTML = resultHTML + trHtml + '</tbody></table>'
						$('#auditResult').html(resultHTML);		
					}
					if(success){
		            	new PNotify({
		                    title: 'Success!',
		                    text: '工单申请成功',
		                    type: 'success',
		                    styling: 'bootstrap3'
		                }); 						
					}else{
		            	new PNotify({
			                title: 'Warning!',
			                text: '工单申请失败',
			                type: 'error',
			                styling: 'bootstrap3'
		                }); 						
					}
					
				}
				else {
		    		$.alert({
		    		    title: '工单申请失败',
		    		    content: response["msg"],
		    		    type: 'red',
		    		});		    		
				};
			},
	    	error:function(response){
	    		btnObj.attr('disabled',false);
	        	new PNotify({
	                title: 'Warning!',
	                text: '工单申请失败',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	    	}
		});	    	
    });		
	
    	
	$("button[name='btn-fileupload-add']").on('click', function() {	
		var btnObj = $(this);
		var required = ["order_subject","dest_path","order_executor","dest_path","chown_user","chown_rwx","server_model","order_files","order_content"];
	    var formData = new FormData();
		var fileSelect = document.getElementById('order_files');
		var files = fileSelect.files;		
		for (var i = 0; i < files.length; i++) {
			  var file = files[i];
			  formData.append('order_files', file, file.name);
		}			
		btnObj.attr('disabled',true);
		var form = document.getElementById('audit_fileupload_order');
		for (var i = 0; i < form.length; ++i) {
			var name = form[i].name;
			var value = form[i].value;	
			idx = $.inArray(name, required);						
			if (idx >= 0 && value.length == 0){
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 	
            	btnObj.attr('disabled',false);
				return false;
			}
			if (name=="order_time"){
				var start_time = value.split(" - ")[0]
				var end_time = value.split(" - ")[1]
			}			
		};
		var serverList = new Array();
		$("#applyFileUploadDiv select[name='custom'] option:selected").each(function(){
			serverList.push($(this).val());
        });
		for (var i = 0; i < files.length; i++) {
			  var file = files[i];
			  formData.append('order_files[]', file, file.name);
		}	
		
		if (!$('#fileupload_order_executor option:selected').val().length){
        	new PNotify({
                title: 'Warning!',
                text: '审核人不能为空',
                type: 'warning',
                styling: 'bootstrap3'
            }); 
        	return false
		}		
		
	    formData.append('order_desc',$('#fileupload_order_subject').val());
	    formData.append('dest_path',$('#dest_path').val());
	    formData.append('chown_user',$('#chown_user').val());		    
	    formData.append('chown_rwx',$('#chown_rwx').val());
	    formData.append('order_content',$('#order_content').val());
	    formData.append('type','upload_audit');
	    formData.append('server',serverList);
	    formData.append('order_executor',$('#fileupload_order_executor option:selected').val());
	    formData.append('start_time',start_time);
	    formData.append('end_time',end_time);	    
		$.ajax({
/* 				dataType: "JSON", */
			url:'/order/apply/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    contentType: false,				
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');				
				if (response["code"] == 200){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '工单申请成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
				}
				else {
		    		$.alert({
		    		    title: '工单申请失败',
		    		    content: response["msg"],
		    		    type: 'red',
		    		});	
				};
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	        	new PNotify({
	                title: 'Warning!',
	                text: '工单申请失败',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	    	}
		});	
	})   			
	
	$("button[name='btn-filedownload-add']").on('click', function() {	
		var btnObj = $(this);
		var required = ["order_subject","order_executor","dest_path","order_content","order_time"];
	    var formData = new FormData();		
		btnObj.attr('disabled',true);
		var form = document.getElementById('audit_filedownload_order');
		for (var i = 0; i < form.length; ++i) {
			var name = form[i].name;
			var value = form[i].value;	
			idx = $.inArray(name, required);						
			if (idx >= 0 && value.length == 0){
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 	
            	btnObj.attr('disabled',false);
				return false;
			}
			if (name=="order_time"){
				var start_time = value.split(" - ")[0]
				var end_time = value.split(" - ")[1]
			}
		};
		var serverList = new Array();
		$("#applyFileDownloadDiv select[name='custom'] option:selected").each(function(){
			serverList.push($(this).val());
        });		
		
		if (!$('#filedownload_order_executor option:selected').val().length){
        	new PNotify({
                title: 'Warning!',
                text: '审核人不能为空',
                type: 'warning',
                styling: 'bootstrap3'
            }); 
        	return false
		}
		
	    formData.append('order_desc',$('#filedownload_order_subject').val());
	    formData.append('dest_path',$('#filedownload_dest_path').val());
	    formData.append('order_content',$('#filedownload_order_content').val());
	    formData.append('type','download_audit');
	    formData.append('server',serverList);
	    formData.append('order_executor',$('#filedownload_order_executor option:selected').val());
	    formData.append('start_time',start_time);
	    formData.append('end_time',end_time);
		$.ajax({
/* 				dataType: "JSON", */
			url:'/order/apply/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    contentType: false,				
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');				
				if (response["code"] == 200){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '工单申请成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
				}
				else {
		    		$.alert({
		    		    title: '工单申请失败',
		    		    content: response["msg"],
		    		    type: 'red',
		    		});	
				};
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	        	new PNotify({
	                title: 'Warning!',
	                text: '工单申请失败',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	    	}
		});	
	}) 	

	$("button[name='btn-service-add']").on('click', function() {	
		var btnObj = $(this);
		var required = ["order_subject","order_executor","order_content","order_time"];
	    var formData = new FormData();
		var fileSelect = document.getElementById('service_order_files');
		var files = fileSelect.files;		
		for (var i = 0; i < files.length; i++) {
			  var file = files[i];
			  formData.append('order_files', file, file.name);
		}
		btnObj.attr('disabled',true);
		var form = document.getElementById('audit_service_order');
		for (var i = 0; i < form.length; ++i) {
			var name = form[i].name;
			var value = form[i].value;	
			idx = $.inArray(name, required);						
			if (idx >= 0 && value.length == 0){
            	new PNotify({
                    title: 'Warning!',
                    text: '请注意必填项不能为空~',
                    type: 'warning',
                    styling: 'bootstrap3'
                }); 	
            	btnObj.attr('disabled',false);
				return false;
			}
			if (name=="order_time"){
				var start_time = value.split(" - ")[0]
				var end_time = value.split(" - ")[1]
			}			
		};
		var serverList = new Array();
		$("#applyFileUploadDiv select[name='custom'] option:selected").each(function(){
			serverList.push($(this).val());
        });
		for (var i = 0; i < files.length; i++) {
			  var file = files[i];
			  formData.append('order_files[]', file, file.name);
		}	
		
		if (!$('#service_order_executor option:selected').val().length){
        	new PNotify({
                title: 'Warning!',
                text: '审核人不能为空',
                type: 'warning',
                styling: 'bootstrap3'
            }); 
        	return false
		}		
	    formData.append('order_desc',$('#service_order_subject').val());
	    formData.append('order_content',$('#service_order_content').val());
	    formData.append('order_executor',$('#service_order_executor option:selected').val());
	    formData.append('type','service_audit');
	    formData.append('start_time',start_time);
	    formData.append('end_time',end_time);	    
		$.ajax({
/* 				dataType: "JSON", */
			url:'/order/apply/', //请求地址
			type:"POST",  //提交类似
		    processData: false,
		    contentType: false,				
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');				
				if (response["code"] == 200){
	            	new PNotify({
	                    title: 'Success!',
	                    text: '工单申请成功',
	                    type: 'success',
	                    styling: 'bootstrap3'
	                }); 
				}
				else {
		    		$.alert({
		    		    title: '工单申请失败',
		    		    content: response["msg"],
		    		    type: 'red',
		    		});	
				};
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	        	new PNotify({
	                title: 'Warning!',
	                text: '工单申请失败',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	    	}
		});	
	}) 	
	
})