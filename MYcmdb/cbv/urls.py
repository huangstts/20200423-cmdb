
from django.urls import path,re_path,register_converter
from . import views


app_name = "cbv"
urlpatterns = [
    path('servers/',views.ServerNode.as_view()),
    path('cbvserver-list/',views.ServerListView.as_view(),name="cbvserverList"),
    path('cbvserver-detail/<slug:pk>/', views.ServerDetailView.as_view(),name="cbvserverDetail"),
    path('cbvserver-table/<slug:pk>/', views.ServerTableView.as_view(),name="cbvserverTable"),
    path('cbvasset-list/',views.AssetListView.as_view(),name="cbvassetList"),
    path('cbvasset-detail/<slug:pk>/', views.AssetDetailView.as_view(),name="cbvassetDetail"),
]