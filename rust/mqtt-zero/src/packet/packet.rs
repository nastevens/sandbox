// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use packet::connect::ConnectPacket;
use packet::connack::ConnAckPacket;
use packet::disconnect::DisconnectPacket;

pub enum MqttPacketType {
    Reserved = 0,
    Connect = 1,
    ConnAck = 2,
    Publish = 3,
    PubAck = 4,
    PubRec = 5,
    PubRel = 6,
    PubComp = 7,
    Subscribe = 8,
    SubAck = 9,
    Unsubscribe = 10,
    UnsubAck = 11,
    PingReq = 12,
    PingResp = 13,
    Disconnect = 14,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum MqttPacket {
    Connect(ConnectPacket),
    ConnAck(ConnAckPacket),
    Disconnect(DisconnectPacket),
}

impl From<ConnectPacket> for MqttPacket {
    fn from(val: ConnectPacket) -> MqttPacket {
        MqttPacket::Connect(val)
    }
}

impl From<ConnAckPacket> for MqttPacket {
    fn from(val: ConnAckPacket) -> MqttPacket {
        MqttPacket::ConnAck(val)
    }
}

impl From<DisconnectPacket> for MqttPacket {
    fn from(val: DisconnectPacket) -> MqttPacket {
        MqttPacket::Disconnect(val)
    }
}

// impl FromBytes for MqttPacket {
//     type Err = ParseError;
//     fn from_bytes<B: Into<Bytes>>(b: B) -> Result<Option<Self>, Self::Err> {
//         let bytes = b.into();
//         if bytes.len() > 0 {
//             let control = bytes[0];
//             match (bytes[0] & 0xF0) >> 4 {
//                 0x01 => map_map(bytes.parse::<ConnectPacket>(), MqttPacket::Connect),
//                 0x02 => map_map(bytes.parse::<ConnAckPacket>(), MqttPacket::ConnAck),
//                 0x0E => map_map(bytes.parse::<DisconnectPacket>(), MqttPacket::Disconnect),
//                 _ => Err(ParseError),
//             }
//         } else {
//             Ok(None)
//         }
//     }
// }

// // Convenience function to map within a Result<Option, Error> type
// fn map_map<T, E, U, F>(val: Result<Option<T>, E>, f: F) -> Result<Option<U>, E> 
//     where F: FnOnce(T) -> U
// {
//     val.map(|inner1| inner1.map(|inner2| f(inner2)))
// }

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn test_basic_parse() {
//         let packet = (&b"\xE0\x00"[..]).parse::<MqttPacket>();
//         let disconnect = DisconnectPacketBuilder::new().build();
//         assert_eq!(Ok(Some(MqttPacket::Disconnect(disconnect))), packet);
//     }
// }
