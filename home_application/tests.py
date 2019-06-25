# -*- coding: utf-8 -*-
# from django.test import TestCase
import sys,os
print('Python %s on %s' % (sys.version, sys.platform))
import django;
print('Django %s' % django.get_version())
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.extend(['E:\\pythonproject\\framework_py', 'D:\\JetBrains\\PyCharm\\helpers\\pycharm', 'D:\\JetBrains\\PyCharm\\helpers\\pydev'])
if 'setup' in dir(django):
    django.setup()
# Create your tests here.

from django.conf import settings

def showdef(func):
    for i in dir(func):
        if i.startswith('__'):
                pass
        else:
                print(i,type(i))
                if callable(i):
                    print(i,'can callable')
                    x = getattr(func, i)
                    x()
                if isinstance(i,str):
                    x = getattr(func, i)
                    print(x)
                print('-'*20)

showdef(settings)
