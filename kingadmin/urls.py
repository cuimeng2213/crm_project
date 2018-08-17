from django.conf.urls import url
from kingadmin.views import *
urlpatterns = [
	url(r'$^', app_index, name='kingadmin'),
	url(r'login/', acc_login),
	url(r'^(\w+)/(\w+)/$', table_obj_list, name='table_obj_list'),
	url(r'^(\w+)/(\w+)/(\d+)/change/', table_obj_change, name='table_obj_change'),
]