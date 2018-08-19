from django.forms import ModelForm


def create_dynamic_model_form(admin_class, form_add=False):
	'''
	动态生成modelForm
	'''
	class Meta:
		model = admin_class.model
		fields = '__all__'
		if not form_add:
			exclude = admin_class.readonly_fields# 将只读字段列表赋值给不包含验证的字段
			admin_class.form_add = False
		else:
			admin_class.form_add = True
	def __new__(cls,*args, **kwargs):
		# print(cls.base_fields)
		#通过修改new方法实现动态展示每个form字段
		#cls类方法中有个base_fields属性存放所有fields对象
		for field_name in cls.base_fields:
			field_obj = cls.base_fields[field_name]
			field_obj.widget.attrs.update({'class':'form-control'})
			#if field_name in cls.readonly_fields:
			#	cls.Meta.exclude.append(field_name)#由于Meta元类优先于new执行，所以此处动态添加不包含验证字段不生效
		return ModelForm.__new__(cls)

	dynamic = type('DynamicModelForm', (ModelForm,), {'Meta':Meta,'__new__':__new__})
	print('>>> dynamic ',dir(admin_class))
	return dynamic