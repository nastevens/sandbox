// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

//! MQTT CONNECT zero-copy parser/generator

use bytes::{BigEndian, Bytes, BytesMut, BufMut};

use packet::{FIXED_HEADER_LENGTH, MqttPacketType};
use packet::error::PacketError;
use parse::{ClientIdentifier, DecodeBytes, EncodeBytes, MqttBytes, MqttString, RemainingLength};
use qos::QoS;

const FIXED_HEADER_FLAGS: u8 = 0x00;
const VARIABLE_HEADER_LENGTH: usize = 10;

// CONNECT header flags
bitflags! {
    flags ConnectFlags: u8 {
        const CONNECT_USER_NAME_FLAG = 0b10000000,
        const CONNECT_PASSWORD_FLAG  = 0b01000000,
        const CONNECT_WILL_RETAIN    = 0b00100000,
        const CONNECT_WILL_QOS_BIT1  = 0b00010000,
        const CONNECT_WILL_QOS_BIT0  = 0b00001000,
        const CONNECT_WILL_QOS_MASK  = CONNECT_WILL_QOS_BIT0.bits | CONNECT_WILL_QOS_BIT1.bits,
        const CONNECT_WILL_FLAG      = 0b00000100,
        const CONNECT_CLEAN_SESSION  = 0b00000010,
        const CONNECT_WILL_QOS_LVL0  = 0b00000000,
        const CONNECT_WILL_QOS_LVL1  = CONNECT_WILL_QOS_BIT0.bits,
        const CONNECT_WILL_QOS_LVL2  = CONNECT_WILL_QOS_BIT1.bits,
    }
}

lazy_static! {
    static ref MQTT_PROTOCOL_NAME: MqttString = "MQTT".parse().expect("static string parse");
}

/// MQTT specification level - only 3.1.1 is currently supported.
#[allow(non_camel_case_types)]
#[derive(Clone, Copy, Debug, Hash, Eq, Ord, PartialEq, PartialOrd)]
pub enum ProtocolLevel {
    MQTT_3_1_1 = 4,
}

/// Maximum time interval between client transmissions.
#[derive(Clone, Copy, Debug, Hash, Eq, Ord, PartialEq, PartialOrd)]
pub enum KeepAlive {
    Disabled,
    Enabled(u16),
}

impl KeepAlive {
    pub fn as_u16(&self) -> u16 {
        match *self {
            KeepAlive::Disabled => 0,
            KeepAlive::Enabled(value) => value,
        }
    }
}

/// Zero-copy layer over a buffer representing an MQTT `CONNECT` packet.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ConnectPacket {
    level: ProtocolLevel,
    flags: ConnectFlags,
    keep_alive: KeepAlive,
    client_id: ClientIdentifier,
    will_topic: Option<MqttString>,
    will_message: Option<MqttBytes>,
    user_name: Option<MqttString>,
    password: Option<MqttBytes>,
}

impl ConnectPacket {
    /// Create a new `ConnectPacket`
    pub fn new<C>(client_id: C, keep_alive: KeepAlive) -> ConnectPacket
        where C: Into<ClientIdentifier>
    {
        ConnectPacket {
            level: ProtocolLevel::MQTT_3_1_1,
            flags: ConnectFlags::empty(),
            keep_alive: keep_alive,
            client_id: client_id.into(),
            will_topic: None,
            will_message: None,
            user_name: None,
            password: None,
        }
    }

    /// Get the protocol level (only 3.1.1 supported for now).
    pub fn level(&self) -> ProtocolLevel {
        self.level
    }

    /// Set the protocol level (only 3.1.1 supported for now).
    pub fn set_level<'input>(&'input mut self, level: ProtocolLevel) -> &'input mut Self {
        self.level = level;
        self
    }

    /// Get the "clean session" flag, i.e. destroy any cached session
    /// information on connect.
    pub fn clean_session(&self) -> bool {
        self.flags.contains(CONNECT_CLEAN_SESSION)
    }

    /// Set the "clean session" flag, i.e. destroy any cached session
    /// information on connect.
    pub fn set_clean_session<'input>(&'input mut self, clean_session: bool) -> &'input mut Self {
        self.flags.set(CONNECT_CLEAN_SESSION, clean_session);
        self
    }

    /// Get keep alive time interval in seconds.
    pub fn keep_alive(&self) -> KeepAlive {
        self.keep_alive
    }

    /// Set keep alive time interval in seconds.
    pub fn set_keep_alive<'input>(&'input mut self, keep_alive: KeepAlive) -> &'input mut Self {
        self.keep_alive = keep_alive;
        self
    }

    /// Get the client identifier.
    pub fn client_identifier(&self) -> &ClientIdentifier {
        &self.client_id
    }

    /// Set the client identifier.
    pub fn set_client_identifier<'input>(&'input mut self, client_id: ClientIdentifier) -> &'input mut Self {
        self.client_id = client_id;
        self
    }

    /// Get topic to send message to on unclean disconnect.
    pub fn will_topic(&self) -> Option<&MqttString> {
        self.will_topic.as_ref()
    }

    /// Get message to send on unclean disconnect.
    pub fn will_message(&self) -> Option<&MqttBytes> {
        self.will_message.as_ref()
    }

    /// Get QoS to be used when delivering message on unclean disconnect.
    pub fn will_qos(&self) -> Option<QoS> {
        if self.flags.contains(CONNECT_WILL_FLAG) {
            match self.flags & CONNECT_WILL_QOS_MASK {
                CONNECT_WILL_QOS_LVL0 => Some(QoS::AtMostOnce),
                CONNECT_WILL_QOS_LVL1 => Some(QoS::AtLeastOnce),
                CONNECT_WILL_QOS_LVL2 => Some(QoS::ExactlyOnce),
                _ => None,
            }
        } else {
            None
        }
    }

    /// Set last will and testiment.
    pub fn set_will<'input, S, B>(&'input mut self, topic: S, message: B, qos: QoS, retain: bool) -> &'input mut Self
        where S: Into<MqttString>,
              B: Into<MqttBytes>
    {
        self.flags.insert(CONNECT_WILL_FLAG);
        self.flags.set(CONNECT_WILL_RETAIN, retain);
        // make sure QoS bits start clear
        self.flags &= !CONNECT_WILL_QOS_MASK;
        self.flags |= match qos {
            QoS::AtMostOnce => CONNECT_WILL_QOS_LVL0,
            QoS::AtLeastOnce => CONNECT_WILL_QOS_LVL1,
            QoS::ExactlyOnce => CONNECT_WILL_QOS_LVL2,
        };
        self.will_topic = Some(topic.into());
        self.will_message = Some(message.into());
        self
    }

    /// Get user name.
    pub fn user_name(&self) -> Option<&MqttString> {
        self.user_name.as_ref()
    }

    /// Set user name.
    pub fn set_user_name<'input, S>(&'input mut self, user_name: Option<S>) -> &'input mut Self
        where S: Into<MqttString>
    {
        self.flags.set(CONNECT_USER_NAME_FLAG, user_name.is_some());
        self.user_name = user_name.map(Into::into);
        self
    }

    /// Get password.
    pub fn password(&self) -> Option<&MqttBytes> {
        self.password.as_ref()
    }

    /// Set password.
    pub fn set_password<'input, B>(&'input mut self, password: Option<B>) -> &'input mut Self
        where B: Into<MqttBytes>
    {
        self.flags.set(CONNECT_PASSWORD_FLAG, password.is_some());
        self.password = password.map(Into::into);
        self
    }

    // Get length of packet less the fixed packet header
    fn calculate_remaining_length(&self) -> usize {
        VARIABLE_HEADER_LENGTH
            + self.client_id.encoded_len()
            + self.will_topic.as_ref().map(MqttString::encoded_len).unwrap_or(0)
            + self.will_message.as_ref().map(MqttBytes::encoded_len).unwrap_or(0)
            + self.user_name.as_ref().map(MqttString::encoded_len).unwrap_or(0)
            + self.password.as_ref().map(MqttBytes::encoded_len).unwrap_or(0)
    }
}

impl DecodeBytes for ConnectPacket {
    type Error = PacketError;
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error> {
        require_length!(FIXED_HEADER_LENGTH, src.len());
        if src[0] >> 4 != MqttPacketType::Connect as u8 {
            return Err(PacketError::InvalidHeader)
        }
        if src[0] & 0x0F != 0 {
            return Err(PacketError::InvalidHeader)
        }
        let remaining = if let Some(inner) = RemainingLength::decode_no_consume(&mut src.slice_from(FIXED_HEADER_LENGTH))? {
            inner
        } else {
            return Ok(None);
        };
        require_length!(FIXED_HEADER_LENGTH + remaining.len() + remaining.value(), src.len());
        // consume bytes we decoded
        let _ = src.split_to(FIXED_HEADER_LENGTH + remaining.len());
        Ok(None)
    }
}


impl EncodeBytes for ConnectPacket {
    type Error = PacketError;
    fn encode(&self, dst: &mut BytesMut) -> Result<(), Self::Error> {
        dst.put_u8((MqttPacketType::Connect as u8) << 4 | FIXED_HEADER_FLAGS);
        let remaining_length = self.calculate_remaining_length();
        RemainingLength::new(remaining_length)?.encode(dst)?;
        dst.put(&*MQTT_PROTOCOL_NAME);
        dst.put_u8(self.level as u8);
        dst.put_u8(self.flags.bits());
        dst.put_u16::<BigEndian>(self.keep_alive.as_u16());
        dst.put(&self.client_id);
        encode_if_some(self.will_topic.as_ref(), dst)?;
        encode_if_some(self.will_message.as_ref(), dst)?;
        encode_if_some(self.user_name.as_ref(), dst)?;
        encode_if_some(self.password.as_ref(), dst)?;
        Ok(())
    }
}

fn encode_if_some<T: EncodeBytes<Error=E>, E: Into<PacketError>>(val: Option<&T>, dst: &mut BytesMut) -> Result<(), PacketError> {
    if let Some(inner) = val {
        inner.encode(dst).map_err(|e| e.into())
    } else {
        Ok(())
    }
}

// impl Wrapped for ConnectPacket {
//     type Wrapper = MqttPacket;
//     fn wrap(self) -> Self::Wrapper {
//         MqttPacket::Connect(self)
//     }
// }

// #[cfg(test)]
// mod tests {
//     use super::*;

//     const TEST_CONNECT_PACKETS: &[&[u8]] = &[
//         b"\x10\x0A\x00\x04MQTT\x04\x00\x00\x00",
//     ];

//     #[test]
//     fn test_parse() {
//         let buffer = &b"\x10\x0A\x00\x04MQTT\x04\x00\x00\x00"[..];
//         let connect = buffer.parse::<ConnectPacket>();
//     }

//     #[test]
//     fn test_builder() {
//         let client_id = "testclient".parse::<ClientIdentifier>().unwrap();
//         let will_topic = MqttString::new("some/fake/topic").unwrap();
//         let will_message = MqttBytes::new(b"fake data").unwrap();
//         let user_name = MqttString::new("username").unwrap();
//         let password = MqttBytes::new(b"super secure password").unwrap();
//         let mut connect = ConnectPacket::new(client_id, KeepAlive::Enabled(60));
//         connect
//             .set_level(ProtocolLevel::MQTT_3_1_1)
//             .set_clean_session(true)
//             .set_will(will_topic, will_message, QoS::AtMostOnce, false)
//             .set_user_name(Some(user_name))
//             .set_password(Some(password))
//             .build();
//         assert_eq!(ProtocolLevel::MQTT_3_1_1, connect.level());
//         assert_eq!(KeepAlive::Enabled(60), connect.keep_alive());
//         assert_eq!(true, connect.clean_session());
//         assert_eq!("testclient", connect.client_identifier());
//         assert_eq!("some/fake/topic", connect.will_topic().unwrap());
//         assert_eq!(b"fake data".as_ref(), connect.will_message().unwrap());
//         assert_eq!("username", connect.user_name().unwrap());
//         assert_eq!(b"super secure password".as_ref(), connect.password().unwrap());
//     }
// }
