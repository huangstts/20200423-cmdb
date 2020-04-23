from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from cmdb.models import Asset
def index(request):
    return render(request,'index.html')

def diagram(request):
    return render(request,'diagram.html')


def page_not_found_view(request, exception=None):
    return render(request, '404.html',status=404)
def page_error(request):
    return render(request,'500.html',status=500)

from django.db.models import Count
#### 数据可视化
class DashView(View):
    def get(self, request):
        l1 = ['设备状态']
        li = []
        d1 = {}
        device_type = dict(Asset.device_type_choices)
        device_status = dict(Asset.device_status_choices)
        
        for q in device_status.keys():
            d1[q]=0
    
        for m in list(device_status.keys()):
            status_qs2 = dict(Asset.objects.filter(device_status_id=m).values_list('device_status_id').annotate(value=Count('device_status_id')))
            if not status_qs2:
                d1.pop(m)

        for s in list(device_status.keys()):
            type_qs = dict(Asset.objects.filter(device_type_id=s).values_list('device_status_id').annotate(value=Count('device_status_id')))
            type_qs1 = list(type_qs.values())
            for p in d1.keys():
                if p not in type_qs.keys():
                    type_qs1.insert(list(d1.keys()).index(p),d1[p])
                 
            type_qs1.insert(0,device_type[s])
            li.append(type_qs1)

        for x in list(device_status.keys()):
            status_qs1 = dict(Asset.objects.filter(device_status_id=x).values_list('device_status_id').annotate(value=Count('device_status_id')))
            if status_qs1:
                l1.append(device_status.get(x))
            else:
                device_status.pop(x)
                
        li.insert(0,l1)
        print(li)
        return JsonResponse(li, safe=False)


