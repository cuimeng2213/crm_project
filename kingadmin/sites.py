from kingadmin.admin_base import BaseKingAdmin
class AdminSite(object):
	def __init__(self):
		#通过import多次导入同一个模块时只执行一次，由于python进行的优化
		print('AAAAAAAAAAAAAAAA: init AdminSite')
		self.enabled_admins = {}
	#def register(self, model_class, admin_class=BaseKingAdmin):#如果未给admin_class赋值使用默认的基类之后页面显示的内容是最后一次注册的对象信息
	def register(self, model_class, admin_class=None):#如果未给admin_class赋值使用默认的基类之后页面显示的内容是最后一次注册的对象信息
		'''
		注册admin表
		'''
		'''
		enabled_admins = {
			'crm':{'customer':CustomerAdmin,'Role':RoleAdmin}
		}
		'''
		#通过类获取app名字
		app_name = model_class._meta.app_label
		#通过类获取表名
		model_name = model_class._meta.model_name
		#如果未给admin_class赋值使用默认的基类之后页面显示的内容是最后一次注册的对象信息,解决办法实例化admin_class
		#为了避免多个model共享一个BaseKingAdminn内存对象
		if not admin_class:
			admin_class = BaseKingAdmin()
		else:
			admin_class = admin_class()
		#把model_class 赋值给了admin_class
		admin_class.model = model_class#如果未给admin_class赋值使用默认的基类之后页面显示的内容是最后一次注册的对象信息,解决办法实例化admin_class
		
		if app_name not in self.enabled_admins:
			self.enabled_admins[app_name] = {}
		self.enabled_admins[app_name][model_name] = admin_class
		
site = AdminSite()

		