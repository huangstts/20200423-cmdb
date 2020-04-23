from rest_framework import serializers
from users.models import UsersProfile
# 自定义字段的序列化，更为灵活
class UsersSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=True, help_text="用户主键"
    )
    username = serializers.CharField(
        required=True,  max_length=150)
    email = serializers.EmailField(
        required=False, allow_null=True )
    password = serializers.CharField(
        required=True, max_length=128)

    last_login = serializers.DateTimeField(
        required=False, allow_null=True)

    avatar = serializers.ImageField(max_length=128)




from rest_framework import serializers
from cmdb.models import Asset, Disk, Server, Memory,IDC,Cabinet,Tag,TreeNode
#创建基于 Model 的序列化类
class DiskSerializer2(serializers.ModelSerializer):
    # 这里可以实现在 硬盘信息中含有对应服务器的详细信息
    class Meta:
        model = Disk
        fields = '__all__'
class MemorySerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Memory
        fields = "__all__"

class ServerSerializer(serializers.ModelSerializer):
    disk = DiskSerializer2(many=True)  #反向访问多对一
    memory = MemorySerializer2(many=True)  #反向访问多对一

    # disk = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True,  #一对一关系
    #     view_name='disks'
    # )
    class Meta:
        model = Server
        fields = ['id','asset',
                'os_name',
                'machine',
                'host_name',
                'os_version',
                'kernel',
                'model_name',
                'cpu_type',
                'physical_count',
                'cpu_cores','disk','memory']


        
class DiskSerializer(serializers.ModelSerializer):
    # 这里可以实现在 硬盘信息中含有对应服务器的详细信息
    server = ServerSerializer()   #正向访问一对多
    class Meta:
        model = Disk
        fields = ['coreced',
                'pd',
                'raw',
                'slot',
                'server']

class MemorySerializer(serializers.ModelSerializer):
    server = ServerSerializer()
    class Meta:
        model = Memory
        fields = "__all__"



class IDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = "__all__"


class CabinetSerializer(serializers.ModelSerializer):
    idc = IDCSerializer()
    class Meta:
        model = Cabinet
        fields = "__all__"

class subsubTreeNodeSerializer(serializers.ModelSerializer):
    sub_node = serializers.SerializerMethodField()
    class Meta:
        model = TreeNode
        fields = "__all__"
    def get_sub_node(self,obj):
        return []
    
        
class subTreeNodeSerializer(serializers.ModelSerializer):
    sub_node = subsubTreeNodeSerializer(many=True)
    class Meta:
        model = TreeNode
        fields = "__all__"

class TreeNodeSerializer(serializers.ModelSerializer):
    sub_node = subTreeNodeSerializer(many=True)
    class Meta:
        model = TreeNode
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    node= TreeNodeSerializer()
    tag= TagSerializer()
    cabinet = CabinetSerializer()
    device_type = serializers.SerializerMethodField()
    device_status = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = "__all__"

    def get_device_type(self,obj):
        return obj.get_device_type_id_display()
    def get_device_status(self,obj):
        return obj.get_device_status_id_display()
                  