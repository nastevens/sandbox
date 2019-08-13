// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

pub struct Message<T> {
    header: (), // TODO: replace with header info like topic name
    body: T,
}

/// Reads incoming messages from a stream and enqueues them into the
/// appropriate subscriptions clients.
pub struct SubscriptionDispatch<S> {
    message_stream: S,
}

impl<S> SubscriptionDispatch<S> {
}

/// Reads commands from a stream to subscribe or unsubscribe from a topic.
/// Completes a future when the request is complete.
///
/// Produces SUBSCRIBE and UNSUBSCRIBE packets. Consumes SUBACK and UNSUBACK
/// packets.
pub struct SubscriptionManagementStream<S> {
    command_stream: S,
}

impl<S> Stream for SubscriptionManagementStream<S> {
    type Item = MqttPacket;
    type Error = MqttError;

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        Ok(Async::NotReady)
    }
}

impl<S> Sink for SubscriptionManagementStream<S> {
    type SinkItem = MqttPacket;
    type SinkError = MqttError;

    fn start_send(&mut self, item: Self::SinkItem) -> StartSend<Self::SinkItem, Self::SinkError> {
        Ok(AsyncSink::Ready)
    }

    fn poll_complete(&mut self) -> Poll<(), Self::SinkError> {
        Ok(Async::NotReady)
    }
}

// struct TopicStream;

// impl TopicStream {
//     pub fn unsubscribe(self) { }
// }

// // Resolves to a stream when successful
// struct SubscriberFuture;
