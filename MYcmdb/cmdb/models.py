from django.db import models
from django.utils import timezone


class TreeNode(models.Model):
    node_name = models.CharField('节点名称', max_length=128)
    node_upstream = models.ForeignKey('self',verbose_name='上级节点',
                                      related_name='sub_node',
                                      on_delete=models.CASCADE,
                                      blank=True,null=True)
    class Meta:
        verbose_name = "服务树节点表"
        verbose_name_plural = verbose_name
        db_table = 'tree_node'

    def __str__(self):
        up_node = self.node_upstream.node_name if self.node_upstream else '根节点'
        return f"{up_node}-->{self.node_name}"


class Tag(models.Model):
    name = models.CharField('标签', max_length=64)
    latest_date = models.DateField(verbose_name='更新时间', default=timezone.now, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True, blank=True)

    class Meta:
        verbose_name = "标签信息表"
        verbose_name_plural = verbose_name
        db_table = 'tag'

    def __str__(self):
        return self.name

class IDC(models.Model):
    name = models.CharField(verbose_name='机房', max_length=128)
    city = models.CharField(verbose_name='城市', max_length=32)
    address = models.CharField(verbose_name='地址', max_length=256)
    latest_date = models.DateField(verbose_name='更新时间', default=timezone.now, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True, blank=True)

    class Meta:
        verbose_name_plural = '机房表'
        db_table = "idc"

    def __str__(self):
        return self.name

class Cabinet(models.Model):
    name = models.CharField(verbose_name='机柜编号', max_length=128)
    cab_lever = models.CharField(verbose_name='U 数', max_length=2)  # 机柜总共几层
    latest_date = models.DateField(verbose_name='更新时间', default=timezone.now, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True, blank=True)
    idc = models.ForeignKey('IDC', verbose_name='所属机房', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '机柜表'
        db_table = "cabinet"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        ('1', '服务器'),
        ('2', '路由器'),
        ('3', '交换机'),
        ('4', '防火墙'),
    )
    device_status_choices = (
        ('1', '上架'),
        ('2', '在线'),
        ('3', '离线'),
        ('4', '下架'),
    )

    device_type_id = models.CharField(choices=device_type_choices, max_length=1, default='1',help_text="服务器类型")
    device_status_id = models.CharField(choices=device_status_choices, max_length=1,default='1',help_text="服务器状态")

    cabinet = models.ForeignKey('Cabinet', verbose_name='机柜号', 
       max_length=30, null=True, blank=True,on_delete=models.CASCADE)
    cabinet_order = models.CharField(verbose_name='机柜中序号', max_length=30, null=True, blank=True)

    # node = models.ForeignKey('TreeNode', verbose_name='节点', null=True, blank=True,
    #                         related_name='assets',
    #                         on_delete=models.CASCADE)
    # tag = models.ManyToManyField('Tag', verbose_name='标签',related_name='assets')
    # idc = models.ForeignKey('IDC', verbose_name='IDC机房', 
    #     null=True, blank=True, on_delete=models.CASCADE)

    latest_date = models.DateField(verbose_name='更新时间', default=timezone.now, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True, blank=True )

    class Meta:
        verbose_name = "资产表"
        verbose_name_plural = verbose_name
        db_table = 'asset'

    def __str__(self):
        return "{}-{}".format(self.cabinet, self.cabinet_order)



class Server(models.Model):
    asset = models.OneToOneField(Asset, related_name='server', verbose_name="资产",
        on_delete=models.CASCADE, null=True, blank=True)
    os_name = models.CharField('操作系统', max_length=520)
    machine = models.CharField('系统架构', max_length=520)
    manager_ip = models.GenericIPAddressField(
                            verbose_name="IP地址",
                            protocol='both',
                            default='',
                            null=True, 
                            blank=True)
    connection = models.ForeignKey("Connection",
                                verbose_name="连接信息",
                                related_name="server",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    host_name = models.CharField('主机名', max_length=520)
    os_version = models.CharField('系统版本', max_length=520)
    kernel = models.CharField('内核信息', max_length=520)
    model_name = models.CharField("cpu名称", max_length=520)
    cpu_type = models.CharField("cpu类型", max_length=520)
    physical_count = models.IntegerField("cpu物理颗数",)
    cpu_cores = models.IntegerField("每颗cpu核心数",)
    latest_date = models.DateField(verbose_name='更新时间', default=timezone.now, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True, blank=True)
    class Meta:
        verbose_name_plural = "服务器表"
        db_table = "server"

    def __str__(self):
        return self.host_name




class Memory(models.Model):
    capacity = models.CharField("内存容量", max_length=100, null=True)
    slot = models.CharField("插槽", max_length=128, null=True)
    model = models.CharField("内存类型", max_length=128, null=True)
    speed = models.CharField("速率", max_length=128, null=True)
    manufacturer = models.CharField("内存厂商", max_length=128, null=True)
    sn = models.CharField("产品序列号", max_length=128, null=True)
    latest_date = models.DateField(verbose_name='更新时间', default=timezone.now, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True, blank=True)
    server = models.ForeignKey("Server",
    related_name="memory",
    verbose_name="服务器",
    default=1,
    on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "内存表"
        db_table = "memory"

    def __str__(self):
        return self.slot

class Disk(models.Model):
    coreced =models.CharField("强制磁盘容量",max_length=200,null=True)
    pd = models.CharField("接口类型",max_length=10,null=True)
    raw = models.CharField("原始磁盘容量",max_length=200,null=True)
    slot = models.CharField("插槽号",max_length=10,null=True)
    latest_date = models.DateField(verbose_name='更新时间', default=timezone.now, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True, blank=True)
    server = models.ForeignKey("Server", verbose_name="服务器",
                related_name="disk",
                default=1,
                on_delete=models.CASCADE)

    class Meta:
      verbose_name = "硬盘表"
      verbose_name_plural = verbose_name
      db_table = "disk"

    def __str__(self):
        return self.slot

class Connection(models.Model):
    """
    服务器连接信息表
    """
    user = models.CharField('ssh用户',max_length=64)
    password=models.CharField('连接密码',max_length=1024)
    port =  models.PositiveIntegerField('sshd 监听端口')
    authed = models.BooleanField(verbose_name='是否认证',default=False,help_text="是否建立了基于密钥的信任关系")

    class Meta:
      verbose_name = "服务器连接表"
      verbose_name_plural = verbose_name
      db_table = "connection"

    def __str__(self):
        return "用户:{}".format(self.user)

class InventoryPool(models.Model):
    group =models.CharField('组名',max_length=64)
    server=models.ManyToManyField('Server', verbose_name='所属服务器',related_name='inventory')
    class Meta:
      verbose_name = "Ansible资产清单"
      verbose_name_plural = verbose_name
      db_table = "inventory_pool"
 
    def __str__(self):
        return "组:{}".format(self.group)

class Variable2Group(models.Model):
    """
    变量到组的关系表
    """
    key = models.CharField("变量名", max_length=64)
    val = models.CharField("变量值", max_length=512)
    group = models.ForeignKey("InventoryPool",
                                 verbose_name="所属组",
                                 related_name="inv2vars",
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    class Meta:
        verbose_name = "Ansible 组变量表"
        verbose_name_plural = verbose_name
        db_table = "variable_group"

    def __str__(self):
        return "{}:{}={}".format(self.group.group, self.key, self.val)

class Variable2Server(models.Model):
    """
    变量到主机的关系表
    """
    key = models.CharField("变量名", max_length=64, default='')
    val = models.CharField("变量值", max_length=512, default='')
    host = models.ForeignKey("Server",
                                 verbose_name="所属主机",
                                 related_name="server2vars",
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    class Meta:
        verbose_name = "Ansible 主机变量表"
        verbose_name_plural = verbose_name
        db_table = "variable_host"

    def __str__(self):
        return "{}:{}={}".format(self.host.host_name, self.key, self.val)
