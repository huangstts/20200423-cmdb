import subprocess
class Disk():
    def __init__(self):
        self.file = "MYcmdb/R710-disk-info"
        self.cmd = "grep -v '^$' %s" % self.file
    
    def run_cmd(self, cmd):
        stat, result = subprocess.getstatusoutput(cmd)
        if not stat:
            return self.parse(result)

    def parse(self,data):
        """处理数据"""
        slot_num_li = []
        pd_type_li = []
        raw_size = []
        coerced_size = []
        disk_info = {}
        for line in data.split('\n'):
            if line.strip().startswith('Slot Number'):
                slot_num_li.append(line.strip().split(':')[-1].strip().replace(' ','_'))
            if line.strip().startswith('PD Type'):
                pd_type_li.append(line.strip().split(':')[-1].strip().replace(' ','_'))
            if line.strip().startswith('Raw Size'):
                raw_size.append(line.strip().split(':')[-1].rsplit(' ',2)[-3].strip().replace(' ','_'))
            if line.strip().startswith('Coerced Size'):
                coerced_size.append(line.strip().split(':')[-1].rsplit(' ',2)[-3].strip().replace(' ','_'))
        # print(slot_num_li,pd_type_li,raw_size)
        i = 0
        while i < len(slot_num_li):
            for x,y,z,b in zip(slot_num_li,pd_type_li,raw_size,coerced_size):
                disk_key = {'slot':'', 'pd':'', 'raw':'', 'coreced':''}
                disk_key['slot'] = x
                disk_key['pd'] = y
                disk_key['raw'] = z
                disk_key['coreced'] = b
                disk_info[x] = disk_key
                i += 1
        # print(disk_dic)
        return disk_info

    def cmd_handle(self):
        """获取R710数据接口"""
        return self.run_cmd(self.cmd)

if __name__ == '__main__':
    disk_obj = Disk()
    info = disk_obj.cmd_handle()
    print(info)