from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
	"""
	用户信息表
	"""
	#用于登录
	user = models.OneToOneField(User)
	name = models.CharField(max_length=64, verbose_name='姓名')
	#双向一对多就是多对多关系
	#多不多字段不需要null=True
	role = models.ManyToManyField('Role', blank=True)
	
	def __str__(self):#__unicode__ 2.7为这个
		return self.name
	class Meta:
		verbose_name='用户信息'
class Role(models.Model):
	'''
	角色表
	'''
	name = models.CharField(max_length=64, unique=True)
	menus = models.ManyToManyField('Menus')
	
	def __str__(self):
		return self.name
	
class CustomerInfo(models.Model):
	'''
	客户信息表
	'''
	name = models.CharField(max_length=64, default=None)
	#联系方式
	contact_type_choices = ((0,'QQ'),(1,'微信'),(2,('手机')))
	contact_type = models.SmallIntegerField(choices=contact_type_choices, default=0)
	contact = models.CharField(max_length=64,unique=True)
	#客户来源
	source_choices=((0,'QQ群'),(1,'51CTO'),(2,'百度推广'),(3,'知乎'),(4,'转介绍'),(5,'其他'))
	source = models.SmallIntegerField(choices=source_choices)
	#转介绍人，关联自己
	refferal_from = models.ForeignKey('self', blank=True, null=True, verbose_name='转介绍')
	#课程咨询
	sonsult_courses = models.ManyToManyField("Course", verbose_name='咨询课程')
	#咨询内容记录
	consult_content = models.TextField(verbose_name='咨询内容')
	consultant = models.ForeignKey('UserProfile',verbose_name='课程顾问')
	#报名状态
	status_choices=((0,'未报名'),(1,'已报名'),(2,'已退学'))
	status = models.SmallIntegerField(choices=status_choices)
	date = models.DateField(auto_now_add=True)
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = '客户信息'
		verbose_name_plural = verbose_name

class Student(models.Model):
	'''
		学员表
	'''
	customer = models.ForeignKey('CustomerInfo')
	#班级问题，如果一个学员报了多个班级怎么处理, 直接关联多个班级
	class_grade = models.ManyToManyField('ClassList')
	
	def __str__(self):
		return self.name

class CustomerFollowUp(models.Model):
	'''
	客户跟踪记录表
	'''
	customer = models.ForeignKey('CustomerInfo')
	content = models.TextField(verbose_name='跟踪内容')
	user=models.ForeignKey('UserProfile',verbose_name='跟进人')
	status_choice = ((0,'近期无报名计划'),(1,'一个月内报名'),(2,'2周内报名'),(3,'已报名'))
	status = models.SmallIntegerField(choices=status_choice)
class Course(models.Model):
	'''
	课程表
	'''
	name = models.CharField(max_length=64,verbose_name='课程名称', unique=True)
	price = models.PositiveSmallIntegerField(verbose_name='课程价格')
	outline = models.TextField(verbose_name='课程大纲')
	period = models.PositiveSmallIntegerField(verbose_name='课程周期(月)',default=5)
	
	def __str__(self):
		return self.name
	
class ClassList(models.Model):
	'''
	班级列表
	'''
	branch = models.ForeignKey('Branch')
	course = models.ForeignKey('Course')
	class_type_choice = ((0,'脱产'),(1,'周末班'),(2,'网络班'))
	class_type= models.SmallIntegerField(choices=class_type_choice,verbose_name='班级类型',default=0)
	semester = models.SmallIntegerField(verbose_name='学期')
	teacher = models.ManyToManyField('UserProfile', verbose_name='讲师')
	start_date = models.DateField(u'开班日期')
	graduate_date = models.DateField(verbose_name='毕业日期', blank=True, null=True)
	
	def __str__(self):
		return '{}{}'.format(self.course.name, self.semster)
		
	#课程不能重复需要联合为一
	class Meta:
		unique_together = ('branch','course','semester')
	
class CourseRecord(models.Model):
	'''
	上课记录
	'''
	class_grade = models.ForeignKey('ClassList', verbose_name='上课班级')
	day_num = models.PositiveSmallIntegerField(verbose_name='课程节次')
	teacher = models.ForeignKey('UserProfile', verbose_name='讲师')
	title = models.CharField(max_length=64, verbose_name='本节主题')
	content = models.TextField(verbose_name='本节内容')
	has_homework = models.BooleanField(verbose_name='本节有作业',default=False)
	homework = models.TextField(verbose_name='作业需求', blank=True, null=True)
	date = models.DateField(auto_now_add = True)
	
	def __str__(self):
		return '{}{}'.format(self.class_grade, self.day_num)
	
	class Meta:
		unique_together = ('class_grade','day_num')
		
class StudyRecord(models.Model):
	'''
	学习记录
	'''
	course_record = models.ForeignKey('CourseRecord',verbose_name='课程')
	student = models.ForeignKey('Student')
	#N/A
	socre_choice = ((100,'A+'),(90,'A'),(85,'B+'),(80,'B'),(75,'B-'),(70,'C+'),(60,'C'),(40,'C-'),(-50,'D'),(0,'N/A'),(-100,'COPY'))
	score = models.SmallIntegerField(choices=socre_choice,default=None)
	show_choice = ((0,'缺勤'),(1,'已签到'),(2,'迟到'),(3,'早退'))
	show_status = models.SmallIntegerField(choices=show_choice)
	note = models.TextField(verbose_name='成绩备注', blank=True, null=True)
	date = models.DateField(auto_now_add=True)
	
	def __str__(self):
		return '{}{}{}'.format(self.corese_record,self.student,self.score)
	
class Branch(models.Model):
	'''
	校区分支
	'''
	name = models.CharField(max_length=64, verbose_name='校区',unique=True)
	addr = models.CharField(max_length=128, verbose_name='地址')
	def __str__(self):
		return self.name
class Menus(models.Model):
	'''
	d动态菜单
	'''
	name = models.CharField(max_length=64,verbose_name='菜单名字')
	#url写死之后对于url带参数怎么设置?使用两种模式
	url_type_choice = ((0,'absolute'),(1,'dynamic'))
	url_type = models.SmallIntegerField(choices=url_type_choice)
	url_name = models.CharField(max_length=128)
	
	class Meta:
		verbose_name ='菜单'
		verbose_name_plural = '菜单'
		unique_together = ('name','url_name')
		
	def __str__(self):
		return self.name
	
	
	
	
	
	
	