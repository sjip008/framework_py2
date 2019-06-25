# -*- coding: utf-8 -*-
import logging
import datetime

from celery import task
from celery.task import periodic_task
from time import sleep
import base64
from home_application.models import DiskUsage,HostInfo
import re

hostip = HostInfo.objects.get(ip='10.0.1.80')
def base64_encode(string):
    """
    对字符串进行base64编码
    """
    return base64.b64encode(string).decode("utf-8")


from blueapps.account.models import User
from blueking.component.shortcuts import get_client_by_user

user = User.objects.get(username=u'314629925')
client = get_client_by_user(user)

script_content = base64_encode(b"df -h / | sed -e '1d' |awk '{if($5>0) print $5}'")
script_param = base64_encode(b'/')

ip_list = [{
    "bk_cloud_id": 0,
    "ip": '10.0.1.80'
}]


def fast_execute_script(client, script_content, script_param, ip_list):
    """
    快速执行脚本函数
    """
    kwargs = {
        'bk_app_code': 'hsqapp1',
        'bk_app_secret': 'a2531495-82e2-44e8-8e70-a0bfb6a0354e',
        # 'bk_token': 'a2531495-82e2-44e8-8e70-a0bfb6a0354e',
        'bk_username': u'314629925',
        'ip_list': ip_list,
        'bk_biz_id': 4,
        'script_content': script_content,
        'script_param': script_param,
        'account': 'root'

    }
    return client.job.fast_execute_script(kwargs)


FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%Y-%m-%d %H:%M:%S]")

logger = logging.getLogger('config')


def get_job_instance_log(client, job_instance_id):
    """
    对作业执行具体日志查询函数
    """

    kwargs = {
        # "bk_app_code": "hsqapp1",
        # "bk_app_secret": "a2531495-82e2-44e8-8e70-a0bfb6a0354e",
        # "bk_token": "a2531495-82e2-44e8-8e70-a0bfb6a0354e",
        "bk_biz_id": 4,
        "job_instance_id": job_instance_id,
        'bk_username':'314629925'
    }
    sleep(2)  # todo 延时2s, 快速执行脚本需要一定的时间， 后期可以用celery串行两个函数
    return client.job.get_job_instance_log(kwargs)


@task()
def get_capacity_task():
    """
    定义一个获取磁盘使用率异步任务
    """
    fast_execute_script_result = fast_execute_script(client, script_content, script_param, ip_list)
    if fast_execute_script_result['message'] == 'success':
        job_instance_id = fast_execute_script_result['data']['job_instance_id']
        get_job_instance_log_result = get_job_instance_log(client, job_instance_id)

        # 如果日志查询成功，提取内容
        if get_job_instance_log_result['message'] == 'success':
            # 匹配log_content规则
            dis = DiskUsage(host=hostip,value=get_job_instance_log_result['data'][0]['step_results'][0]['ip_logs'][0]['log_content'])
            dis.save()
            return get_job_instance_log_result
        else:
            return None




@periodic_task(run_every=datetime.timedelta(seconds=3))
def get_disk_periodic():
    """
    获取磁盘使用率周期执行定义
    """
    return  get_capacity_task.delay()

