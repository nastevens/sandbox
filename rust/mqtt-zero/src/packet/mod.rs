// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

const FIXED_HEADER_LENGTH: usize = 2;

mod connack;
mod connect;
mod disconnect;
mod error;
mod packet;

pub use self::connect::{ConnectPacket, KeepAlive};
pub use self::connack::ConnAckPacket;
pub use self::disconnect::DisconnectPacket;
pub use self::packet::{MqttPacket, MqttPacketType};
