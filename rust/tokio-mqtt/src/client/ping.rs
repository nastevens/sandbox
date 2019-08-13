// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use futures::{Async, Poll, Stream, Sink, StartSend, AsyncSink};
use mqtt_zero::packet::MqttPacket;

use error::MqttError;

/// Generates PINGREQ, consumes PINGRESP. Consumes a (?) of events signalling
/// that packets have been successfully received from the server (resetting the
/// timout).
struct PingStream;

impl Stream for PingStream {
    type Item = MqttPacket;
    type Error = MqttError;

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        Ok(Async::NotReady)
    }
}

impl Sink for PingStream {
    type SinkItem = MqttPacket;
    type SinkError = MqttError;

    fn start_send(&mut self, item: Self::SinkItem) -> StartSend<Self::SinkItem, Self::SinkError> {
        Ok(AsyncSink::Ready)
    }

    fn poll_complete(&mut self) -> Poll<(), Self::SinkError> {
        Ok(Async::NotReady)
    }
}
