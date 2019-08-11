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
use std::str::FromStr;

use bytes::{Bytes, BytesMut, IntoBuf};

use parse::{DecodeBytes, EncodeBytes, MqttString, MqttStringError};

/// Specialization of `MqttString` with additional restrictions per rules for
/// client identifiers:
///
///   * Must be between 1 and 23 characters (inclusive)
///   * Must be valid UTF-8
///   * Must only consist of the characters [a-z], [A-Z], and [0-9]
#[derive(Clone, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ClientIdentifier(MqttString);

impl ClientIdentifier {
    /// Create a `ClientIdentifier` from the given string.
    ///
    /// Creates a new `ClientIdentifier` from the provided string reference.
    /// This method will return an error if the string does not meet the
    /// following restrictions:
    /// 
    ///   * Must be between 1 and 23 characters (inclusive)
    ///   * Must be valid UTF-8
    ///   * Must only consist of the characters [a-z], [A-Z], and [0-9]
    pub fn new<S: AsRef<str>>(s: S) -> Result<ClientIdentifier, ClientIdentifierError> {
        let mqtt_string = MqttString::new(s)?;
        if mqtt_string.len() < 1 || mqtt_string.len() > 23 {
            Err(ClientIdentifierError::InvalidLength)
        } else if !mqtt_string.chars().all(allowed_character) {
            Err(ClientIdentifierError::InvalidCharacters)
        } else {
            Ok(ClientIdentifier(mqtt_string))
        }
    }

    /// Create a `ClientIdentifier` from the given `Bytes` without checking
    /// validity.
    ///
    /// Creates a `ClientIdentifier` with no validity checking, which is why the
    /// function is `unsafe`. The `Bytes` buffer _must_ be exactly the length
    /// of the bytes object, _must_ have a correct two-byte length field,
    /// _must_ be valid UTF-8 that meets the requirements of the MQTT
    /// specification, and _must_ meet the additional MQTT specification
    /// requirements for client identifier allowed characters.
    pub unsafe fn from_bytes_unchecked(buffer: Bytes) -> ClientIdentifier {
        ClientIdentifier(MqttString::from_bytes_unchecked(buffer))
    }

    /// Returns the length of the string in bytes, not including length of
    /// header.
    pub fn len(&self) -> usize {
        self.as_ref().len()
    }

    /// Returns the total length of the encoded bytes, including the length of
    /// the header.
    pub fn encoded_len(&self) -> usize {
        self.0.encoded_len()
    }

    /// Returns a lightweight copy of this string's `Bytes` buffer (including
    /// length header).
    pub fn as_bytes(&self) -> Bytes {
        self.0.as_bytes()
    }

    /// Returns a slice over the bytes of the string (including length header).
    pub fn as_slice(&self) -> &[u8] {
        &self.0.as_slice()
    }

    /// Consumes the `ClientIdentifier`, returning the underlying `Bytes`.
    pub fn take(self) -> Bytes {
        self.0.take()
    }
}

// Allowed ClientIdentifier string characters: [0-9][a-z][A-Z]
fn allowed_character(c: char) -> bool {
    match c {
        'a'...'z' | 'A'...'Z' | '0'...'9' => true,
        _ => false,
    }
}

impl DecodeBytes for ClientIdentifier {
    type Error = ClientIdentifierError;
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error> {
        // Just decode as an `MqttString` and then check for allowed characters.
        if let Some(mqtt_string) = MqttString::decode(src)? {
            if mqtt_string.len() < 1 || mqtt_string.len() > 23 {
                Err(ClientIdentifierError::InvalidLength)
            } else if !mqtt_string.chars().all(allowed_character) {
                Err(ClientIdentifierError::InvalidCharacters)
            } else {
                Ok(Some(ClientIdentifier(mqtt_string)))
            }
        } else {
            Ok(None)
        }
    }
}

impl EncodeBytes for ClientIdentifier {
    type Error = ClientIdentifierError;
    fn encode(&self, dst: &mut BytesMut) -> Result<(), Self::Error> {
        self.0.encode(dst).map_err(Into::into)
    }
}

impl fmt::Debug for ClientIdentifier {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "ClientIdentifier({:?})", self.as_ref())
    }
}

impl fmt::Display for ClientIdentifier {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.as_ref())
    }
}

impl AsRef<str> for ClientIdentifier {
    fn as_ref(&self) -> &str {
        self.0.as_ref()
    }
}

impl Deref for ClientIdentifier {
    type Target = str;
    fn deref(&self) -> &str {
        self.0.as_ref()
    }
}

impl From<ClientIdentifier> for MqttString {
    fn from(val: ClientIdentifier) -> MqttString {
        val.0
    }
}

impl FromStr for ClientIdentifier {
    type Err = ClientIdentifierError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        ClientIdentifier::new(s)
    }
}

impl IntoBuf for ClientIdentifier {
    type Buf = Cursor<Bytes>;
    fn into_buf(self) -> Self::Buf {
        self.0.into_buf()
    }
}

impl<'a> IntoBuf for &'a ClientIdentifier {
    type Buf = Cursor<Bytes>;
    fn into_buf(self) -> Self::Buf {
        self.clone().into_buf()
    }
}

impl PartialEq<str> for ClientIdentifier {
    fn eq(&self, other: &str) -> bool {
        self.as_ref() == other
    }
}

impl PartialEq<ClientIdentifier> for str {
    fn eq(&self, other: &ClientIdentifier) -> bool {
        self == other.as_ref()
    }
}

/// Errors that may occur while parsing a `ClientIdentifier`.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ClientIdentifierError {
    /// Error parsing the string as an `MqttString`
    MqttStringError(MqttStringError),
    /// `ClientIdentifier` contains invalid character(s)
    InvalidCharacters,
    /// `ClientIdentifier` is not between 1 and 23 characters (inclusive)
    InvalidLength,
}

impl ClientIdentifierError {
    #[doc(hidden)]
    pub fn __description(&self) -> &str {
        use self::ClientIdentifierError::*;
        match *self {
            MqttStringError(ref inner) => inner.description(),
            InvalidCharacters => "string contains characters other than [0-9][a-z][A-Z]",
            InvalidLength => "string is not between 1 and 23 characters long",
        }
    }
}

impl fmt::Display for ClientIdentifierError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl Error for ClientIdentifierError {
    fn description(&self) -> &str {
        self.__description()
    }

    fn cause(&self) -> Option<&Error> {
        use self::ClientIdentifierError::*;
        match *self {
            MqttStringError(ref inner) => Some(inner),
            _ => None,
        }
    }
}

impl From<MqttStringError> for ClientIdentifierError {
    fn from(e: MqttStringError) -> ClientIdentifierError {
        ClientIdentifierError::MqttStringError(e)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    enum DecodeResult {
        Decoded(&'static str, usize),
        DecodeIncomplete,
        DecodeErrored,
    }

    use self::DecodeResult::*;

    const TEST_DECODES: &[(&[u8], DecodeResult)] = &[
        (b"\x00\x05hello", Decoded("hello", 5)),
        (b"\x00\x04thisislongerthan4", Decoded("this", 4)),
        (b"\x00", DecodeIncomplete),
        (b"\xFF\xFFNotenoughcharacters", DecodeIncomplete),
        (b"\x00\x00", DecodeErrored), // can't be zero characters
        (b"\x00\x20Thisstringismorethan23characters", DecodeErrored),
        (b"\x00\x10Longerthan23butonly16count", Decoded("Longerthan23buto", 16)),
        (b"\x00\x11This'isnotallowed", DecodeErrored),
        (b"\x00\x11This_isnotallowed", DecodeErrored),
        (b"\x00\x11This?isnotallowed", DecodeErrored),
        (b"\x00\x09nullbyte\x00", DecodeErrored),
        (b"\x00\x11controlcharacter\x1D", DecodeErrored),
        (b"\x00\x0Fnoncharacter\xEF\xB7\xAF", DecodeErrored),
        (b"\x00\x0Elonesurrogate\xED\xA0\x80", DecodeErrored),
    ];

    #[test]
    fn test_decoding() {
        for &(ref test_data, ref expected) in TEST_DECODES {
            let mut bytes = Bytes::from(&test_data[..]);
            let result = ClientIdentifier::decode(&mut bytes);
            println!("{:?}", test_data);
            match *expected {
                Decoded(expected, expected_len) => {
                    let unwrapped = result.unwrap().unwrap();
                    let total_len = expected_len + 2;
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
        ("", CreateErrored),
        ("no spaces", CreateErrored),
        ("no-good", CreateErrored),
        ("thisoneiswaywaywaytoolong", CreateErrored),
        ("null byte:\u{0}", CreateErrored),
        ("control character:\u{1D}", CreateErrored),
        ("non-character:\u{FDEF}", CreateErrored),
    ];

    #[test]
    fn test_from_str() {
        for &(ref test_str, ref expected) in TEST_ENCODES {
            let result = test_str.parse::<ClientIdentifier>();
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

}
