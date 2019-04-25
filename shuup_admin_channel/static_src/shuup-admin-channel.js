/**
 * This file is part of Shuup Admin Channel.
 *
 * Copyright (c) 2019, Christian Hess. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import EventEmitter from "event-emitter";

// The base object to be used in JS to handle channels
const ShuupAdminChannel = {
    socket: null,
    events: EventEmitter(),
    connect() {
        const that = this;
        const channelEndpoint = window.ShuupAdminConfig.settings.adminChannelUrl;
        if (channelEndpoint) {
            this.socket = new WebSocket(`ws://${window.location.host}${channelEndpoint}`);
            this.socket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                that.onReceive(data);
            };
            this.socket.onclose = function(e) {
                console.error("Channel socket closed unexpectedly");
            };
        }
    },
    send(payload) {
        this.socket.send(JSON.stringify(payload));
    },
    onReceive(payload) {
        this.events.emit("received", payload);
    }
};
if (window.ShuupAdminChannelConfig.connectOnLoad) {
    ShuupAdminChannel.connect();
}
// expose to the world
window.ShuupAdminChannel = ShuupAdminChannel;

// Listen for 'alert' command messages
ShuupAdminChannel.events.on("received", (payload) => {
    if (payload.command === "alert") {
        Messages.enqueue({
            tags: payload.level,
            text: payload.message
        });
    }
});
