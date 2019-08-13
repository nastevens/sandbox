// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use std::collections::VecDeque;
use std::path::PathBuf;

use futures::{Async, Future, Poll, Stream, Sink, StartSend, AsyncSink};
use futures::stream;
use futures::task::{self, Task};
use futures::unsync::mpsc::Sender;
use mqtt_zero::QoS;
use mqtt_zero::packet::{ConnectPacket, KeepAlive, ConnAckPacket, MqttPacket};
use mqtt_zero::parse::ClientIdentifier;

use error::MqttError;
use stream::spsc;

use super::{ProcessingStreamItem, ProcessingSinkItem};

pub struct ConnectOptions {
    pub broker: String,
    pub keep_alive: Option<u16>,
    pub clean_session: bool,
    pub client_id: Option<String>,
    pub username: Option<String>,
    pub password: Option<String>,
    pub reconnect: Option<u16>,
    pub will: Option<(String, String)>,
    pub will_qos: QoS,
    pub will_retain: bool,
    pub pub_q_len: u16,
    pub sub_q_len: u16,
    pub queue_timeout: u16,
    pub ca: Option<PathBuf>,
    pub client_cert: Option<(PathBuf, PathBuf)>,
}

enum ConnectStreamCommand {
    SetOptions(ConnectOptions),
    Disconnect,
}

/// Generates CONNECT, DISCONNECT packets, consumes CONNACK packets. Manages a command
/// queue for allowing re-connects and disconnects.
struct ConnectStream {
    output: spsc::SpscQueue<ProcessingStreamItem>,
    state: Box<Stream<Item=ProcessingStreamItem, Error=MqttError>>,
}

impl ConnectStream {
    pub fn new() -> ConnectStream {
        ConnectStream {
            output: spsc::channel(16),
            state: Box::new(stream::empty()),
        }
    }
}

impl Stream for ConnectStream {
    type Item = ProcessingStreamItem;
    type Error = MqttError;

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        // Poll against local packet stream as well as against ???
        // Need to poll 
        Ok(Async::NotReady)
        // self.output.poll()
    }
}

impl Sink for ConnectStream {
    type SinkItem = ProcessingSinkItem<ConnectStreamCommand>;
    type SinkError = MqttError;

    fn start_send(&mut self, item: Self::SinkItem) -> StartSend<Self::SinkItem, Self::SinkError> {
        match item {
            ProcessingSinkItem::Command(c) => {
            }
            ProcessingSinkItem::Event(e) => {
            }
            ProcessingSinkItem::PacketIn(p) => {
            }
        }
        Ok(AsyncSink::Ready)
    }

    fn poll_complete(&mut self) -> Poll<(), Self::SinkError> {
        Ok(Async::Ready(()))
    }
}

struct ConnectStreamState {
    connect_sent: bool,
    connact_recv: bool,
    stream: (),
}

impl Stream for ConnectStreamState {
    type Item = ProcessingStreamItem;
    type Error = MqttError;

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        Ok(Async::NotReady)
    }
}

enum GlobalEvent {
    StreamEstablished,
    StreamLost,
    FatalError,
    Disconnect,
}

enum ConnectEvent {
    StreamEstablished,
    StreamLost,
    Disconnect,
    ConnAckReceived(ConnAckPacket),
    TimerExpired,
}

enum GlobalResponse {
    None,
    GlobalEvent(GlobalEvent),
    PacketOut(MqttPacket),
    Both(GlobalEvent, MqttPacket),
}

// impl From<GlobalEvent> for ConnectEvent {
//     fn from(val: GlobalEvent) -> ConnectEvent {
//         match val {
//             GlobalEvent::StreamEstablished => ConnectEvent::StreamEstablished,
//             GlobalEvent::StreamLost => ConnectEvent::StreamLost,
//             GlobalEvent::Disconnect => ConnectEvent::Disconnect,
//         }
//     }
// }

struct ConnectStateCommon {
    clean_session: bool,
}

trait ConnectStateTrait {
    /// Get the next transition. If `self` is returned, no transitions are run.
    fn next(self) -> ConnectState;

    /// Optional action executed when a new input is received.
    fn input(self, event: ConnectEvent) -> (Option<MqttPacket>, Option<ConnectEvent>) {
        (None, None)
    }

    /// Optional action executed when entering a state.
    fn enter(&mut self) -> (Option<MqttPacket>, Option<ConnectEvent>) {
        (None, None)
    }

    /// Optional action executed when exiting a state.
    fn exit(&mut self) -> (Option<MqttPacket>, Option<ConnectEvent>) {
        (None, None)
    }
}

// This allows us to return a stack-allocated, static sized type instead of a
// Box, saving time for allocations. This still incurs a really small
// performance hit for the vtable lookup.
enum ConnectState {
    NoSession(NoSession),
    SendConnect(SendConnect),
    ConnAckError,
    Sleep,
    Connected,
    DisconnectedSession,
    SendDisconnect,
    Done,
}

struct NoSession;

impl From<NoSession> for ConnectState {
    fn from(val: NoSession) -> ConnectState {
        ConnectState::NoSession(val)
    }
}

impl ConnectStateTrait for NoSession {
    fn input(self, event: ConnectEvent) -> (Option<MqttPacket>, Option<ConnectEvent>) {
        use self::ConnectEvent::*;
        match event {
            StreamEstablished => no_output(SendConnect),
            Disconnect => no_output(ConnectState::Done),
            _ => no_output(self),
        }
    }
}

struct SendConnect;

impl From<SendConnect> for ConnectState {
    fn from(val: SendConnect) -> ConnectState {
        ConnectState::SendConnect(val)
    }
}

impl ConnectStateTrait for SendConnect {
    fn input(self, event: ConnectEvent) -> (ConnectState, Option<MqttPacket>, Option<ConnectEvent>) {
        use self::ConnectEvent::*;
        match event {
            _ => no_output(self),
        }
    }

    fn enter(&mut self) -> (Option<MqttPacket>, Option<ConnectEvent>) {
        let client_id = ClientIdentifier::new("foo").unwrap();
        let keep_alive = KeepAlive::Disabled;
        (Some(ConnectPacket::new(client_id, keep_alive).into()), None)
    }
}
