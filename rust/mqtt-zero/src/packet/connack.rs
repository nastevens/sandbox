// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use bytes::{BufMut, Bytes, BytesMut};

use parse::{DecodeBytes, EncodeBytes};
use packet::FIXED_HEADER_LENGTH;
use packet::error::PacketError;

const CONNACK_HEADER: &'static [u8] = &[0x20, 0x02];
const PACKET_LENGTH: usize = FIXED_HEADER_LENGTH + 2;

#[derive(Clone, Copy, Debug, Hash, Eq, Ord, PartialEq, PartialOrd)]
pub enum ConnectReturnCode {
    ConnectionAccepted,
    UnacceptableProtocolVersion,
    IdentifierRejected,
    ServiceUnavailable,
    BadUserNameOrPassword,
    NotAuthorized,
    Reserved(u8),
}

impl From<u8> for ConnectReturnCode {
    fn from(val: u8) -> ConnectReturnCode {
        use self::ConnectReturnCode::*;
        match val {
            0x00 => ConnectionAccepted,
            0x01 => UnacceptableProtocolVersion,
            0x02 => IdentifierRejected,
            0x03 => ServiceUnavailable,
            0x04 => BadUserNameOrPassword,
            0x05 => NotAuthorized,
            other => Reserved(other),
        }
    }
}

impl From<ConnectReturnCode> for u8 {
    fn from(val: ConnectReturnCode) -> u8 {
        use self::ConnectReturnCode::*;
        match val {
            ConnectionAccepted => 0x00,
            UnacceptableProtocolVersion => 0x01,
            IdentifierRejected => 0x02,
            ServiceUnavailable => 0x03,
            BadUserNameOrPassword => 0x04,
            NotAuthorized => 0x05,
            Reserved(x) => x,
        }
    }
}

#[derive(Clone, Debug, Hash, Eq, Ord, PartialEq, PartialOrd)]
pub struct ConnAckPacket {
    pub session_present: bool,
    pub return_code: ConnectReturnCode,
    _private: (),
}

impl ConnAckPacket {
    /// Create a new CONNACK packet.
    pub fn new(session_present: bool, return_code: ConnectReturnCode) -> Result<ConnAckPacket, PacketError> {
        Ok(ConnAckPacket { session_present, return_code, _private: () })
    }
}

impl DecodeBytes for ConnAckPacket {
    type Error = PacketError;
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error> {
        require_length!(PACKET_LENGTH, src.len());
        if &src[0..FIXED_HEADER_LENGTH] == CONNACK_HEADER && src[2] & 0xFE == 0 {
            Ok(Some(ConnAckPacket {
                session_present: src[2] & 0x01 > 0,
                return_code: ConnectReturnCode::from(src[3]),
                _private: (),
            }))
        } else {
            Err(PacketError::InvalidHeader)
        }
    }
}

impl EncodeBytes for ConnAckPacket {
    type Error = PacketError;
    fn encode(&self, dst: &mut BytesMut) -> Result<(), Self::Error> {
        dst.put(CONNACK_HEADER);
        dst.put_u8(if self.session_present { 1 } else { 0 });
        dst.put_u8(self.return_code.into());
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    lazy_static! {
        static ref TEST_DECODES: Vec<(&'static [u8], Result<Option<ConnAckPacket>, PacketError>)> = vec![
            (b"\x20\x02\x01\x00", Ok(Some(ConnAckPacket::new(true, ConnectReturnCode::ConnectionAccepted).unwrap()))),
            (b"\x20\x02\x00\x01", Ok(Some(ConnAckPacket::new(false, ConnectReturnCode::UnacceptableProtocolVersion).unwrap()))),
            (b"\x20\x02\x01\x05", Ok(Some(ConnAckPacket::new(true, ConnectReturnCode::NotAuthorized).unwrap()))),
            (b"\x20\x02\x01\x05\xFF", Ok(Some(ConnAckPacket::new(true, ConnectReturnCode::NotAuthorized).unwrap()))),
            (b"", Ok(None)),
            (b"\x20\x02", Ok(None)),
            (b"\x20\x02\x11\x00", Err(PacketError::InvalidHeader)),
            (b"\x20\x00\x01\x00", Err(PacketError::InvalidHeader)),
        ];
    }

    #[test]
    fn test_decoding() {
        for &(test_data, ref expected) in TEST_DECODES.iter() {
            let mut bytes = Bytes::from(&test_data[..]);
            let result = ConnAckPacket::decode(&mut bytes);
            assert_eq!(*expected, result, "input: {:?}", test_data);
        }
    }

    const TEST_ENCODES: &[(bool, ConnectReturnCode, &[u8])] = &[
        (true, ConnectReturnCode::ConnectionAccepted, b"\x20\x02\x01\x00"),
        (false, ConnectReturnCode::UnacceptableProtocolVersion, b"\x20\x02\x00\x01"),
        (false, ConnectReturnCode::NotAuthorized, b"\x20\x02\x00\x05"),
        (true, ConnectReturnCode::Reserved(7), b"\x20\x02\x01\x07"),
    ];

    #[test]
    fn test_create_and_encode() {
        for &(session_present, return_code, expected) in TEST_ENCODES {
            let packet = ConnAckPacket::new(session_present, return_code).unwrap();
            let mut buffer = BytesMut::with_capacity(8 * 1024);
            packet.encode(&mut buffer).unwrap();
            assert_eq!(expected, &buffer[..]);
        }
    }
}
