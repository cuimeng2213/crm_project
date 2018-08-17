from django.forms import ModelForm
from crm import models

'''
此处是一个静态的form表单类，
后续需要使用type方法自动生成form类
'''
class CustomerForm(ModelForm):
	class Meta:
		model = models.CustomerInfo
		fields = '__all__'


def create_dynamic_model_form(self, admin_class):
	'''
	动态生成modelForm
	'''
	class Mete:
		model = admin_class.model
		fields = '__all__'
	dynamic = type('DynamicModelForm', (ModelForm,), {'Meta':Meta})
	print(dynamic)