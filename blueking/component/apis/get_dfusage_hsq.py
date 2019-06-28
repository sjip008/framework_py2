# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsGetDfusageHsq(object):
    """Collections of get_dfusage_bay1 APIS"""

    def __init__(self, client):
        self.client = client
        self.get_dfusage_hsq = ComponentAPI(
            client=self.client, method='GET',
            #path='/api/c/hsq-api/api/get_dfusage_hsq/',
            path='/api/c/self-service-api/api/c/hsq-api/api/get_dfusage_hsq/',
            description=u'获取指定磁盤容量'
        )
