import subprocess
class Memory():
    # def __init__(self,debug):
    #     self.file = 'MYcmdb/mem_info'
    #     if debug:
    #         self.cmd = "grep -v '^$' %s" % self.file
    #     else:
    #         self.cmd = "dmidecode -q -t 17|grep -v '^$' "
    #     self.debug = debug


    def __init__(self,debug):
        
        self.cmd = "dmidecode -q -t 17|grep -v '^$' "
        self.debug = debug

    def run_cmd(self, cmd):
        print(cmd)
        stat, result = subprocess.getstatusoutput(cmd)
        print(stat,result)
        if not stat:
            return self.parse(result)


    def parse(self, data):
        info_mem = {}
        key_map = {
            'Size': 'capacity',
            'Manufacturer': 'manufacturer',
            'Type': 'model',
            'Locator': 'slot',
            'Serial Number': 'sn',
            'Speed': 'speed',
        }
        memory_list = [ mem for mem in data.split('Memory Device') if mem]

        for item in memory_list:
            single_slot = {}

            for line in item.splitlines():
                line = line.strip()
                if len(line.split(':')) == 2:
                    key, val = line.split(':')
                    key,val = key.strip(), val.strip()

                    if key in key_map:
                        single_slot[key_map[key]] = val
            # print(single_slot)
            info_mem[single_slot["slot"]] = single_slot
        return info_mem

    def cmd_handle(self):
        """获取R710数据接口"""
        return self.run_cmd(self.cmd)


if __name__ == '__main__':
    mem_obj = Memory(debug=False)
    info = mem_obj.cmd_handle()
    print(info)
    # return info

# import subprocess
# def run_cmd(cmd):
#     stat,result=subprocess.getstatusoutput(cmd)
#     if not stat:
#         return parse(result)
    
# def parse(data):
#     if data.endswith('_'):
#         data=data[:-1]
#     elif data.startswith('_'):
#         data=data[1:]
#     return data

# def get_mem():
#         global capacity,slot,model,speed,manufacturer,sn
#         capacity=run_cmd(' grep  "Size" ./task/oyzx/info作业/cpuinfo.txt|tr -d [:blank:]|grep "^[S]"|cut -d: -f2|tr "\n" "," ')[:-1].split(',')
#         slot=run_cmd(' grep  "Locator" ./task/oyzx/info作业/cpuinfo.txt|tr -d [:blank:]|grep "^[L]"|cut -d: -f2|tr "\n" "," ')[:-1].split(',')
#         model=run_cmd(' grep  "DDR3" ./task/oyzx/info作业/cpuinfo.txt|tr -d [:blank:]|cut -d: -f2|cut -d: -f2|tr "\n" "," ')[:-1].split(',')
#         speed=run_cmd(' grep  "Speed" ./task/oyzx/info作业/cpuinfo.txt|tr -d [:blank:]|grep "^[S]"|cut -d: -f2|tr "\n" "," ')[:-1].split(',')
#         manufacturer=run_cmd(' grep  "Manufacturer" ./task/oyzx/info作业/cpuinfo.txt|tr -d [:blank:]|cut -d: -f2|tr "\n" "," ')[:-1].split(',')
#         sn=run_cmd(' grep  "Serial" ./task/oyzx/info作业/cpuinfo.txt|tr -d [:blank:]|cut -d: -f2|tr "\n" "," ')[:-1].split(',')
        

# # get_mem()