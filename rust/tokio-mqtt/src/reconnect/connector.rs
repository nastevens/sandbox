// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use std::io;
use std::mem;
use std::net::SocketAddr;

use futures::{Future, IntoFuture};
use futures::future::FutureResult;
use tokio_core::net::{TcpStream, TcpStreamNew};
use tokio_core::reactor::Handle;
use tokio_io::{AsyncRead, AsyncWrite};

use error::MqttError;

/// Trait for generators capable of creating connections.
///
/// Because the MQTT protocol allows and often utilizes reconnects, the MQTT
/// library needs to be able to own the creation and destruction of the
/// underlying streams. However, MQTT can also be used over numerous
/// byte-oriented channels: TCP, TLS, WebSockets, and others, and each has its
/// own requirements for how to connect.
///
/// Types that implement `Connector` abstract connection, reconnection, and
/// disconnection logic for a particular stream. All configuration needs to be
/// "baked into" the `Connector` itself.
pub trait Connector: Sized {
    type Future: Future<Item = Self::Item, Error = Self::Error> + Send;
    type Item: AsyncRead + AsyncWrite + 'static;
    type Error: Into<MqttError>;

    /// Create a future that will resolve into an async stream on success.
    fn connect(&mut self) -> Self::Future;

    /// Create a future that will resolve into an async stream on success,
    /// possibly utilizing information from the previous connection.
    ///
    /// The default implementation calls `connect` and ignores the previous
    /// return value.
    fn reconnect(&mut self, previous: Self::Item) -> Self::Future {
        self.connect()
    }
}

/// `Connector` wrapper for types that implement AsyncRead and AsyncWrite.
///
/// Wraps a type implementing `AsyncRead` and `AsyncWrite`, providing a
/// `Connector` implementation that will return the underlying type the first
/// time that `connect` is called. Note that `reconnect` is not implemented for
/// this type, meaning that it will error if the original inner connection
/// errors.
pub struct AsyncIoConnector<T> {
    inner: Option<T>,
}

impl<T> AsyncIoConnector<T>
    where T: AsyncRead + AsyncWrite + 'static
{
    pub fn new(inner: T) -> AsyncIoConnector<T> {
        AsyncIoConnector {
            inner: Some(inner),
        }
    }
}

impl<T> Connector for AsyncIoConnector<T>
    where T: AsyncRead + AsyncWrite + Send + 'static
{
    type Future = FutureResult<T, io::Error>;
    type Item = T;
    type Error = io::Error;

    fn connect(&mut self) -> Self::Future {
        if let Some(stream) = mem::replace(&mut self.inner, None) {
            Ok(stream).into_future()
        } else {
            Err(io::Error::new(io::ErrorKind::InvalidData, "Stream already consumed")).into_future()
        }
    }
}

/// `Connector` implementation for TCP streams.
///
/// Wraps a `TcpStream`, returning a new connection each time `connect` or
/// `reconnect` are called.
pub struct TcpStreamConnector {
    addr: SocketAddr,
    handle: Handle,
}

impl TcpStreamConnector {
    pub fn new(addr: SocketAddr, handle: Handle) -> TcpStreamConnector {
        TcpStreamConnector {
            addr,
            handle,
        }
    }
}

impl Connector for TcpStreamConnector {
    type Future = TcpStreamNew;
    type Item = TcpStream;
    type Error = io::Error;

    fn connect(&mut self) -> Self::Future {
        TcpStream::connect(&self.addr, &self.handle)
    }
}


