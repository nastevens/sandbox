// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use bytes::{Bytes, BytesMut};

mod bytes;
mod client_id;
mod length;
mod string;

pub use self::bytes::{MqttBytes, MqttBytesError};
pub use self::client_id::ClientIdentifier;
pub use self::length::{RemainingLength, RemainingLengthError};
pub use self::string::{MqttString, MqttStringError};

pub trait EncodeBytes {
    /// The type of encoding errors.
    type Error;

    /// Attempts to encode this item into the buffer provided.
    ///
    /// This method will encode `self` into the byte buffer provided by `buf`.
    fn encode(&self, buf: &mut BytesMut) -> Result<(), Self::Error>;
}

pub trait DecodeBytes: Sized {
    /// The type of decoding errors.
    type Error;

    /// Attempts to decode an item from the provided buffer of bytes.
    ///
    /// If the bytes look valid, but an item isn't fully available yet, then
    /// `Ok(None)` is returned. This indicates that more bytes are needed
    /// before calling this method again.
    ///
    /// If an entire item is available, then this instance will remove those
    /// bytes from the buffer provided and return them as a decoded
    /// item. Note that removing bytes from the provided buffer doesn't always
    /// necessarily copy the bytes, so this should be an efficient operation in
    /// most circumstances.
    ///
    /// Note that the bytes provided may be empty.
    ///
    /// Finally, if the bytes in the buffer are malformed then an error should
    /// be returned indicating why.
    fn decode(src: &mut Bytes) -> Result<Option<Self>, Self::Error>;
}
