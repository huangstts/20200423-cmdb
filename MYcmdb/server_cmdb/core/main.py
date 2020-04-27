import importlib                 #导入内置模块

#导入自定义模块 conf/settings下的PLUGINS_DIC字典并定义别名为pluhins
from conf.settings import PLUGINS_DIC as plugins    

#从settings中取出数据（字典）执行主方法main()
server_info={}
def main():
    for key,val in plugins.items():
        mod_path,cls_name=val.rsplit('.',1)   #右边第一个点分割一次，切割出来函数名
        mod_obj=importlib.import_module(mod_path)       #用importlib下的import_module方法导入mod_path模块                                                         # 等价于 import plugins.class_baseinfo  
        cls=getattr(mod_obj,cls_name)     #getattr() 如果存在mob_obj 则将cls_name返回给cls    等价于 cls=Baseinfo 或cpu或Memory
        if cls_name == 'Memory':             #由于Memory需要传参数 所以判断 如果为Memory则传参
            obj=cls(debug=True)                #将debug=True参数传递给Memory()
        else:
            obj=cls()                                   #否则直接执行函数
        info=obj.cmd_handle()                    #连接cmd端口
        print(info)     
        server_info[key] = info
        
    return server_info