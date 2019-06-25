# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
systemname = (
    (str('1'),'linux'),
    (str('2'),'windows'),
    (str('3'),'other'),
)

class HostInfo(models.Model):
    ip = models.GenericIPAddressField('ip',unique=True)
    osname = models.CharField('系统名称',max_length=20,choices=systemname,blank=True,null=True)
    prartition = models.CharField("分区情况描述",max_length=200,blank=True,null=True)

    def __str__(self):
        return self.ip

class DiskUsage(models.Model):
    host = models.ForeignKey('HostInfo')
    value = models.CharField('磁盘使用率',max_length=20)
    add_time = models.DateTimeField('录入时间', auto_now=True)
