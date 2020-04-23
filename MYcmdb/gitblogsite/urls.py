"""gitblogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from extra_apps import xadmin
from gitblogsite import settings
from gitblogsite.settings import MEDIA_ROOT
from django.views.generic import TemplateView
from django.urls import path,re_path,include
from django.views.static import serve
from .views import index,diagram
from rest_framework.authtoken import views as auth_views

from .views import DashView
urlpatterns = [
    
    path('xadmin/', xadmin.site.urls),
    path('',index,name="index"),
    path('users/',include("users.urls")),  #使用include模块来使用users应用的路由
    path('cmdb/',include("cmdb.urls")), 
    path('cbv/',include("cbv.urls")), 
    # path('octopus/',include("octopus.urls")), 
    path('api-token-auth/', auth_views.obtain_auth_token),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    path('diagram/',diagram,name="diagram"),
    path('dash/',DashView.as_view())

]

handler404 = 'gitblogsite.views.page_not_found_view'
handler500 = 'gitblogsite.views.page_error'


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
