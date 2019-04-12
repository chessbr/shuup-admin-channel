# -*- coding: utf-8 -*-
# This file is part of Shuup Admin Channel
#
# Copyright (c) 2019, Christian Hess. All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


def get_room_name_for_shop(shop_id):
    return "shuup_admin__shop__{}".format(shop_id)


def get_room_name_for_user(user_id):
    return "shuup_admin__user__{}".format(user_id)


def get_global_room_name():
    return "shuup_admin"
