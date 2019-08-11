// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use parse::{MqttBytesError, MqttStringError, RemainingLengthError};

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PacketError {
    MqttBytesError(MqttBytesError),
    MqttStringError(MqttStringError),
    RemainingLengthError(RemainingLengthError),
    InvalidHeader,
}

impl From<MqttBytesError> for PacketError {
    fn from(e: MqttBytesError) -> PacketError {
        PacketError::MqttBytesError(e)
    }
}

impl From<MqttStringError> for PacketError {
    fn from(e: MqttStringError) -> PacketError {
        PacketError::MqttStringError(e)
    }
}

impl From<RemainingLengthError> for PacketError {
    fn from(e: RemainingLengthError) -> PacketError {
        PacketError::RemainingLengthError(e)
    }
}
