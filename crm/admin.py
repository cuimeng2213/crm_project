from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
	list_display = ['name','source','contact_type','contact','consultant','consult_content','status','date']
	list_filter = ['source','consultant','status','date']
	#Related Field got invalid lookup: icontains
	#consultant是外键需要指定所搜属性
	search_fields = ['contact','consultant_name']
	list_per_page = 2
	
	actions = ["change_status"]
	def change_status(self, *args, **kwargs):
		print("change_status")


admin.site.register(UserProfile)
admin.site.register(CustomerInfo,CustomerAdmin)
admin.site.register(Student)
admin.site.register(Menus)
admin.site.register(CustomerFollowUp)
admin.site.register(Course)
admin.site.register(ClassList)
admin.site.register(CourseRecord)
admin.site.register(Role)
admin.site.register(Branch)
admin.site.register(StudyRecord)
