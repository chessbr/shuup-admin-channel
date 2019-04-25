# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from django.templatetags.static import static
from shuup.utils.importing import cached_load
from shuup.xtheme.resources import add_resource, InlineScriptResource


class DefaultSettingsProvider(object):
    @classmethod
    def get_configs(cls, request, context):
        return {
            "connectOnLoad": True
        }


def add_resources(context, content):
    request = context.get("request")
    if not request:
        return

    match = request.resolver_match
    if match and match.app_name == "shuup_admin":
        settings_provider = cached_load("SHUUP_ADMIN_CHANNEL_SETTINGS_PROVIDER")
        add_resource(
            context,
            "body_end",
            InlineScriptResource.from_vars("ShuupAdminChannelConfig", settings_provider.get_configs(request, context))
        )
        add_resource(context, "body_end", static("shuup-admin-channel.js"))
