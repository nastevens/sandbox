// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use std::mem;

use futures::{Async, BoxFuture, Future, IntoFuture, Poll, Sink, Stream, future};
use futures::stream::MergedItem;
use futures::unsync::{mpsc, oneshot};

use reconnect::Connector;
use client::ClientCommand;
use error::MqttError;
use mqtt_zero::packet::MqttPacket;

pub struct ClientProcessOptions {
    reconnect_retries: usize,
}

/// Background process to an MqttClient acting as traffic director for incoming
/// and outgoing messages. Must be on the same thread as the MqttClient.
pub struct ClientProcess<C: Connector> {
    connector: C,
    command_rx: mpsc::Receiver<ClientCommand>,
    state: ClientState<C::Item, C::Future>,
    future: BoxFuture<(), ()>,
}

enum ProcessItem {
    PacketIn(MqttPacket),
    PacketOut(MqttPacket),
    Command(ClientCommand),
}

impl<C: Connector + 'static> ClientProcess<C> {
    pub fn new(mut connector: C, rx: mpsc::Receiver<ClientCommand>) -> ClientProcess<C> {
        ClientProcess {
            future: Self::do_it(&mut connector),
            connector: connector,
            command_rx: rx,
            state: ClientState::New,
        }
    }

    fn dispatch_command(&mut self,
                        command: ClientCommand)
                        -> BoxFuture<(), <Self as Future>::Error>
    {
        match command {
            ClientCommand::Connect => {
            },
            ClientCommand::GetStatus(_reply) => {
            }
            ClientCommand::Disconnect => {
            }
            _ => unimplemented!(),

        }
        future::ok(()).boxed()
    }

    fn dispatch_packet(&mut self,
                       packet: MqttPacket)
                       -> BoxFuture<(), <Self as Future>::Error>
    {
        match packet {
            MqttPacket::ConnAck(_connack) => {
            }
            _ => unimplemented!(),
        }
        future::ok(()).boxed()
    }

    fn do_it(connector: &mut C) -> BoxFuture<(), ()> {
        connector
            .connect()
            .map_err(|_| ())
            .and_then(|stream| Ok(()))
            .boxed()
    }
}

fn with_shutdown<S>(network_rx: S, shutdown: oneshot::Receiver<()>) -> Box<Future<Item=(), Error=()>>
    where S: Stream<Item=MqttPacket, Error=MqttError> + 'static
{

    let shutdown_stream = shutdown.map_err(|_| MqttError::Cancelled).into_stream();
    Box::new(network_rx.merge(shutdown_stream).for_each(|message| {
        match message {
            MergedItem::First(packet) => {
            }
            MergedItem::Second(()) => {
            }
            MergedItem::Both(packet, ()) => {
            }
        }
        Ok(())
    }).map_err(|_| ()))
}

// Manage connection (and reconnection)
// Receive commands over channel
// Receive packets from network
// Send packets to network

fn do_it_all<C, R, T>(command_rx: C, network_rx: R, network_tx: T) -> Poll<(), MqttError>
    where C: Stream<Item=ClientCommand, Error=()>,
          R: Stream<Item=MqttPacket, Error=MqttError>,
          T: Sink<SinkItem=MqttPacket, SinkError=MqttError>,
{
    Ok(Async::Ready(()))
}

impl<C: Connector> Future for ClientProcess<C> {
    type Item = ();
    type Error = ();

    fn poll(&mut self) -> Poll<Self::Item, Self::Error> {
        self.future.poll()
        // let command = match self.rx.poll() {
        //     Ok(Async::Ready(Some(command))) => command,
        //     Ok(Async::Ready(None)) => return Ok(Async::Ready(())),
        //     Ok(Async::NotReady) => return Ok(Async::NotReady),
        //     Err(_) => return Ok(Async::Ready(())),
        // };
        // println!("I got polled");

        // match mem::replace(&mut self.state, ClientState::None) {
        //     ClientState::New => {
        //         let mut connect_future = self.connector.connect();
        //         match connect_future.poll() {
        //             Ok(Async::Ready(connection)) => {
        //                 self.state = ClientState::Connected(connection);
        //                 Ok(Async::NotReady)
        //             }
        //             Ok(Async::NotReady) => {
        //                 self.state = ClientState::Connecting(connect_future);
        //                 Ok(Async::NotReady)
        //             }
        //             Err(_) => Err(()),
        //         }
        //     }
        //     ClientState::Connecting(mut connect_future) => {
        //         match connect_future.poll() {
        //             Ok(Async::Ready(connection)) => {
        //                 self.state = ClientState::Connected(connection);
        //                 Ok(Async::NotReady)
        //             }
        //             Ok(Async::NotReady) => {
        //                 self.state = ClientState::Connecting(connect_future);
        //                 Ok(Async::NotReady)
        //             }
        //             Err(_) => Err(()),
        //         }
        //     }
        //     ClientState::Connected(mut stream) => {
        //         Ok(Async::Ready(()))
        //     }
        //     ClientState::Reconnecting => {
        //         Ok(Async::NotReady)
        //     }
        //     ClientState::Disconnecting => {
        //         Ok(Async::NotReady)
        //     }
        //     ClientState::Disconnected => {
        //         Ok(Async::NotReady)
        //     }
        //     ClientState::None => panic!(),
        // }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum ClientState<C, F> {
    New,
    Connecting(F),
    Connected(C),
    Disconnecting,
    Reconnecting,
    Disconnected,
    None,
}

// Some notes
// Sending a publish with QoS 1 or QoS 2 should create a future that is
// resolved when the packet send is complete. But packet resends need to
// remain in the same order.
//    Use BTreeMap to achieve fast lookup against ordered list
//    Use VecDeque to achieve ring buffer of who is allowed to resend next
// Subscriptions also use the packet identifier field and will need to be
// dispatched to the correct handler
// All QoS 1/2 packets must be acked, even if the packet is dropped due to lack
// of subscribers on the client
// Need to manage list of subscribers' topic filters and provide incoming
// publish messages to the correct subscriber outputs


// pub struct PublishFutureQoS0;
// pub struct PublishFutureQoS1;
// pub struct PublishFutureQoS2;

// fn dispatch(packet: MqttPacket) -> BoxFuture<(), MqttError> {
//     let state = State::Connecting;
//     match state {
//         Connecting => {
//             // only care about CONNACK packet
//         }
//         Connected => {}
//         _ => {}
//     }
//     future::ok(()).boxed()
// }

// struct ClientConnectFuture {
//     connected: oneshot::Receiver<ClientCommandSender>,
// }
