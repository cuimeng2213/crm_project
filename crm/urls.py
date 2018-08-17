from django.conf.urls import include, url
from crm.views import dashboard
urlpatterns = [
	url(r'index/',dashboard, name='sales_dashboard'),
]