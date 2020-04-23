from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.utils import timezone
from cmdb.models import Server,Asset
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ServerListView(ListView):
    # 指定获取数据的 model
    model = Server
    # 指定模板语言中使用的变量名
    context_object_name = "serverList"
    # 指明模板名称, 默认是 `model所在的应用名/model 名称的小写_list.html
    template_name = "cbv/cbvserver-list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ServerDetailView(LoginRequiredMixin,DetailView):
    login_url=reverse_lazy("users:usersLogin")
    model = Server
    context_object_name = "server"
    template_name = "cbv/cbvserver-detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ServerTableView(LoginRequiredMixin,DetailView):
    login_url=reverse_lazy("users:usersLogin")
    model = Server
    context_object_name = "server"
    template_name = "cbv/cbvserver-table.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
class AssetListView(ListView):
    # 指定获取数据的 model
    model = Asset
    # 指定模板语言中使用的变量名
    context_object_name = "assetList"
    # 指明模板名称, 默认是 `model所在的应用名/model 名称的小写_list.html
    template_name = "cbv/cbvasset-list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class AssetDetailView(LoginRequiredMixin,DetailView):
    login_url=reverse_lazy("users:usersLogin")
    model = Asset
    context_object_name = "asset"
    template_name = "cbv/cbvasset-detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context



class ServerNode(ListView):
    template_name = 'cbv/cbvserver-list.html'
    context_object_name = 'serverList'

    def get_queryset(self):
        node_id = self.request.GET.get("node_id")
        if node_id:
            queryset = Server.objects.filter(asset__node__id=node_id)
        else:
            queryset = Server.objects.all()
        return queryset