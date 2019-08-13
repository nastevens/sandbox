// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

//! Tokio `Encoder` and `Decoder` implementations for the MQTT protocol.

use bytes::BytesMut;
use mqtt_zero::packet::MqttPacket;
use tokio_io::codec::{Encoder, Decoder};

use error::MqttError;

pub struct MqttCodec;

impl Decoder for MqttCodec {
    type Item = MqttPacket;
    type Error = MqttError;

    fn decode(&mut self, src: &mut BytesMut) -> Result<Option<Self::Item>, Self::Error> {
        // src.parse::<MqttPacket>().map_err(|e| e.into())
        Ok(None)
    }
}

impl Encoder for MqttCodec {
    type Item = MqttPacket;
    type Error = MqttError;

    fn encode(&mut self, item: Self::Item, dst: &mut BytesMut) -> Result<(), Self::Error> {
        Err(MqttError::Other("".to_string()))
    }
}
