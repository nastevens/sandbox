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
use std::str::{self, FromStr, Utf8Error};

use bytes::{Bytes, BytesMut, BigEndian, Buf, BufMut, IntoBuf};

use parse::{DecodeBytes, EncodeBytes};

// Leading byte field is a constant fixed 2 bytes
const LENGTH_FIELD_BYTES: usize = 2;

/// Length-prefixed UTF-8 string per MQTT v3.1.1 section 1.5.3
///
/// # Examples
///
/// ```
/// use mqtt_zero::parse::MqttString;
/// let string = MqttString::new("mqtt").unwrap();
/// assert_eq!(&b"\x00\x04mqtt"[..], string.as_slice());
/// ```
#[derive(Clone, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct MqttString {
    buffer: Bytes,
}

impl MqttString {
    /// Create an MqttString from the given string reference.
    ///
    /// Creates a new MqttString from the provided string reference.
    ///
    /// This method will return an error if the string contains characters
    /// prohibited by the MQTT spec:
    ///
    ///   * U+0000..U+001F - control characters
    ///   * U+007F..U+009F - control characters
    ///   * U+FDD0..U+FDEF - not a character
    ///   * U+FFFE..U+FFFF - not a character
    pub fn new<S: AsRef<str>>(s: S) -> Result<MqttString, MqttStringError> {
        let s = s.as_ref();
        if s.len() > 0xFFFF {
            Err(MqttStringError::TooLong)
        } else if s.contains(forbidden_character) {
            Err(MqttStringError::ForbiddenCharacter)
        } else {
            let mut parsed = BytesMut::with_capacity(LENGTH_FIELD_BYTES + s.len());
            parsed.put_u16::<BigEndian>(s.len() as u16);
            parsed.put(s.as_bytes());
            Ok(MqttString {
                buffer: parsed.freeze(),
            })
        }
    }

    /// Create an `MqttString` from the given `Bytes` without checking validity.
    ///
    /// Creates an `MqttString` with no validity checking, which is why the
    /// function is `unsafe`. The `Bytes` buffer _must_ be exactly the length
    /// of the bytes object, _must_ have a correct two-byte length field, and
    /// _must_ be valid UTF-8 that meets the requirements of the MQTT
    /// specification.
    pub unsafe fn from_bytes_unchecked(buffer: Bytes) -> MqttString {
        MqttString { buffer }
    }

    /// Returns the length of the string in bytes, not including length of
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

    /// Returns a slice over the bytes of the string (including length header).
    pub fn as_slice(&self) -> &[u8] {
        &self.buffer[..]
    }

    /// Consumes the `MqttString`, returning the underlying `Bytes`.
    pub fn take(self) -> Bytes {
        self.buffer
    }
}

// Forbidden MQTT string characters:
//     U+0000..U+001F - control characters
//     U+007F..U+009F - control characters
//     U+FDD0..U+FDEF - not a character
//     U+FFFE..U+FFFF - not a character
fn forbidden_character(c: char) -> bool {
    match c {
        '\u{0000}'...'\u{001F}' => true,
        '\u{007F}'...'\u{009F}' => true,
        '\u{FDD0}'...'\u{FDEF}' => true,
        '\u{FFFE}'...'\u{FFFF}' => true,
        _ => false,
    }
}

impl DecodeBytes for MqttString {
    type Error = MqttStringError;
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error> {
        // Verify data represents an MQTT string:
        //   - Big-endian u16 at start gives length
        //   - Bytes after length form valid UTF-8 string
        //   - Cannot contain forbidden characters (see `forbidden_characters`)
        let length = {
            let mut buf = Cursor::new(&src);
            require_length!(LENGTH_FIELD_BYTES, buf.remaining());
            let string_len = buf.get_u16::<BigEndian>() as usize;
            require_length!(string_len, buf.remaining());
            LENGTH_FIELD_BYTES + string_len
        };

        let split_buf = src.split_to(length);
        let string_buf = split_buf.slice_from(LENGTH_FIELD_BYTES);
        if str::from_utf8(&string_buf[..])?.contains(forbidden_character) {
            Err(MqttStringError::ForbiddenCharacter)
        } else {
            Ok(Some(MqttString { buffer: split_buf }))
        }
    }
}

impl EncodeBytes for MqttString {
    type Error = MqttStringError;
    fn encode(&self, dst: &mut BytesMut) -> Result<(), Self::Error> {
        dst.extend(&self.buffer);
        Ok(())
    }
}

impl fmt::Debug for MqttString {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "MqttString({:?})", self.as_ref())
    }
}

impl fmt::Display for MqttString {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.as_ref())
    }
}

impl AsRef<str> for MqttString {
    fn as_ref(&self) -> &str {
        // UTF-8 validity is established at initialization
        unsafe {
            str::from_utf8_unchecked(&self.buffer[LENGTH_FIELD_BYTES..])
        }
    }
}

impl Deref for MqttString {
    type Target = str;
    fn deref(&self) -> &str {
        self.as_ref()
    }
}

impl FromStr for MqttString {
    type Err = MqttStringError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        MqttString::new(s)
    }
}

impl IntoBuf for MqttString {
    type Buf = Cursor<Bytes>;
    fn into_buf(self) -> Self::Buf {
        self.buffer.into_buf()
    }
}

impl<'a> IntoBuf for &'a MqttString {
    type Buf = Cursor<Bytes>;
    fn into_buf(self) -> Self::Buf {
        self.buffer.clone().into_buf()
    }
}

impl PartialEq<str> for MqttString {
    fn eq(&self, other: &str) -> bool {
        self.as_ref() == other
    }
}

impl PartialEq<MqttString> for str {
    fn eq(&self, other: &MqttString) -> bool {
        self == other.as_ref()
    }
}

/// Errors created when initializing `MqttString`s
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum MqttStringError {
    /// String contains invalid UTF-8 characters.
    Utf8Error(Utf8Error),
    /// String contains characters prohibited by MQTT spec section 1.5.3.
    ForbiddenCharacter,
    /// String is longer than u16 length field can encode.
    TooLong,
}

impl MqttStringError {
    #[doc(hidden)]
    pub fn __description(&self) -> &str {
        use self::MqttStringError::*;
        match *self {
            Utf8Error(ref inner) => inner.description(),
            ForbiddenCharacter => "string contains a forbidden character",
            TooLong => "string is too long",
        }
    }
}

impl fmt::Display for MqttStringError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl Error for MqttStringError {
    fn description(&self) -> &str {
        self.__description()
    }

    fn cause(&self) -> Option<&Error> {
        use self::MqttStringError::*;
        match *self {
            Utf8Error(ref inner) => Some(inner),
            _ => None,
        }
    }
}

impl From<Utf8Error> for MqttStringError {
    fn from(e: Utf8Error) -> MqttStringError {
        MqttStringError::Utf8Error(e)
    }
}

#[cfg(test)]
mod tests {
    use std::iter;
    use super::*;

    enum DecodeResult {
        Decoded(&'static str, usize),
        DecodeIncomplete,
        DecodeErrored,
    }

    use self::DecodeResult::*;

    const TEST_DECODES: &[(&[u8], DecodeResult)] = &[
        (b"\x00\x00", Decoded("", 0)),
        (b"\x00\x05hello", Decoded("hello", 5)),
        (b"\x00\x04this is longer than 4", Decoded("this", 4)),
        (b"\x00", DecodeIncomplete),
        (b"\xFF\xFFNot enough characters", DecodeIncomplete),
        (b"\x00\x0Bnull byte:\x00", DecodeErrored),
        (b"\x00\x13control character:\x1D", DecodeErrored),
        (b"\x00\x11non-character:\xEF\xB7\xAF", DecodeErrored),
        (b"\x00\x10lone surrogate:\xED\xA0\x80", DecodeErrored),
    ];

    #[test]
    fn test_decoding() {
        for &(ref test_data, ref expected) in TEST_DECODES {
            let mut bytes = Bytes::from(&test_data[..]);
            let result = MqttString::decode(&mut bytes);
            match *expected {
                Decoded(expected, expected_len) => {
                    let unwrapped = result.unwrap().unwrap();
                    let total_len = expected_len + LENGTH_FIELD_BYTES;
                    assert_eq!(expected, unwrapped.as_ref());
                    assert_eq!(expected, &*unwrapped);
                    assert_eq!(&test_data[..total_len], unwrapped.as_slice());
                }
                DecodeIncomplete => assert_eq!(Ok(None), result),
                DecodeErrored => assert!(result.is_err()),
            }
        }
    }

    enum CreateAndEncodeResult {
        Encoded(&'static [u8]),
        CreateErrored,
    }

    use self::CreateAndEncodeResult::*;

    const TEST_ENCODES: &[(&str, CreateAndEncodeResult)] = &[
        ("goodbye", Encoded(b"\x00\x07goodbye")),
        ("null byte:\u{0}", CreateErrored),
        ("control character:\u{1D}", CreateErrored),
        ("non-character:\u{FDEF}", CreateErrored),
    ];

    #[test]
    fn test_create_and_encode() {
        for &(ref test_str, ref expected) in TEST_ENCODES {
            let result = test_str.parse::<MqttString>();
            match *expected {
                Encoded(expected) => {
                    let unwrapped = result.unwrap();
                    let mut buffer = BytesMut::with_capacity(8 * 1024);
                    buffer.clear();
                    assert!(unwrapped.encode(&mut buffer).is_ok());
                    assert_eq!(expected, buffer);
                }
                CreateErrored => {
                    assert!(result.is_err());
                }
            }
        }
    }

    #[test]
    fn test_from_str_huge() {
        let test_string = iter::repeat('x').take(0xFFFF).collect::<String>();
        let result = test_string.parse::<MqttString>().unwrap();
        assert_eq!(0xFFFF, result.len());
        assert_eq!(test_string, &*result);
        assert_eq!(&b"\xFF\xFF"[..], &result.as_slice()[..2]);
    }

    #[test]
    fn test_from_str_too_long() {
        let test_string = iter::repeat('x').take(0x20000).collect::<String>();
        let result = test_string.parse::<MqttString>();
        assert_eq!(Err(MqttStringError::TooLong), result);
    }
}
