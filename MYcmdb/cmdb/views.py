import json
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from cmdb.models import Server,Memory,Disk,Asset,Cabinet,IDC,TreeNode

from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')

class AssetView(View):
    def get(self, request):

        return HttpResponse("get方法")

    def post(self, request):
        print("body 数据", request.body)
        asset_s = str(request.body, encoding='utf-8')
        asset_data = json.loads(asset_s)
        print("JSON 数据", asset_data)

        base_dic = asset_data["base_info"]
        cpu_dic = asset_data["cpu_info"]
        server_dic = { **base_dic, **cpu_dic}
        try:
            server_obj = Server.objects.create(**server_dic)
        except Exception as e:
            print(e)
            return HttpResponse("存库失败")
        
        mem_list = asset_data["mem_info"].values()
        [mem.update(server=server_obj) for mem in mem_list]
        try:
            for item in mem_list:   
                Memory.objects.create(**item)
        except Exception as e:
            print(e)
            return HttpResponse("内存存库失败")
        
        disk_list = asset_data["disk_info"].values()
        [disk.update(server=server_obj) for disk in disk_list]        
        try:
            for item in disk_list:   
                Disk.objects.create(**item)
        except Exception as e:
            print(e)
            return HttpResponse("硬盘存库失败")


        return HttpResponse("上报成功")

from rest_framework import viewsets
from .serializers import ServerSerializer,MemorySerializer,DiskSerializer,DiskSerializer2,AssetSerializer,CabinetSerializer,IDCSerializer,TreeNodeSerializer
##############  自定义过滤器
from .api_filters import ServersFilter,MemorysFilter
from django_filters.rest_framework import DjangoFilterBackend
####基于搜索的过滤
from rest_framework import filters

from .page import StandardResultsSetPagination

class ServersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer  #序列化
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter] #过滤器
    filter_class = ServersFilter  #自定义过滤
    search_fields = ['$host_name', 'os_name']    #搜索匹配的字段
    ordering_fields = ["physical_count", "disk__id"]  #自定义排序的字段
    ordering = ["-physical_count"] # 默认排序字段
    pagination_class = StandardResultsSetPagination  #使用自定义分页类


class MemorysViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    # filter_class = MemorysFilter
    search_fields = ['slot']
    ordering = ["-id"] # 默认排序字段
    pagination_class = StandardResultsSetPagination  #使用自定义分页类

class DisksViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['slot']
    ordering = ["-id"] # 默认排序字段
    pagination_class = StandardResultsSetPagination  #使用自定义分页类


class AssetsViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    ordering = ["-id"] # 默认排序字段 
    pagination_class = StandardResultsSetPagination



class CabinetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    ordering = ["-id"] # 默认排序字段
    pagination_class = StandardResultsSetPagination





class IDCViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    ordering = ["-id"] # 默认排序字段
    pagination_class = StandardResultsSetPagination



class TreeNodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TreeNode.objects.filter(node_upstream=None)
    serializer_class = TreeNodeSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    ordering = ["-id"] # 默认排序字段
    pagination_class = StandardResultsSetPagination


######2020-04-11
from django.views.generic import ListView,DetailView
class ServersListView(ListView):
    model = Server
    context_object_name = "serverList"
    template_name = "cmdb/servers-list.html"

class DisksListView(ListView):
    model = Disk
    context_object_name = "diskList"
    template_name = "cmdb/disks-list.html"

class MemoryListView(ListView):
    model = Memory
    context_object_name = "memoryList"
    template_name = "cmdb/memorys-list.html"

class IDCListView(ListView):
    model = IDC
    context_object_name = "idcList"
    template_name = "cmdb/idc-list.html"

class CabinetListView(ListView):
    model = Cabinet
    context_object_name = "cabinetList"
    template_name = "cmdb/cabinet-list.html"

class AssetListView(ListView):
    model = Asset
    context_object_name = "assetList"
    template_name = "cmdb/assets-list.html"










