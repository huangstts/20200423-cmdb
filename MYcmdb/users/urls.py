
from django.urls import path,re_path
from . import views


app_name = "users"

urlpatterns = [
    path('login/',views.UsersLoginView.as_view(),name="usersLogin"),
    path('logout/',views.UsersLogoutView.as_view(),name="usersLogout"),
    path('register/',views.UserRegisterFormView.as_view(),name="usersRegister"),
    path('forget_pwd/',views.ForgetPwdView.as_view(),name="forgetPwd"),
    path('lockscreen/',views.UsersLockscreenView.as_view(),name="Lockscreen"),

    path('user-list/',views.UserListView.as_view(),name="userList"),
    path('user-add/',views.AddUser.as_view(),name="userAdd"),
    path('user-delete/<slug:pk>/',views.DeleteUser.as_view(),name="userDelete"),
    path('user-alter/<slug:pk>/',views.AlterUser.as_view(),name="userAlter"),


]
