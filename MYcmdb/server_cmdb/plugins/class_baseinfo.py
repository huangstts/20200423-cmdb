import subprocess
class Baseinfo():
    def run_cmd(self,cmd):
        stat, result = subprocess.getstatusoutput(cmd)
        if not stat:
            return self.parse(result)
        else:
            return {"stat": False, "error": result}


    def parse(self,data):
        return data.strip().strip('_')


    def cmd_handle(self):
        info_base = {
        'os_name': self.run_cmd('uname -s'),
        'machine': self.run_cmd("uname -m"),
        'host_name': self.run_cmd("hostname"),
        'os_version': self.run_cmd("cat /etc/redhat-release|tr -s ' '|tr ' ' _"),
        'kernel': self.run_cmd('uname -r')
        }
        return info_base

if __name__ == '__main__':
    info=Baseinfo().cmd_handle()
    print(info)
    # return info