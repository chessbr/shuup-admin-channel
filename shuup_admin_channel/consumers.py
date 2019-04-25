# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import json
import types

from channels.generic.websocket import AsyncWebsocketConsumer
from shuup.apps.provides import get_provide_objects
from shuup.core.models import Shop
from shuup_admin_channel.utils import (
    get_global_room_name, get_room_name_for_shop, get_room_name_for_user
)


class AdminConsumer(AsyncWebsocketConsumer):
    shop_room_name = None
    global_room_name = None
    user_room_name = None

    def __init__(self, *args, **kwargs):
        """
        Initialize the Admin Consumer
        Add message handlers dynamically to this instance.

        Consumer handler must be a class on the following format:
        ```
            class MyAdminConsumerHandler(object):
                name = "handle_my_message"
                def handle(self, payload):
                    do_something(payload)
        ```

        """
        super().__init__(*args, **kwargs)

        # get all the reserver methods and properties of this class
        reserved_names = dir(self)

        for consumer_handler in get_provide_objects("admin_channel_consumer_handler"):
            # do not allow overriding reserved names
            if consumer_handler.name not in reserved_names:
                # bind the method to 'self'
                handle_method = types.MethodType(consumer_handler.handle, self)
                setattr(self, consumer_handler.name, handle_method)

    async def connect(self):
        shop_id = self.scope["url_route"]["kwargs"]["shop_id"]
        self.user = self.scope.get("user")
        self.shop = Shop.objects.filter(pk=shop_id).first()

        # users that are not identified, can't connect
        if not self.shop:
            return self.close(code=404)
        if not self.user:
            return self.close(code=401)
        # users that are not staff or superusers, can't connect
        elif not ((self.user.is_staff and self.user in self.shop.staff_members.all()) or self.user.is_superuser):
            return self.close(code=403)

        # add this user to 3 rooms:
        # 1) shop room - to receive messages related to the shop
        # 2) global room - to receive messages from the platform as a whole
        # 3) solo room - to receive messages alone

        self.shop_room_name = get_room_name_for_shop(self.shop.pk)
        self.global_room_name = get_global_room_name()
        self.user_room_name = get_room_name_for_user(self.user.pk)

        # 1) add this user to the shop room
        await self.channel_layer.group_add(self.shop_room_name, self.channel_name)
        # 2) add this user to global channel
        await self.channel_layer.group_add(self.global_room_name, self.channel_name)
        # 3) add this user to solo channel to receive private messages
        await self.channel_layer.group_add(self.user_room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.shop_room_name, self.channel_name)
        await self.channel_layer.group_discard(self.global_room_name, self.channel_name)
        await self.channel_layer.group_discard(self.user_room_name, self.channel_name)

    async def receive(self, text_data):
        """
        Received a message from the socket.
        Go through all receiver handlers and execute those which handles the message
        """
        payload = json.loads(text_data)
        handler = payload.get("handler")

        for receiver_handler in get_provide_objects("admin_channel_receiver_handler"):
            if receiver_handler.name == handler:
                # do not allow using reserved names
                await receiver_handler.handle(self, payload)
