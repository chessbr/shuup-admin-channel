# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = "shuup_admin_channel"
    label = "shuup_admin_channel"
    provides = {
        "channels_urls": [
            "shuup_admin_channel.urls:channels_urls"
        ],
        "admin_browser_config_provider": [
            "shuup_admin_channel.browser_config:AdminChannelBrowserConfigProvider"
        ],
        "admin_channel_consumer_handler": [
            "shuup_admin_channel.handlers:OrderReceivedConsumerHandler",
            "shuup_admin_channel.handlers:SendAlertConsumerHandler"
        ],
        "admin_channel_receiver_handler": [
            "shuup_admin_channel.handlers:SendAlertReceiverHandler"
        ],
        "xtheme_resource_injection": [
            "shuup_admin_channel.resources:add_resources"
        ]
    }

    def ready(self):
        # connect events
        import shuup_admin_channel.signal_handling  # noqa
