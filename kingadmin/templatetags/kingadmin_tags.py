from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time
register = Library()
@register.simple_tag
def get_selected_m2m_data(field_name, form_obj, admin_class):
	'''
	返回已经选择的m2m数据信息
	'''
	select_data = getattr(form_obj.instance, field_name).all()
	return select_data


@register.simple_tag
def get_available_m2m_data(field_name, form_obj, admin_class):
	'''
	返回m2m关联的所有数据
	'''
	#获取字段对象
	field_obj = admin_class.model._meta.get_field(field_name)
	#获取mantyToMany字段对应的所有数据
	obj_list = set(field_obj.related_model.objects.all())
	select_data = set(getattr(form_obj.instance, field_name).all())
	#差集
	print("ssssss: ",obj_list,select_data)
	return obj_list - select_data

@register.simple_tag
def get_obj_field_val(form_obj, field): 
	return getattr(form_obj.instance, field)

@register.simple_tag
def get_sorted_column_index(sorted_o):
	'''
	获取排序的字段信息
	'''
	return list(sorted_o.values())[0] if sorted_o else ''

@register.simple_tag
def render_filter_arg(admin_class, render_html=True):
	'''
	拼接筛选的字段
	'''
	if admin_class.filter_conditions:
		ele = ''
		for k,v in admin_class.filter_conditions.items():
			ele+='&%s=%s' % (k,v)
		if render_html:
			return mark_safe(ele)
		else:
			return ele
	else:
		return ''
@register.simple_tag
def render_sorted_arrow(column, sorted_o):
	if column in sorted_o:
		sorted_index = sorted_o[column]
		if sorted_index.startswith('-'):
			action = 'bottom'
		else:
			action = 'top'
		ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % action
		return mark_safe(ele)
	else:
		return ''

@register.simple_tag
def render_sorted_url(counter0,column, sorted_o):
	if column in sorted_o:#如果字段在sorted_o中代表上次排序过
		last_sorted_index = sorted_o[column]
		if last_sorted_index.startswith('-'):
			this_time_index = last_sorted_index.strip('-')
		else:
			this_time_index = '-%s' % last_sorted_index
		return this_time_index
	else:
		return counter0

@register.simple_tag
def render_paginator_btn(querysets, admin_class, sorted_o):
	ele='''
	<ul class="pagination">
		<li>
			<a href="#" aria-label="Previous">
				<span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
			</a>
		</li>
	'''
	for i in querysets.paginator.page_range:
		active=''
		if abs(querysets.number-i) < 3:
			if querysets.number == i:
				active = 'active'
			get_filter_ele = render_filter_arg(admin_class)

			sorted_ele = ''
			if sorted_o:
				sorted_ele = '&_o=%s' % list(sorted_o.values())[0]

			p_ele = "<li class='%s'><a href='?_page=%s%s%s'>%s</a></li>" % (active,i,get_filter_ele,sorted_ele,i)
			ele+=p_ele
	ele+='<li><a href="#" aria-label="Next"><span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span></a></li></ul>'
	return mark_safe(ele)

@register.simple_tag
def get_model_name( admin_class ):
	'''
		获取模型名称并且返回大写的
	'''
	return admin_class.model._meta.verbose_name_plural
@register.simple_tag
def build_filter_ele(filter_column, admin_class):
	
	column_obj = admin_class.model._meta.get_field(filter_column)
	try:
		filter_ele="<div class='col-md-2'><span>%s</span><select class='form-control' name='%s' > " % (filter_column,filter_column)
		for choice in column_obj.get_choices():
			selected=''
			if filter_column in admin_class.filter_conditions:
				#根据admin_class.filter_conditions判断需要展示的过滤条件
				if str(choice[0]) == admin_class.filter_conditions.get(filter_column):#代表当前的option被过滤了设置成选中状态
					option = "<option value='%s' selected>%s</option>" % (choice)
					selected = 'selected'

			option = "<option value='%s' %s >%s</option>" % (choice[0],selected,choice[1])
			filter_ele+=option
			
	except AttributeError as e:
		filter_ele="<div class='col-md-2'><span>%s</span><select class='form-control' name='%s__gte' > " % (filter_column,filter_column)
		#获取字段类型
		if column_obj.get_internal_type() in ('DateField','DateTimeField'):
			opt_list = []
			#获取时间戳
			time_obj = datetime.datetime.now()
			#获取当天时间
			opt_list.append(['%s-%s-%s'%(time_obj.year,time_obj.month,time_obj.day),'Today'])
			'''
				import datetime
				datetime.now() - datetime.timedelta(3) 当前时间减3天
			'''
			time_list = [
				['','---------'],
				[time_obj,'Today'],
				[time_obj - datetime.timedelta(7),'7天内'],
				[time_obj.replace(day=1),'本月'],
				[time_obj - datetime.timedelta(90),'三月天内'],
				[time_obj.replace(month=1,day=1),'YearToDay'],
				['','All'],
			]

			for i in time_list:
				selected = ''
				#需要根据时间戳拼接对应的过滤字符
				time_to_str = '' if not i[0] else '%s-%s-%s' % (i[0].year,i[0].month,i[0].day)
				#时间过滤时拼接__gte比较字符， 用于判断大小查询
				if '%s__gte'%filter_column in admin_class.filter_conditions:
					#根据admin_class.filter_conditions判断需要展示的过滤条件
					if time_to_str == admin_class.filter_conditions.get('%s__gte'%filter_column):#代表当前的option被过滤了设置成选中状态
						selected = 'selected'
				option = "<option value='%s' %s>%s</option>" % (time_to_str,selected, i[1])
				filter_ele+=option
				
	filter_ele+='</select></div>'
	#print('>>> filter_ele= ',filter_ele)
	return mark_safe(filter_ele)

@register.simple_tag
def build_table_row(obj, admin_class):

	ele=''
	td_ele=''
	if admin_class.list_display:
		for index,column_name in enumerate(admin_class.list_display) :
			'''
			获取一个字段对象
			models.CustomserInfo._meta.get_field('status')
			查询choices信息
			models.CustomserInfo._meta.get_field('status').choices
			'''
			column_obj = admin_class.model._meta.get_field(column_name)
			#判断是否有choices，有choice时显示对应的汉字信息
			if column_obj.choices:
				#getattr(obj,'get_{}_display'.format(column_name))返回一个方法需加一个()执行
				column_data = getattr(obj,'get_%s_display' % (column_name))()
			else:
				column_data = getattr(obj,column_name)
			if index == 0:
				td_ele += "<td><a href='%s/change/'>%s</a></td>"% (obj.id,column_data)
			else:
				td_ele += '<td>%s</td>'% (column_data)
	else:#默认为空直接显示模型对象的str属性值
		td_ele += "<td><a href='%s/change/'>%s</a></td>"% (obj.id, obj)
			
	ele+=td_ele
	return mark_safe(ele)
	
