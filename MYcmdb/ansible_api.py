import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
# from cmdb.models import InverrtoryPool


class ResultCallback(CallbackBase):
    """
    重写callbackBase类的部分方法
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.task_ok = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, **kwargs):
        self.host_failed[result._host.get_name()] = result


class MyAnsiable2():
    def __init__(self, addgroup='',
                 connection='local',  # 连接方式 local 本地方式，smart ssh方式
                 remote_user=None,    # 远程用户
                 ack_pass=None,       # 提示输入密码
                 sudo=None, sudo_user=None,     ask_sudo_pass=None,
                 module_path=None,    # 模块路径，可以指定一个自定义模块的路径
                 become=None,         # 是否提权
                 become_method=None,  # 提权方式 默认 sudo 可以是 su
                 become_user=None,  # 提权后，要成为的用户，并非登录用户
                 check=False, diff=False,
                 listhosts=None, listtasks=None, listtags=None,
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None):
        self.addgroup = addgroup
        # 函数文档注释
        """
        初始化函数，定义的默认的选项值，
        在初始化的时候可以传参，以便覆盖默认选项的值
        """
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            ack_pass=ack_pass,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            syntax=syntax,
            start_at_task=start_at_task,
        )

        # 三元表达式，假如没有传递 inventory, 就使用 "localhost,"
        self.inventory = inventory if inventory else "localhost,"

        # 实例化数据解析器
        self.loader = DataLoader()

        # 实例化 资产配置对象
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)
        # self.AddInv_obj()
        # 设置密码，可以为空字典，但必须有此参数
        self.passwords = {}

        # 实例化回调插件对象
        self.results_callback = ResultCallback()

       
    def handle_group_host(self,group_hosts,run_group="default"):
        #动态添加组
        self.inv_obj.add_group(run_group)
        #添加组及其成员
        for group,hosts in group_hosts.items(): 
            self.inv_obj.add_group(group)
            #动态添加组内成员
            """
            1.可以让前端选择每个组中的部分主机
                {"group_name":["h1","h2"],...}
            """
            for host in hosts:
                self.inv_obj.add_host(host,group)
        
        #添加变量
        # handle_group_variable(group)
        
        #添加父子组关系，最终我们可执行父组
        #父组是动态添加的，不存在于数据库中
        parent_group=self.inv_obj.groups[run_group]        
        parent_group.add_child_group(self.inv_obj.groups[group])
        
         # 变量管理器
        self.variable_manager = VariableManager(self.loader, self.inv_obj)
    
    # 1.从数据库中拿到所有组及其成员
    # 2.从数据库中拿到所有组的变量和每个主机的变量
    # 3.数据处理
    #     3.1把变量和组，变量和主机的关系建立一下
    #     3.2把组和其他成员主机的关系建立一下
    # 4.把上面的数据结构存放到 redis/mangodb
    #  以上的操作作为一个模块或者一个中间件
    #  用celery每天执行一次
    #  并且考虑到，每天可能会有管理人员添加新的关系到数据库中
    #   1.支持手动更新数据到redis中 
    #   2.利用信号也可以自动触发更新数据到redis中
        # 信号就是当数据库中的某些数据更新或者新建的时候可以
        # 触发一个函数的执行，那么我们就可以在这个函数中写更新
        # 数据到redis里的逻辑代码
    # 5.从redis中获取到资产信息的数据
    #   用 Inventory 把这些组和主机添加进来，并且添加其对应的变量
    # 6.动态的添加一个临时组（run_group）
    # 7.把前端传过来的所有主机添加到这个动态添加的组中（run_group）
    # 8.执行 run 方法的时候，传递目标组为 run_group
    
    def handle_group_variable(self,group,key,val):
        #从数据库中取出变量
        #[{"group_name":{"key":"val","key2":"val2"}},{}
        #动态给组添加变量
        group_obj = self.inv_obj.groups[group]
        group_obj.set_variable(key,val)
        pass

    # def AddInv_obj(self):
    #     # 动态添加组
    #     # print(self.addgroup)
    #     for i in self.addgroup:
    #         self.inv_obj.add_group(i)
    #         host_list = InverrtoryPool.objects.filter(group=i)[0]
    #         for j in host_list.server.values():
    #             self.inv_obj.add_host(j['manager_ip'], i)

        # # 动态给组添加变量
        # group_obj = self.inv_obj.groups['nginx']
        # group_obj.set_variable('name', 'shark')

    def run(self, hosts='localhost', gether_facts="no", module="ping", args=''):
        play_source = dict(
            name="Ad-hoc",
            hosts=hosts,
            gather_facts=gether_facts,
            tasks=[
                # 这里每个 task 就是这个列表中的一个元素，格式是嵌套的字典
                # 也可以作为参数传递过来，这里就简单化了。
                {"action": {"module": module, "args": args}},
            ])

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback)

            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self, playbooks):
        from ansible.executor.playbook_executor import PlaybookExecutor

        playbook = PlaybookExecutor(playbooks=playbooks,  # 注意这里是一个列表
                                    inventory=self.inv_obj,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=self.passwords)

        # 使用回调函数
        playbook._tqm._stdout_callback = self.results_callback

        result = playbook.run()

    def get_result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

        # print(self.results_callback.host_ok)
        for host, result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result

        # 最终打印结果，并且使用 JSON 继续格式化
        # return json.dumps(result_raw, indent=4)
        print(result_raw)

if __name__ == "__main__":
    group="nginx"
    hosts=['10.0.122.38']
    target="default"
    # 使用自己的 资产配置文件，并使用 ssh 的远程连接方式
    ansible2 = MyAnsiable2(inventory='localhost,', 
                           connection='smart',
                           remote_user="oyzx")
    ansible2.handle_group_host(group=group,hosts=hosts,run_group=target)
    # 执行自定义任务，执行对象是 nginx 组
    ansible2.run(hosts= target, module="shell", args='ls /tmp')

    # 打印结果
    ansible2.get_result()
