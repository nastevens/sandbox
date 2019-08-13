// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

//! Asynchronous MQTT client interactions.

use futures::unsync::oneshot;
use mqtt_zero::packet::MqttPacket;

pub enum ClientCommand {
    Connect,
    GetStatus(oneshot::Sender<ClientStatus>),
    AddSubscriber(Vec<String>, oneshot::Sender<()>),
    AddPublisher(String, oneshot::Sender<()>),
    Disconnect,
}

enum ClientEvent {
    ConnectionEstablished,
    ConnectionLost,
}

enum ProcessingSinkItem<T> {
    Command(T),
    Event(ClientEvent),
    PacketIn(MqttPacket),
}

enum ProcessingStreamItem {
    Event(ClientEvent),
    PacketOut(MqttPacket),
}

pub enum ClientStatus {
    Connected,
    Retrying,
    Disconnected,
}


pub mod client;
pub mod connect;
pub mod ping;
pub mod process;
pub mod publish;
