'''
创建BaseKingAdmin给所有的模型使用，如后续扩展功能直接在此类添加即可实现给所有模型添加新功能
'''
class BaseKingAdmin(object):
	#默认字段
	list_display = []
	list_filter = []
	search_field = []
	readonly_fields = []
	filter_horizontal = []