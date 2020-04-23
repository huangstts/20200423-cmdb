import xadmin

# from .models import Server, Memory, Disk, IDC, Cabinet, Asset, TreeNode,Tag,Connection, InventoryPool, Variable2Server, Variable2Group
from .models import Server, Memory, Disk, IDC, Cabinet, Asset

#xadmin显示、过滤、搜索

class Variable2ServerAdmin(object):
    pass
class Variable2GroupAdmin(object):
    pass

class ConnectionAdmin(object):
    pass
class TreeNodeAdmin(object):
    pass
class TagAdmin(object):
    pass
class ServerAdmin(object):
    # 设置显示的字段   
    list_display = ("host_name","os_name",
"machine",
"os_version","asset")
    
    # 设置搜索的字段
    search_fields = (
   
"os_name","host_name",
"machine",
"os_version")
    # 设置过滤的字段
    list_filter = ("os_name","host_name",
"machine",
"os_version")
class MemoryAdmin(object):
    #设置显示的字段
    list_display = ('server','slot', 'capacity', 'speed', 'sn')
    #设置搜索的字段
    search_fields = ('slot', 'capacity', 'speed','sn')
    #设置过滤的字段
    list_filter = ('slot', 'capacity', 'speed', 'sn')

class DiskAdmin(object):
        #设置显示的字段
    list_display = ( 'server','slot', 'coreced', 'pd', 'raw')
    #设置搜索的字段
    search_fields = ( 'server','slot', 'coreced', 'pd', 'raw')
    #设置过滤的字段
    list_filter = ( 'server','slot', 'coreced', 'pd', 'raw')

class IDCAdmin(object):
    #设置显示的字段
    list_display = ('name', 'city', 'address')
    #设置搜索的字段
    search_fields = ('name', 'city', 'address')
    #设置过滤的字段
    list_filter = ('name', 'city', 'address')


class CabinetAdmin(object):
    #设置显示的字段
    list_display = ('name','cab_lever', 'idc')
    #设置搜索的字段
    search_fields = ('name','cab_lever', 'idc')
    #设置过滤的字段
    list_filter = ('name','cab_lever', 'idc')

class AssetAdmin(object):
    #设置显示的字段
    list_display = ('device_type_id','device_status_id',
     'cabinet','cabinet_order','latest_date','create_at')
    #设置搜索的字段
    search_fields = ('device_type_id','device_status_id',
     'cabinet','cabinet_order','latest_date','create_at')
    #设置过滤的字段
    list_filter = ('device_type_id','device_status_id',
     'cabinet','cabinet_order','latest_date','create_at')

# class InventoryPoolAdmin(object):
#     pass

xadmin.site.register(Server, ServerAdmin)
xadmin.site.register(Memory, MemoryAdmin)
xadmin.site.register(Disk, DiskAdmin)
xadmin.site.register(IDC, IDCAdmin)
xadmin.site.register(Cabinet, CabinetAdmin)
xadmin.site.register(Asset, AssetAdmin)
# xadmin.site.register(TreeNode, TreeNodeAdmin)
# xadmin.site.register(Tag, TagAdmin)
# xadmin.site.register(Connection, ConnectionAdmin)
# xadmin.site.register(InventoryPool, InventoryPoolAdmin)
# xadmin.site.register(Variable2Server, Variable2ServerAdmin)
# xadmin.site.register(Variable2Group, Variable2GroupAdmin)
