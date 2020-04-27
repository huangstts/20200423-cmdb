#执行文件
#!/usr/bin/env  python3
import sys,os,requests
Base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   #将server_cmdb设为基目录

sys.path.insert(0,Base_dir)     

from core.main import  main          #导入main模块

if  __name__ == "__main__":
     info=main()
     requests.post(url='http://47.98.34.58:11223/cmdb/asset/', json=info)
