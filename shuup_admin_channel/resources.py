# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from django.templatetags.static import static
from shuup.xtheme.resources import add_resource


def add_resources(context, content):
    request = context.get("request")
    if not request:
        return

    match = request.resolver_match
    if match and match.app_name == "shuup_admin":
        add_resource(context, "body_end", static("shuup-admin-channel.js"))
