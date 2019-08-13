// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use std::io::{self, Read, Write};

use futures::{Async, Future, Poll};
use tokio_io::{AsyncRead, AsyncWrite};

use reconnect::Connector;

// pub fn reconnect<C: Connector>(connector: C) -> Reconnect<C> {

// }

pub struct Reconnect<C: Connector> {
    connector: C,
    connection: Option<C::Item>,
}

impl<C: Connector> Reconnect<C> {

}

impl<C: Connector> Read for Reconnect<C> {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        // TODO: If connection is available, read from it, otherwise try to
        // establish connection. Connection may also be in the process of being
        // opened.
        Ok(0)
    }
}

impl<C: Connector> AsyncRead for Reconnect<C> {}

impl<C: Connector> Write for Reconnect<C> {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        // TODO
        Ok(0)
    }

    fn flush(&mut self) -> io::Result<()> {
        // TODO
        Ok(())
    }
}

impl<C: Connector> AsyncWrite for Reconnect<C> {
    fn shutdown(&mut self) -> Poll<(), io::Error> {
        // TODO
        Ok(Async::Ready(()))
    }
}
