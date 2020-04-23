import  os, sys
# 获取到项目的根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 把项目的根目录放到 sys.path 中
sys.path.insert(0, PROJECT_ROOT)

# 设置环境变量
os.environ["DJANGO_SETTINGS_MODULE"] = 'gitblogsite.settings'
import django
django.setup()

if __name__ == "__main__":
    inv_dic = {"all": {"hosts": []}, "_meta": {"hostvars": {}}}

    from cmdb.models import InventoryPool, Server
    invs = InventoryPool.objects.values(
        'group', 'inv2vars__key', 'inv2vars__val',
        'server__manager_ip'
    )
    import json
    # print(json.dumps(list(invs),indent=4))
    print("*" * 20)
    for item in invs:
        if item['inv2vars__key']:
            inv_dic.setdefault(item['group'], {"vars": {}}
                              )["vars"].update({item['inv2vars__key']:item['inv2vars__val']})
            inv_dic[item['group']].setdefault('hosts', []).append(item['server__manager_ip'])
        else:
            inv_dic.setdefault(item['group'],{"hosts": []}
                              )["hosts"].append(item['server__manager_ip'])

    # print(json.dumps(inv_dic,indent=4))

    qst_servers = Server.objects.values(
        "host_name",
        "manager_ip",
        "server2vars__key",
        "server2vars__val",
        )
    print(json.dumps(list(qst_servers),indent=4))

    for server in qst_servers:
        # 添加所以的主机到 all组中
        # {"all": {
        #     "hosts": ["app1.server",
        #               ...
        #               ]
        #      }
        # }
        inv_dic["all"]["hosts"].append(server["host_name"])
        if server["server2vars__key"]:
            key = server["server2vars__key"]
            val = server["server2vars__val"]
            inv_dic["_meta"]["hostvars"].setdefault(server["manager_ip"], {}).update({key:val})
    print(json.dumps(inv_dic,indent=4))