#自定义过滤器
from django_filters import rest_framework as filters
from cmdb.models import Server, Memory

class ServersFilter(filters.FilterSet):
    os_name = filters.CharFilter(field_name='os_name',  lookup_expr='icontains')
    # create_at_min = filters.DateFromToRangeFilter(field_name='create_at',label="创建时间 大于等于")
    physical_count = filters.RangeFilter(field_name='physical_count',label="cpu")
    # physical_count_min = filters.CharFilter(
    #     field_name='physical_count', lookup_expr='gte',label="cpu物理颗数 大于等于")
    # physical_count_max = filters.CharFilter(
    #     field_name='physical_count', lookup_expr='lte', label="cpu物理颗数 小于等于")

    class Meta:
        model = Server
        fields = ['os_name','physical_count']


class MemorysFilter(filters.FilterSet):
    slot = filters.CharFilter(field_name='slot',  lookup_expr='icontains')
    # create_at_min = filters.DateFromToRangeFilter(field_name='create_at',label="创建时间 大于等于")
    # physical_count = filters.RangeFilter(field_name='physical_count',label="cpu")
    # physical_count_min = filters.CharFilter(
    #     field_name='physical_count', lookup_expr='gte',label="cpu物理颗数 大于等于")
    # physical_count_max = filters.CharFilter(
    #     field_name='physical_count', lookup_expr='lte', label="cpu物理颗数 小于等于")

    class Meta:
        model = Memory
        fields = ['slot']
