
from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse,reverse_lazy
from .models import UsersProfile
from django.views.generic import ListView,DetailView
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView   
class UsersLoginView(LoginView):
	# 指定一个用于接收到 GET 请求时，需要返回的模板文件
	template_name = "users/login.html"
class UsersLogoutView(LogoutView):
	# 用户退出登录后，将要跳转的 URL
	next_page = reverse_lazy('index')

from django.contrib.auth.hashers import check_password,make_password
class UsersLockscreenView(View):
    def get(self,request):
        return render(request,'users/lockscreen.html')
    def post(self,request):
        user_name = request.POST.get('username')
        user = UsersProfile.objects.filter(username=user_name)
        pwd = user[0].password
        pwd1 = request.POST.get('password')
        if check_password(pwd1,pwd):
            return redirect('index')
        else:
            return redirect('users:Lockscreen')

from django.views import View
from django.views.generic.edit import FormView
from users.users_forms import UserRegisterModelForm


class UserRegisterFormView(FormView):
	template_name = 'users/register.html'
	form_class = UserRegisterModelForm
	success_url = reverse_lazy('users:usersLogin')
	def form_valid(self,form):
		user = UsersProfile(**form.cleaned_data)
		user.set_password(form.cleaned_data['password'])
		user.save()
		return super().form_valid(form)
	def form_invalid(self,form):
		print("form-->", form)
		return super().form_invalid(form)


#### 增加修改密码功能
class ForgetPwdView(View):
    def get(self,request):
        return render(request,'users/forget_pwd.html')
    def post(self,request):
        user_name = request.POST.get('username','')
        user = UsersProfile.objects.filter(username=user_name)
        user_mobile = request.POST.get('mobile','')
        if user and user[0].mobile == user_mobile:
            pwd1 = request.POST.get('password')
            pwd2 = request.POST.get('password2')
            if pwd1 == pwd2:
                user[0].password = make_password(pwd1)
                user[0].save()
                return redirect('users:usersLogin')
            else:
                return render(request,'users/forget_pwd.html',{'error1':'两次密码不匹配'})
        else:
            return render(request,'users/forget_pwd.html',{'error2':'用户和手机号不匹配'}) 

class UserListView(LoginRequiredMixin,ListView):
    # 指定获取数据的 model
    model = UsersProfile
    # 指定模板语言中使用的变量名
    context_object_name = "userList"
    # 指明模板名称, 默认是 `model所在的应用名/model 名称的小写_list.html
    template_name = "users/user_list.html"    


class AddUser(FormView):
	template_name = 'users/adduser.html'
	form_class = UserRegisterModelForm
	success_url = reverse_lazy('users:userList')
	def form_valid(self,form):
		user = UsersProfile(**form.cleaned_data)
		user.set_password(form.cleaned_data['password'])
		user.save()
		return super().form_valid(form)
	def form_invalid(self,form):
		print("form-->", form)
		return super().form_invalid(form)


from django.http import HttpResponseRedirect
class AlterUser(FormView):
    def get(self, request,pk):
        pk=pk
        u=UsersProfile.objects.filter(id=pk)[0]
        context={'u':u}
        return render(request,'users/alter_user.html',context)

    def post(self, request,pk):
        user=UsersProfile.objects.filter(id=pk)[0]
        user.username=request.POST.get('username')
        user.email=request.POST.get('email')
        user.mobile=request.POST.get('mobile')
        user.age=request.POST.get('age')
        user.password=request.POST.get('password')
        user.set_password(user.password)
        user.save()
        print("body 数据",user.password)
        url = reverse_lazy('users:userList')
        return HttpResponseRedirect(url) #post重定向到了这个url 数据被重新加载
	

class DeleteUser(View):
    def get(self,request,pk):
        pk=pk
        UsersProfile.objects.filter(id=pk).delete()
        return render(request,'users/delete_user.html')



