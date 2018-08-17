from django.shortcuts import render
#认证装饰器
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard(request):
	return render(request, 'index.html')
	
