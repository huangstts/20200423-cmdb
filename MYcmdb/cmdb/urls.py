from django.urls import include,path,re_path,register_converter
from . import views
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

router = DefaultRouter()
router.register('servers', views.ServersViewSet)
router.register('memorys', views.MemorysViewSet)
router.register('disks', views.DisksViewSet)
router.register('assets', views.AssetsViewSet)
router.register('cabinet', views.CabinetViewSet)
router.register('idc', views.IDCViewSet)
router.register('treenode', views.TreeNodeViewSet)

app_name = "cmdb"

urlpatterns = [
    path('', include(router.urls)),

    path('servers-list/',views.ServersListView.as_view(),name="serverslist"),
    path('disks-list/',views.DisksListView.as_view(),name="diskslist"),
    path('memorys-list/',views.MemoryListView.as_view(),name="memoryslist"),
    path('idc-list/',views.IDCListView.as_view(),name="idclist"),
    path('cabinet-list/',views.CabinetListView.as_view(),name="cabinetlist"),
    path('assets-list/',views.AssetListView.as_view(),name="assetslist"),
    path('asset/',views.AssetView.as_view(),name="getinfo"), #收集服务器信息


]