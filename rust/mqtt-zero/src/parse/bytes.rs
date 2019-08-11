// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use std::error::Error;
use std::fmt;
use std::io::Cursor;
use std::ops::Deref;

use bytes::{Bytes, BytesMut, BigEndian, Buf, BufMut, IntoBuf};

use parse::{DecodeBytes, EncodeBytes};

const LENGTH_FIELD_BYTES: usize = 2;

/// Length-prefixed bytes per MQTT spec.
///
/// # Examples
///
/// ```
/// use mqtt_zero::parse::MqttBytes;
/// let bytes = MqttBytes::new(b"some bytes").unwrap();
/// assert_eq!(&b"\x00\x0Asome bytes"[..], bytes.as_slice());
/// ```
#[derive(Clone, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct MqttBytes {
    buffer: Bytes,
}

impl MqttBytes {
    /// Create an `MqttBytes` from the given bytes.
    ///
    /// Reads the provided bytes into an MqttBytes object, adding the
    /// necessary length field before the payload.
    ///
    /// This method will return an error if the payload is more than 65535
    /// bytes.
    pub fn new<B: AsRef<[u8]>>(bytes: B) -> Result<MqttBytes, MqttBytesError> {
        let bytes = bytes.as_ref();
        if bytes.len() > 0xFFFF {
            Err(MqttBytesError::TooLong)
        } else {
            let mut parsed = BytesMut::with_capacity(LENGTH_FIELD_BYTES + bytes.len());
            parsed.put_u16::<BigEndian>(bytes.len() as u16);
            parsed.put(bytes);
            Ok(MqttBytes {
                buffer: parsed.freeze(),
            })
        }
    }

    /// Create an `MqttBytes` from the given `Bytes` without checking validity.
    ///
    /// Creates an `MqttBytes` with no validity checking, which is why the
    /// function is `unsafe`. The `Bytes` buffer _must_ be exactly the length
    /// of the bytes object and _must_ have a correct two-byte length field.
    pub unsafe fn from_bytes_unchecked(buffer: Bytes) -> MqttBytes {
        MqttBytes { buffer }
    }

    /// Returns the length of the bytes, not including the length of the
    /// header.
    pub fn len(&self) -> usize {
        self.as_ref().len()
    }

    /// Returns the total length of the encoded bytes, including the length of
    /// the header.
    pub fn encoded_len(&self) -> usize {
        self.buffer.len()
    }

    /// Returns a lightweight copy of this string's `Bytes` buffer (including
    /// length header).
    pub fn as_bytes(&self) -> Bytes {
        self.buffer.clone()
    }

    /// Returns a slice over the bytes of this object (including length
    /// header).
    pub fn as_slice(&self) -> &[u8] {
        &self.buffer[..]
    }

    /// Consumes the `MqttBytes`, returning the underlying `Bytes`.
    pub fn take(self) -> Bytes {
        self.buffer
    }
}

impl DecodeBytes for MqttBytes {
    type Error = MqttBytesError;
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error> {
        let length = {
            let mut buf = Cursor::new(&src);
            require_length!(LENGTH_FIELD_BYTES, buf.remaining());
            let bytes_len = buf.get_u16::<BigEndian>() as usize;
            require_length!(bytes_len, buf.remaining());
            LENGTH_FIELD_BYTES + bytes_len
        };

        let split_buf = src.split_to(length);
        Ok(Some(MqttBytes { buffer: split_buf }))
    }
}

impl EncodeBytes for MqttBytes {
    type Error = MqttBytesError;
    fn encode(&self, dst: &mut BytesMut) -> Result<(), Self::Error> {
        dst.extend(&self.buffer);
        Ok(())
    }
}

impl fmt::Debug for MqttBytes {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "MqttBytes({:?})", self.as_ref())
    }
}

// No Display impl as raw bytes don't have a canonical display type

impl AsRef<[u8]> for MqttBytes {
    fn as_ref(&self) -> &[u8] {
        &self.buffer[LENGTH_FIELD_BYTES..]
    }
}

impl Deref for MqttBytes {
    type Target = [u8];
    fn deref(&self) -> &[u8] {
        self.as_ref()
    }
}

impl IntoBuf for MqttBytes {
    type Buf = Cursor<Bytes>;
    fn into_buf(self) -> Self::Buf {
        self.buffer.into_buf()
    }
}

impl<'a> IntoBuf for &'a MqttBytes {
    type Buf = Cursor<Bytes>;
    fn into_buf(self) -> Self::Buf {
        self.buffer.clone().into_buf()
    }
}

impl PartialEq<[u8]> for MqttBytes {
    fn eq(&self, other: &[u8]) -> bool {
        self.as_ref() == other
    }
}

impl PartialEq<MqttBytes> for [u8] {
    fn eq(&self, other: &MqttBytes) -> bool {
        self == other.as_ref()
    }
}

impl<'a> PartialEq<MqttBytes> for &'a [u8] {
    fn eq(&self, other: &MqttBytes) -> bool {
        *self == (*other).as_ref()
    }
}

impl<'a, T: ?Sized> PartialEq<&'a T> for MqttBytes
    where MqttBytes: PartialEq<T>
{
    fn eq(&self, other: &&'a T) -> bool {
        *self == **other
    }
}

/// Errors created when initializing `MqttBytes`
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum MqttBytesError {
    /// Data is longer than u16 length field can encode.
    TooLong,
}

impl MqttBytesError {
    #[doc(hidden)]
    pub fn __description(&self) -> &str {
        use self::MqttBytesError::*;
        match *self {
            TooLong => "bytes length is too long for u16 length field",
        }
    }
}

impl fmt::Display for MqttBytesError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl Error for MqttBytesError {
    fn description(&self) -> &str {
        self.__description()
    }

    fn cause(&self) -> Option<&Error> {
        None
    }
}

#[cfg(test)]
mod tests {
    use std::iter;
    use super::*;

    const TEST_DECODES: &[(&[u8], Option<&[u8]>)] = &[
        (b"\x00\x00", Some(b"")),
        (b"\x00\x05hello", Some(b"hello")),
        (b"\x00\x04this is longer than 4", Some(b"this")),
        (b"", None),
        (b"\x00", None),
        (b"\xFF\xFFNot enough characters", None),
    ];

    #[test]
    fn test_decoding() {
        for &(ref test_data, ref expected) in TEST_DECODES {
            let mut bytes = Bytes::from(&test_data[..]);
            let result = MqttBytes::decode(&mut bytes);
            if let Some(expected) = *expected {
                let unwrapped = result.unwrap().unwrap();
                assert_eq!(expected, unwrapped.as_ref());
                assert_eq!(expected, &*unwrapped);
            } else {
                assert_eq!(Ok(None), result);
            }
        }
    }

    const TEST_ENCODES: &[(&[u8], &[u8])] = &[
        (b"", b"\x00\x00"),
        (b"goodbye", b"\x00\x07goodbye"),
        (b"nulls\0are\0okay", b"\x00\x0Enulls\0are\0okay"),
    ];

    #[test]
    fn test_create_and_encode() {
        for &(ref test_bytes, expected) in TEST_ENCODES {
            let result = MqttBytes::new(test_bytes);
            let unwrapped = result.unwrap();
            let mut buffer = BytesMut::with_capacity(8 * 1024);
            buffer.clear();
            assert!(unwrapped.encode(&mut buffer).is_ok());
            assert_eq!(expected, buffer);
        }
    }

    #[test]
    fn test_encode_huge_bytes() {
        let test_bytes = iter::repeat(b'x').take(0xFFFF).collect::<Vec<u8>>();
        let result = MqttBytes::new(&test_bytes).unwrap();
        assert_eq!(0xFFFF, result.len());
        assert_eq!(test_bytes, &*result);
    }

    #[test]
    fn test_encode_too_long() {
        let test_bytes = iter::repeat(b'x').take(0x20000).collect::<Vec<u8>>();
        let result = MqttBytes::new(&test_bytes);
        assert_eq!(Err(MqttBytesError::TooLong), result);
    }
}
