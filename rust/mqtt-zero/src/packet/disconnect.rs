// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use bytes::{Bytes, BytesMut};

use packet::error::PacketError;
use parse::{DecodeBytes, EncodeBytes};

const DISCONNECT_PACKET: &'static [u8] = &[0xE0, 0x00];

#[derive(Clone, Debug, Hash, Eq, Ord, PartialEq, PartialOrd)]
pub struct DisconnectPacket;

impl DisconnectPacket {
    /// Create a new DISCONNECT packet.
    pub fn new() -> Result<DisconnectPacket, PacketError> {
        Ok(DisconnectPacket)
    }
}

impl DecodeBytes for DisconnectPacket {
    type Error = PacketError;
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error> {
        require_length!(2, src.len());
        if &src[0..2] == DISCONNECT_PACKET {
            Ok(Some(DisconnectPacket))
        } else {
            Err(PacketError::InvalidHeader)
        }
    }
}

impl EncodeBytes for DisconnectPacket {
    type Error = PacketError;
    fn encode(&self, dst: &mut BytesMut) -> Result<(), Self::Error> {
        dst.extend(DISCONNECT_PACKET);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    lazy_static! {
        static ref TEST_DECODES: Vec<(&'static [u8], Result<Option<DisconnectPacket>, PacketError>)> = vec![
            (b"\xE0\x00", Ok(Some(DisconnectPacket::new().unwrap()))),
            (b"\xE0\x00\xFF\x00", Ok(Some(DisconnectPacket::new().unwrap()))),
            (b"\xE0", Ok(None)),
            (b"\xF0\x00", Err(PacketError::InvalidHeader)),
        ];
    }

    #[test]
    fn test_decoding() {
        for &(ref test_data, ref expected) in TEST_DECODES.iter() {
            let mut bytes = Bytes::from(&test_data[..]);
            let result = DisconnectPacket::decode(&mut bytes);
            assert_eq!(*expected, result);
        }
    }

    #[test]
    fn test_create_and_encode() {
        let packet = DisconnectPacket::new().unwrap();
        let mut buffer = BytesMut::with_capacity(8 * 1024);
        packet.encode(&mut buffer).unwrap();
        assert_eq!(&b"\xE0\x00"[..], &buffer[..]);
    }
}
