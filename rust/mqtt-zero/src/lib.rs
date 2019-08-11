// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

// #![allow(dead_code)]
// #![allow(unused_variables)]
// #![allow(unused_mut)]
// #![allow(unused_imports)]

//! Zero-copy implementation of MQTT protocol.

#[macro_use] extern crate bitflags;
#[macro_use] extern crate lazy_static;

extern crate bytes;

macro_rules! require_length {
    ($required:expr, $actual:expr) => {
        if $actual < $required {
            return Ok(None);
        }
    };
}

pub mod packet;
pub mod parse;
mod qos;

pub use self::qos::QoS;
pub use self::parse::DecodeBytes;
pub use self::parse::EncodeBytes;
