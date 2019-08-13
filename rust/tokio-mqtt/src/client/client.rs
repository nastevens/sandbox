// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use std::marker::PhantomData;

use futures::unsync::mpsc;
use tokio_core::reactor::Handle;

use reconnect::Connector;
use client::process::ClientProcess;
use client::ClientCommand;

const COMMAND_CHANNEL_SIZE: usize = 1024;

pub struct ClientOptions {
    command_queue: usize,
}

impl Default for ClientOptions {
    fn default() -> Self {
        ClientOptions {
            command_queue: 16,
        }
    }
}

/// Asynchronous interactions with an MQTT broker.
pub struct Client<C> {
    tx: mpsc::Sender<ClientCommand>,
    _connector: PhantomData<C>,
}

impl<C: Connector> Client<C>
    where C: 'static
{
    pub fn new(connector: C, handle: &Handle, options: ClientOptions) -> Client<C> {
        // TODO: start client process and hand off connector
        let (tx, rx) = mpsc::channel::<ClientCommand>(options.command_queue);
        handle.spawn(ClientProcess::new(connector, rx));
        Client {
            tx: tx,
            _connector: PhantomData,
        }
    }

    // TODO: Implement publisher types
    // /// Returns a Future that resolves to a PublishSink.
    // pub fn publisher<E: Encoder, T: Into<Topic>>(&self, topic: T, encoder: E) -> PublisherFuture {
    //     PublisherFuture
    // }

    // TODO: subscribe to multiple in one command
    // TODO: return in wrapper on messages with topic?
    // /// Returns a Future that resolves to a SubscriptionStream after
    // /// successfully registering with the broker.
    // pub fn subscriber<D: Decoder, T: Into<Topic>>(&self, topic: T, decoder: T) -> SubscriberFuture {
    //     SubscriberFuture
    // }

    // pub fn disconnect(self) -> DisconnectFuture {
    //     DisconnectFuture
    // }
}

#[cfg(test)]
mod tests {
    use std::time::Duration;

    use futures::{future, Future, Stream};
    use tokio_core::reactor::Core;
    use tokio_core::net::{TcpListener, TcpStream};
    use tokio_timer::Timer;

    use reconnect::TcpStreamConnector;
    use super::*;

    #[test]
    fn test_start_stop() {
        let options = ClientOptions::default();
        let address = "127.0.0.1:0".parse().unwrap();
        let mut core = Core::new().unwrap();
        let handle = core.handle();
        let timer = Timer::default();
        let server = TcpListener::bind(&address, &handle).unwrap();
        let connector = TcpStreamConnector::new(server.local_addr().unwrap(), handle.clone());
        let service = server.incoming().take(1).for_each(|connection| {
            println!("I ran");
            Ok(())
        });
        let client = Client::new(connector, &handle, options);
        let timeout = timer.timeout(service, Duration::new(1, 0));
        let result = core.run(timeout);
        assert!(result.is_ok(), "error: {:?}", result);
    }
}
