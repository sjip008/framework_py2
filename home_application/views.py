# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ImproperlyConfigured
import json

from home_application.models import *
from django.views.generic import TemplateView, View, ListView, DetailView
from blueking.component.shortcuts import get_client_by_request
from blueapps.account.decorators import login_exempt



# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, 'home_application/home.html')


def helloworld(request):
    return render(request, 'home_application/helloworld.html')


@csrf_exempt
def HelloBlueking(request):
    if request.POST and request.POST.get('inputid'):
        print(request.POST.get('inputid'))
        if request.POST.get('inputid') == 'Hello Blueking':
            dis = 'Congratulation！'
        else:
            dis = '请输入正确的内容：'
        return JsonResponse({'data': dis})
    return render(request, 'home_application/HelloBlueking.html')


@csrf_exempt
def addhost(request):
    if request.method == 'GET':
        return render(request, 'home_application/addhost.html')
    if request.method == 'POST':
        try:
            addinfo = HostInfo(ip=request.POST.get('ip', None),
                               osname=request.POST.get('os', None),
                               prartition=request.POST.get('part', None),
                               )
            addinfo.save()
            msg = {"msg": "data is save"}
        except Exception as e:
            msg = {"msg": "error " + e[1]}
        return JsonResponse(msg)


def quickshow(request):
    if request.method == 'GET':
        hostqueryset = HostInfo.objects.all()
        return render(request, 'home_application/quickshow.html', locals())


def api_data(request):
    fieldlist = ['id', 'ip', 'osname', 'prartition']
    qs = HostInfo.objects.all()
    prelist = [[getattr(i, x) for x in fieldlist] for i in qs]

    jsondata = {"data": prelist}
    return JsonResponse(jsondata)


class showdata(ListView):
    context_object_name = 'usedisk'
    template_name = 'home_application/showdata.html'
    model = DiskUsage


@csrf_exempt
def get_usage_data(request):
    """
    调用自主接入接口api
    """
    if request.method == 'POST':
        client = get_client_by_request(request)
        kwargs = request.body
        kwargs = json.loads(request.body)
        kwargs['bk_username'] = '314629925'
        usage = client.hsq.get_dfusage_hsq(kwargs)
        return JsonResponse(usage)
    if request.method == 'GET':
        return render(request, "home_application/get_usage_data.html")


@login_exempt
def api_disk_usage(request):
    """
    磁盘使用率API接口 api/get_dfusage_xxx
    """
    ip = request.GET.get('ip', '')
    system = request.GET.get('system', '')
    mounted = request.GET.get('disk', '')
    if ip and system and mounted:
        _data = HostInfo.objects.get(ip=ip, )

    else:
        return JsonResponse({
            "result": False,
            "data": [],
            "message": '参数不完整'
        })

    data_list = []

    disk_usages = _data.diskusage_set.all()
    disk_usage_add_time, disk_usage_value = model_data_format(disk_usages)

    data_list.append(
        {
            'ip': _data.ip,
            'system': _data.osname,
            'mounted': _data.prartition,
            'disk_usage': {
                "xAxis": disk_usage_add_time,
                "series": [
                    {
                        "name": "磁盘使用率",
                        "type": "line",
                        "data": disk_usage_value
                    }
                ]
            }
        }
    )

    return JsonResponse({
        "result": True,
        "data": data_list,
        "message": 'ok'
    })


def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value

@login_exempt
def importdata(request):
    host = HostInfo.objects.get(ip='10.0.1.80')
    for i in range(10):
        sv=DiskUsage(host=host,value='7%')
        sv.save()
        


