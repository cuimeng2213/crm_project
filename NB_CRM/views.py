from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

'''
认证登录使用django自带的认证
'''
def acc_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		print(username,password)
		#判断用户名密码
		user = authenticate(username=username, password=password)
		if user:
			print('passed authenticated')
			#登录动作
			login(request, user)
			#此处的跳转不能写死，获取next参数，如果next为空跳转到首页 http://127.0.0.1:8000/login/?next=/crm/index/
			print('next: ', request.GET.get('next'))
			nextUrl = request.GET.get('next')
			if nextUrl:
				return redirect(nextUrl)
			else:
				return redirect('/crm/index/')
	
	return render(request,'login.html')

def acc_logout(request):
	logout(request)
	
	return redirect('/login/')
