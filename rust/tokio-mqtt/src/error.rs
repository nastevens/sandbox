// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

use std::io;

pub enum MqttError {
    Other(String),
    IoError(io::Error),
    Cancelled,
    // ParseError(ParseError),
}

impl From<io::Error> for MqttError {
    fn from(e: io::Error) -> MqttError {
        MqttError::IoError(e)
    }
}

// impl From<ParseError> for MqttError {
//     fn from(e: ParseError) -> MqttError {
//         MqttError::ParseError(e)
//     }
// }
