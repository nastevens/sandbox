// Copyright (c) 2017, Nick Stevens <nick@bitcurry.com>
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/license/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option.  This file may not be copied, modified, or distributed
// except according to those terms.

extern crate tokio_mqtt;
extern crate futures;
extern crate tokio_core;

fn main() {
}

// use tokio_core::net::TcpStream;
// use tokio_core::reactor::Core;

// fn main() {
//     let mut reactor = Core::new().unwrap();

//     let client = MqttClient::new(reactor.handle());
//     let transport = TcpStream::connect("127.0.0.1:8080".parse().unwrap(), reactor.handle());

//     let app = transport.and_then(move |conn| {
//         client.connect(conn, MqttOptions::default())
//             .and_then(|client| {
//                 let s1 = client.subscriber("hello/earth", StringEncoder);
//                 let s2 = client.subscriber("hello/mars", StringEncoder);

//                 handle.spawn_fn(move || {
//                     s1.for_each(|msg| {
//                         // do something
//                     })
//                 });

//                 handle.spawn_fn(move || {
//                     s2.for_each(|msg| {
//                         // do something else
//                     })
//                 });
//                 client.disconnect()
//             })
//     });

//     reactor.run(app);
// }
