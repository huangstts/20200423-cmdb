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
    from cmdb.models import InventoryPool
    inv_dic = {}
    invs = InventoryPool.objects.values(
        'group', 'inv2vars__key', 'inv2vars__val',
        'server__manager_ip'
    )
    import json
    print(json.dumps(list(invs),indent=4))
    print("*" * 40)
    for item in invs:
        if item['inv2vars__key']:
            inv_dic.setdefault(item['group'], {"vars": {}}
                              )["vars"].update({item['inv2vars__key']:item['inv2vars__val']})
            inv_dic[item['group']].setdefault('hosts', []).append(item['server__manager_ip'])
        else:
            inv_dic.setdefault(item['group'],{"hosts": []}
                              )["hosts"].append(item['server__manager_ip'])

    print(json.dumps(inv_dic,indent=4))


    