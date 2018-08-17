from kingadmin.admin_base import BaseKingAdmin
from kingadmin.sites import site
from crm import models
print('kingadmin .....................')

'''
自动发现和注册功能，生成全局的字典返回给调用者
'''
#继承BaseKingAdmin
class CustomerAdmin(BaseKingAdmin):
	list_display = ['id','name','source','contact_type','contact','consultant','consult_content','status','date']
	list_filter = ['source','contact_type','consultant','date']
	search_field = ['contact','consultant__name']
	
site.register(models.CustomerInfo,CustomerAdmin)
site.register(models.Menus)
site.register(models.UserProfile)
	