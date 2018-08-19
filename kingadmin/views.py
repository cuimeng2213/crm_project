from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#动态导入settings文件的installed_apps
from django import conf
from kingadmin import app_setup
from kingadmin.sites import site
import importlib
from django.db.models import Q
from . import form_handle

#动态导入settings文件的installed_apps
app_setup.kingadmin_auto_discover()
'''
认证登录使用django自带的认证
'''
def acc_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		print(username,password)
		#判断用户名密码
		user = authenticate(username=username, password=password)
		if user:
			print('passed authenticated')
			#登录动作
			login(request, user)
			#此处的跳转不能写死，获取next参数，如果next为空跳转到首页 http://127.0.0.1:8000/login/?next=/crm/index/
			print('next: ', request.GET.get('next'))
			return redirect(request.GET.get('next','/kingadmin/'))
	
	return render(request,'kingadmin/login.html')

def acc_logout(request):
	logout(request)
	
	return redirect('/login/')
@login_required	
def app_index(request):

	return render(request,'kingadmin/app_index.html',{'site':site})
	
def filter_by_options(req, querysets):
	'''
	执行过滤操作
	'''
	filter_conditions = {}
	for key, val in req.GET.items():
		#分页、排序、参数字段不在过滤字段中直接执行下一个循环
		if key in ('_page','_o','_q'): continue
		if val:
			filter_conditions[key] = val
	print('>>>filter_conditions ', filter_conditions)
	return querysets.filter(**filter_conditions),filter_conditions

def sorted_by_options(req, qy,admin_class):
	'''
	排序功能实现
	'''
	sorted_o = {}
	option = req.GET.get('_o')
	if option:#有值代表需要排序
		orderby_key = admin_class.list_display[abs(int(option))]
		sorted_o[orderby_key] = option
		if option.startswith('-'):
			orderby_key = '-%s' % orderby_key

		return qy.order_by(orderby_key), sorted_o
	#默认返回无排序的数据
	return qy, sorted_o
def get_searched_result(request,querysets,admin_class):

	search_key = request.GET.get('_q')
	if search_key:
		q = Q()
		q.connector='OR'
		for search_field in admin_class.search_field:
			q.children.append(('%s__contains'%search_field, search_key))
		return querysets.filter(q),search_key
	return querysets,search_key	
@login_required
def table_obj_list(request, app_name, model_name):
	#获取模型类
	print('>>>table_obj_list :  ', request.GET)
	admin_class = site.enabled_admins[app_name][model_name]
	querysets = admin_class.model.objects.all().order_by('-id')
	querysets,filter_conditions = filter_by_options(request, querysets)
	admin_class.filter_conditions = filter_conditions

	#搜索功能实现
	querysets, search_key =get_searched_result(request,querysets,admin_class)
	admin_class.search_key = search_key

	#排序功能--放到分页之前
	querysets,sorted_o = sorted_by_options(request,querysets, admin_class)
	
	#分页功能实现
	pager = Paginator(querysets,2)
	page = request.GET.get('_page')
	try:
		querysets = pager.page(page)
	except PageNotAnInteger:
		querysets = pager.page(1)
	except EmptyPage:
		querysets = pager.page(pager.num_pages)
		
	return render(request,'kingadmin/table_obj_list.html',{'querysets':querysets,'admin_class':admin_class,'sorted_o':sorted_o})

@login_required
def table_obj_change(request, app_name, model_name, obj_id):
	# from crm.forms import CustomerForm
	# form_obj = CustomerForm()
	admin_class = site.enabled_admins[app_name][model_name]
	model_form = form_handle.create_dynamic_model_form(admin_class)
	obj = admin_class.model.objects.get(id=obj_id)
	if request.method == 'GET':
		form_obj = model_form(instance=obj)
	elif request.method == 'POST':
		form_obj = model_form(instance=obj, data=request.POST)
		if form_obj.is_valid():
			form_obj.save()
			return redirect('/kingadmin/%s/%s/'%(app_name,model_name))

	return render( request, 'kingadmin/table_obj_change.html', locals() )
@login_required
def table_obj_add(request, app_name, model_name):
	'''
		新增数据视图
	'''
	admin_class = site.enabled_admins[app_name][model_name]
	model_form = form_handle.create_dynamic_model_form(admin_class, form_add=True)
	if request.method == 'GET':
		form_obj = model_form()
	elif request.method == 'POST':#添加数据
		form_obj = model_form(data=request.POST)
		if form_obj.is_valid():
			form_obj.save()
		return redirect('/kingadmin/%s/%s' % (app_name,model_name))
	return render(request, 'kingadmin/table_obj_add.html',locals())
