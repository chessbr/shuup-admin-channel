# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from channels import DEFAULT_CHANNEL_LAYER
from django.conf import settings
from shuup.core.order_creator.signals import order_creator_finished
from shuup_admin_channel.utils import get_room_name_for_shop


def send_order_received_message(order, **kwargs):
    """
    Send message to users that a new order is received

    TODO: Put these on a queue and group messages so when
    a lot of orders is place inside a minute this won't flood users.
    """
    payload = dict(
        type="handle_order_received",      # this will be called in the consumer handlers
        order_id=order.pk,
        customer_name=order.customer.name,
        customer_email=order.email,
        customer_phone=order.phone,
        order_total=order.taxful_total_price.as_rounded().value
    )
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer(settings.SHUUP_ADMIN_CHANNEL_LAYER or DEFAULT_CHANNEL_LAYER)
    from asgiref.sync import async_to_sync
    async_to_sync(channel_layer.group_send)(get_room_name_for_shop(order.shop.pk), payload)


if settings.SHUUP_ADMIN_CHANNEL_ORDER_RECEIVED_ENABLED:
    order_creator_finished.connect(
        send_order_received_message,
        dispatch_uid="channel_send_order_received_message"
    )
