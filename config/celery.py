# coding: utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 单独脚本调用Django内容时，需配置脚本的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('conf', backend='redis://10.64.2.246:6379/2', broker='redis://10.64.2.246:6379/1')

#  CELERY_ 作为前缀，在settings中写配置
#app.config_from_object('settings')

# app 扩展配置
app.conf.update(
    result_expires=3600,

    CELERY_RESULT_SERIALIZER='json',
    CELERY_TASK_SERIALIZER = 'json'
)

# 到Django各个app下，自动发现tasks.py 任务脚本
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
