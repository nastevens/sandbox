// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

//! Functions for encoding and decoding the "remaining length" fields of MQTT
//! packets.

use std::iter;
use std::ops::Deref;

use bytes::{Bytes, BytesMut};

use parse::{DecodeBytes, EncodeBytes};

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct RemainingLength(usize, usize);

impl RemainingLength {
    pub fn new(value: usize) -> Result<RemainingLength, RemainingLengthError> {
        let bytes_needed = Self::bytes_needed(value)?;
        Ok(RemainingLength(value, bytes_needed))
    }

    pub fn value(&self) -> usize {
        self.0
    }

    pub fn len(&self) -> usize {
        self.1
    }

    pub fn bytes_needed(value: usize) -> Result<usize, RemainingLengthError> {
        if value < 128 {
            Ok(1)
        } else if value < 16_384 {
            Ok(2)
        } else if value < 2_097_152 {
            Ok(3)
        } else if value < 268_435_456 {
            Ok(4)
        } else {
            Err(RemainingLengthError)
        }
    }

    pub fn decode_no_consume(src: &Bytes) -> Result<Option<RemainingLength>, RemainingLengthError> {
        let mut value: Option<usize> = None;
        // Note that clone here is lightweight clone over Bytes type
        let iter = src.iter().map(|x| *x as usize).take(4).enumerate();
        for (round, encoded) in iter {
            value = value
                .map(|v| v + (encoded & 0x7F) * (1 << (round * 7)))
                .or(Some(encoded & 0x7F));
            if encoded & 0x80 == 0 {
                return Ok(value.map(|inner| RemainingLength(inner, round + 1)));
            }
            if round == 3 && encoded & 0x80 != 0 {
                // Decoded value is too long
                return Err(RemainingLengthError);
            }
        }
        // Decoded value is incomplete
        Ok(None)
    }
}

impl DecodeBytes for RemainingLength {
    type Error = RemainingLengthError;
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error> {
        match Self::decode_no_consume(src) {
            Ok(Some(RemainingLength(value, bytes))) => {
                // Consume bytes we used
                let _ = src.split_to(bytes);
                Ok(Some(RemainingLength(value, bytes)))
            }
            other => other,
        }
    }
}

impl EncodeBytes for RemainingLength {
    type Error = RemainingLengthError;
    fn encode(&self, dst: &mut BytesMut) -> Result<(), Self::Error> {
        if self.0 > 268_435_455 {
            return Err(RemainingLengthError);
        }
        let mut value = self.0 as u32;
        loop {
            let mut encoded = (value % 0x80) as u8;
            value /= 0x80;
            if value > 0 {
                encoded |= 0x80;
            }
            dst.extend(iter::once(encoded));
            if value == 0 {
                break;
            }
        }
        Ok(())
    }
}

impl From<RemainingLength> for usize {
    fn from(val: RemainingLength) -> usize {
        val.0
    }
}

impl Deref for RemainingLength {
    type Target = usize;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl AsRef<usize> for RemainingLength {
    fn as_ref(&self) -> &usize {
        &self.0
    }
}

/// The buffer does not contain a valid encoded length.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct RemainingLengthError;

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_DECODES: &[(&[u8], Result<Option<(usize, usize)>, RemainingLengthError>)] = &[
        (&[], Ok(None)),
        (&[0x00], Ok(Some((0, 1)))),

        // Too short, maybe more coming
        (&[0x80], Ok(None)),
        (&[0x80, 0x80], Ok(None)),

        // Junk values after good bytes, should be ignored
        (&[0x40, 0xAB, 0xCD, 0xEF], Ok(Some((64, 1)))),
        (&[0xC1, 0x02, 0xAB, 0xCD], Ok(Some((321, 2)))),

        // Transition points
        (&[0x7F], Ok(Some((127, 1)))),
        (&[0x80, 0x01], Ok(Some((128, 2)))),
        (&[0xFF, 0x7F], Ok(Some((16_383, 2)))),
        (&[0x80, 0x80, 0x01], Ok(Some((16_384, 3)))),
        (&[0xFF, 0xFF, 0x7F], Ok(Some((2_097_151, 3)))),
        (&[0x80, 0x80, 0x80, 0x01], Ok(Some((2_097_152, 4)))),

        // Max value
        (&[0xFF, 0xFF, 0xFF, 0x7F], Ok(Some((268_435_455, 4)))),

        // Max value with junk after last byte
        (&[0xFF, 0xFF, 0xFF, 0x7F, 0xFF], Ok(Some((268_435_455, 4)))),

        // Too long, more than 4 bytes
        (&[0xFF, 0xFF, 0xFF, 0x80], Err(RemainingLengthError)),
        (&[0xFF, 0xFF, 0xFF, 0x80, 0xFF], Err(RemainingLengthError)),
    ];

    #[test]
    fn test_decode() {
        for &(test_data, expected) in TEST_DECODES {
            let expected = expected.map(|option| option.map(|(value, size)| RemainingLength(value, size)));
            let mut buffer = Bytes::from_static(test_data);
            assert_eq!(expected,
                       RemainingLength::decode(&mut buffer),
                       "input: {:?}",
                       buffer);
        }
    }

    const TEST_ENCODES: &[(usize, Result<&[u8], RemainingLengthError>)] = &[
        // Normal cases
        (0, Ok(&[0x00])),
        (127, Ok(&[0x7F])),
        (128, Ok(&[0x80, 0x01])),
        (16_383, Ok(&[0xFF, 0x7F])),
        (16_384, Ok(&[0x80, 0x80, 0x01])),
        (2_097_151, Ok(&[0xFF, 0xFF, 0x7F])),
        (2_097_152, Ok(&[0x80, 0x80, 0x80, 0x01])),
        (268_435_455, Ok(&[0xFF, 0xFF, 0xFF, 0x7F])),

        // More than maximum value
        (268_435_456, Err(RemainingLengthError)),
    ];

    #[test]
    fn test_encode() {
        for &(test_value, expected) in TEST_ENCODES {
            let mut buffer = BytesMut::with_capacity(32);
            if let Ok(expected_bytes) = expected {
                let test_length = RemainingLength::new(test_value).unwrap();
                let _ = test_length.encode(&mut buffer).unwrap();
                assert_eq!(expected_bytes, buffer, "input: {:?}", test_value);
            } else {
                assert!(RemainingLength::new(test_value).is_err());
            }
        }
    }
}
