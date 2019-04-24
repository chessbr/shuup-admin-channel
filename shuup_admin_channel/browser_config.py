# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from shuup.admin.browser_config import BaseBrowserConfigProvider
from shuup.admin.shop_provider import get_shop


class AdminChannelBrowserConfigProvider(BaseBrowserConfigProvider):
    @classmethod
    def get_gettings(cls, request, **kwargs):
        if not request.user.is_authenticated():
            return {}
        if not (request.user.is_staff or request.user.is_superuser):
            return {}

        return {
            "adminChannelUrl": "/ws/admin/{}/".format(get_shop(request).pk)
        }
