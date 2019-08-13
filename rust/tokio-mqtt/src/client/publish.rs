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

/// Incoming PUBLISH and PUBREL packets are fed into the sink, which may
/// trigger new PUBACK, PUBREC, or PUBCOMP packets to be available to read from the
/// stream. Timeouts causing packet resends can also trigger new packets to be
/// made available on the stream.
///
/// Completed messages are passed off to a different stream that figures out
/// which subscribers should receive a copy of the message. That is a one-way
/// operation.
struct PublishReceiveStream<S> {
    subscription_sink: S,
}

impl<S> Stream for PublishReceiveStream<S> {
    type Item = MqttPacket;
    type Error = MqttError;

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        Ok(Async::NotReady)
    }
}

impl<S> Sink for PublishReceiveStream<S> {
    type SinkItem = MqttPacket;
    type SinkError = MqttError;

    fn start_send(&mut self, item: Self::SinkItem) -> StartSend<Self::SinkItem, Self::SinkError> {
        Ok(AsyncSink::Ready)
    }

    fn poll_complete(&mut self) -> Poll<(), Self::SinkError> {
        Ok(Async::NotReady)
    }
}

/// Watches an incoming stream for new PUBLISH messages with an associated
/// Future. Then sends PUBLISH and PUBREL packets out through its stream as
/// appropriate, and takes PUBACK, PUBREC, and PUBCOMP packets on its sink.
/// Finally completes the publish Future once the send is successful.
struct PublishSendStream<S> {
    publish_stream: S,
}

impl<S> Stream for PublishSendStream<S> {
    type Item = MqttPacket;
    type Error = MqttError;

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        Ok(Async::NotReady)
    }
}

impl<S> Sink for PublishSendStream<S> {
    type SinkItem = MqttPacket;
    type SinkError = MqttError;

    fn start_send(&mut self, item: Self::SinkItem) -> StartSend<Self::SinkItem, Self::SinkError> {
        Ok(AsyncSink::Ready)
    }

    fn poll_complete(&mut self) -> Poll<(), Self::SinkError> {
        Ok(Async::NotReady)
    }
}

// // Resolves to a sink when successful
// struct PublisherFuture;

// // convenience for cases where custom codec isn't desired
// struct StringEncoder;
// struct BytesEncoder;

