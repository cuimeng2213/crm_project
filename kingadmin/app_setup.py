from django import conf
def kingadmin_auto_discover():
	print('find kingadmin model.......')
	for app_name in conf.settings.INSTALLED_APPS:
		#mod = importlib.import_module(app_name,'kingadmin')
		try:
			#反射方法使用
			#根据字符串导入crm下面的kingadmin文件
			mod = __import__('{}.kingadmin'.format(app_name))
			if hasattr(mod,'kingadmin'):
				print('AAAA: ',mod.kingadmin)
		except ImportError:
			pass