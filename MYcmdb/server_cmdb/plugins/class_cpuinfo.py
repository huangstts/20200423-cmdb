import subprocess

class cpu():
    def run_cmd(self,cmd):
        """执行命令，并返回结果"""
        stat, result = subprocess.getstatusoutput(cmd)
        if not stat:
            return self.parse(result)
        else:
            return {"stat": False, "error": result}


    def parse(self,data):
        """处理数据"""
        return data.strip().strip('_')


    def cmd_handle(self):
        """获取数据的接口"""
        # 定义获取CPU 信息的命令
        cmd_cpu_name = "grep 'model name' /proc/cpuinfo | uniq |cut -d: -f2|tr ' ' '_'"
        cmd_cpu_type = "uname -p"
        cmd_cpu_count = "grep 'physical id' /proc/cpuinfo | sort -u | wc -l"
        cmd_cpu_cores = "grep 'cpu cores' /proc/cpuinfo | uniq |cut -d: -f2"

        cpu_info = {
            'model_name': self.run_cmd(cmd_cpu_name),
            'cpu_type': self.run_cmd(cmd_cpu_type),
            'physical_count': int(self.run_cmd(cmd_cpu_count).strip()),
            'cpu_cores': int(self.run_cmd(cmd_cpu_cores).strip())
        }
        return cpu_info

if __name__ == "__main__":
    get_cpu=cpu().cmd_handle()
    # print(get_cpu)
    # return get_cpu