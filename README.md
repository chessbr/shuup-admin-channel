# Shuup Admin Channel

Adds a generic and extendable channel to Admin module using [Shuup Channels](https://github.com/chessbr/shuup-channels).

This adds an optional consumer that will warn logged staff users when a new order is created through a notification, without the need of a page reload.

You can also create your own custom admin consumer and plug it in this channel.

1. Install `pip install shuup-admin-channel`
2. Add `shuup-admin-channel` to your `INSTALLED_APPS` settings
3. Profit! This will make Shuup load the scripts on each admin page load and connect with the Admin channel.

## How it works

This addon will provide a websocket consumer to Django Channels on the `ws://HOST/ws/admin/(?P<shop_id>\d+)/` URL pattern.

You must connect to it using the shop ID you want to receive Admin related messages. This addon already provides a JS lib to connect and listen and send messages to the channel.

XTheme resource injection is used to append the small lib to each Shuup Admin request. If you don't want that to be injected, you must blacklist the `"shuup_admin_channel.resources:add_resources"` provide entry in your settings ([see how to do that here](https://shuup.readthedocs.io/en/latest/ref/provides.html#blacklisting-provides).)

### Listening channel messages

To listen to Admin channel, do the following:

```js
// Listen for 'alert' command messages
ShuupAdminChannel.events.on("received", (payload) => {
    if (payload.command === "alert") {
        Messages.enqueue({
            tags: payload.level,
            text: payload.message
        });
    }
});
```

The `payload` is a JSON object sent by the channel. `payload.command` will contain the command sent from the channel and you can check that for custom commands.

### Sending messages

To send messages to the channel using JavaScript, you can do the following:

```js
ShuupAdminChannel.send({
    handler: "send_alert",
    message: "Hello staff users!",
    level: "info"
});
```

This will send an info message to all logged staff users. `handler` is the existing the consumer handler. If no handler with that name exists, nothing will be executed.

### Extending Consumers

It is possible to extend the current Admin channel to receive and handle all sort of messages from the frontend (JavaScript) and make it fit to your project needs.

You first must understand Django Channels to understand our handlers.

To make it simple: we basically have two types of messages:

- Those sent from JavaScript to a Consumer
- Those sent from the backend to be broadcasted to all consumers (or a set of them)

Imagine that you are a staff user and want to send a message to all other staff users (like an internal message). You then send a websocket message to be broadcasted and here we cover those 2 possible messages listed above.

1. Staff user send a message to the channel
2. The channel received the message and retransmit to all connected users

Now imagine you want a report that takes some time to complete but you don't want to keep the page loading for a long time. You can write a consumer to handle this message and send a message back to the user when the report is completed. This won't need to distribute the message to other consumers, you just must implement a receiver handler.

All kinds of possibilities can be created, just use your imagination :)

### Handling messages from the socket
If you want to handle a message that came from the socket (from JS for example), you must implement a Receiver Handler object and add it to the `admin_channel_receiver_handler` provide key.


```py
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
```

This receiver handler will receive messages that contains `handler: "send_alert"` in the payload.

On this example, the andler will check for other payload values and if all of expected parameters are valid, it will broadcast a message to all consumers of the Admin Channel where the handler name should be `handle_send_alert`. It is basically a message broadcaster, it receives a message and retransmit to all consumers. It could just return something to the user directly but on this example we are passing that to other consumers.

### Handling messages received from other consumers

In cases like above where a consumer wants to broadcast messages to all consumers, you want to add handlers to behave to those messages. For those, you must implement a Consumer Handler object and add it to `admin_channel_consumer_handler` provides key.

```py
class OrderReceivedConsumerHandler(object):
    name = "handle_order_received"

    async def handle(self, payload):
        await self.send(text_data=json.dumps({
            "command": "alert",
            "message": ugettext("New order received!"),
            "level": "info"
        }))

```

On this example, we are handling messages that were sent by the system, other consumer of anywhere in our python code which passed the type `handle_order_received`. This particular one is sent when a new order by a Django Signal.

Each user is connected to a consumer and all them will receive this same message.

For examples of handlers and consumers, check [`handlers.py`](./shuup_admin_channel/handlers.py).

### Room names

Admin Channel adds each user (consumer) to 3 rooms:

- A shop room, which contains all staff users from that shop.
- A global room, which contains all staff users from all shops.
- A user room, which contains only that specific user.

When sending messages to consumers you can select one of those rooms to reach the desired user group.

## Settings

- `SHUUP_ADMIN_CHANNEL_ORDER_RECEIVED_ENABLED` - Enable/disable the new order received notification
- `SHUUP_ADMIN_CHANNEL_LAYER` - The name of the channel layer to use while sending messages
- `SHUUP_ADMIN_CHANNEL_SETTINGS_PROVIDER` - The object that will provide configuration to the admin channel.

## Features

- Add notifications to warn users about new orders received
- Add websocket command to dispatch a notification to all logged staff users through JavaScript
- Add a way of exentending the channel

# Copyright

Copyright (C) 2019 by Christian Hess

# License

MIT
