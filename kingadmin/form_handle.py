from django.forms import ModelForm


def create_dynamic_model_form(admin_class):
	'''
	动态生成modelForm
	'''
	class Meta:
		model = admin_class.model
		fields = '__all__'

	dynamic = type('DynamicModelForm', (ModelForm,), {'Meta':Meta})
	print('>>> dynamic ',dir(admin_class))
	return dynamic