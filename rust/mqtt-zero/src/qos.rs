// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

/// Quality of service as described in the MQTT spec section 4.3.
#[derive(Clone, Copy, Debug, Hash, Eq, Ord, PartialEq, PartialOrd)]
pub enum QoS {
    /// Packet is delivered either once or not at all.
    AtMostOnce,
    /// Packet is delivered at least once, but may be delivered multiple times.
    AtLeastOnce,
    /// Packet is delivered exactly once.
    ExactlyOnce,
}
