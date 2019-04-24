# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import json

from django.utils.translation import ugettext


class SendAlertReceiverHandler(object):
    name = "send_alert"

    @classmethod
    async def handle(cls, consumer, payload):
        message = payload.get("message")
        level = payload.get("level")
        if not (message and level):
            return

        # Send message to room group using the `handle_send_alert` type
        await consumer.channel_layer.group_send(consumer.shop_room_name, {
            "type": "handle_send_alert",
            "message": message,
            "level": level
        })


class SendAlertConsumerHandler(object):
    name = "handle_send_alert"

    async def handle(self, payload):
        await self.send(text_data=json.dumps({
            "command": "alert",
            "message": payload["message"],
            "level": payload["level"],
        }))


class OrderReceivedConsumerHandler(object):
    name = "handle_order_received"

    async def handle(self, payload):
        await self.send(text_data=json.dumps({
            "command": "alert",
            "message": ugettext("New order received!"),
            "level": "info"
        }))
