# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

#: Set the channel layer to use when sending messages
#: Keep None to use Django Channels' default
SHUUP_ADMIN_CHANNEL_LAYER = None

#: Indicates whether the order received handler is enabled in JavaScript
#: It is enabled by default and
SHUUP_ADMIN_CHANNEL_ORDER_RECEIVED_ENABLED = True

#: Indicates the object that will provide settings to the Admin Channel websocket
SHUUP_ADMIN_CHANNEL_SETTINGS_PROVIDER = "shuup_admin_channel.resources:DefaultSettingsProvider"
