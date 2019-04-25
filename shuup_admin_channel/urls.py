# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from django.conf.urls import url
from shuup_admin_channel.consumers import AdminConsumer

channels_urls = [
    url(r"^ws/admin/(?P<shop_id>\d+)/$", AdminConsumer)
]
