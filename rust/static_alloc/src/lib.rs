// The MIT License (MIT)
//
// Copyright (c) 2015 Nick Stevens <nick@bitcurry.com>
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

//! Base64 binary encoder and decoder, implemented without using libstd

#![feature(core)]
extern crate core;

use core::slice::Chunks;

/// Available encoding character sets
#[derive(Clone, Copy)]
pub enum CharacterSet {
    /// The standard character set (uses `+` and `/`)
    Standard,
    /// The URL safe character set (uses `-` and `_`)
    UrlSafe
}

/// Available newline types
#[derive(Clone, Copy)]
pub enum Newline {
    /// A linefeed (i.e. Unix-style newline)
    LF,
    /// A carriage return and a linefeed (i.e. Windows-style newline)
    CRLF
}

/// Contains configuration parameters for `Base64Encoder` and Base64Decoder`.
#[derive(Clone, Copy)]
pub struct Config {
    /// Character set to use
    pub char_set: CharacterSet,
    /// Newline to use
    pub newline: Newline,
    /// True to pad output with `=` characters
    pub pad: bool,
    /// `Some(len)` to wrap lines at `len`, `None` to disable line wrapping
    pub line_length: Option<usize>
}

static STANDARD_CHARS: &'static[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ\
                                        abcdefghijklmnopqrstuvwxyz\
                                        0123456789+/";

static URLSAFE_CHARS: &'static[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ\
                                       abcdefghijklmnopqrstuvwxyz\
                                       0123456789-_";

pub struct Base64Encoder<'a> {
    chunks: Chunks<'a, u8>,
    buffer: [u8; 4],  // 3 bytes generates 4 characters
    buffer_idx: usize
}

impl <'a> Base64Encoder<'a> {

    /// Creates a new Base64Encoder
    pub fn new(input: &'a [u8]) -> Base64Encoder {
        Base64Encoder {
            chunks: input.chunks(3),
            buffer: [0; 4],
            buffer_idx: 4
        }
    }
}

impl <'a> Iterator for Base64Encoder<'a> {
    type Item = u8;

    fn next(&mut self) -> Option<u8> {
        if self.buffer_idx < self.buffer.len() {
            // Data available in output buffer
            self.buffer_idx += 1;
            Some(self.buffer[self.buffer_idx - 1])
        } else {
            if let Some(chunk) = self.chunks.next() {
                // Process the next hunk of data
                let combined: u32 =
                    0 | if chunk.len() >= 1 {
                        ((chunk[0] as u32) << 16)
                    } else {
                        0
                    } | if chunk.len() >= 2 {
                        ((chunk[1] as u32) << 8 )
                    } else {
                        0
                    } | if chunk.len() >= 3 {
                        ((chunk[2] as u32) << 0 )
                    } else {
                        0
                    };
                encode_chunk(combined, &mut self.buffer[..]);
                if chunk.len() <= 1 {
                    self.buffer[2] = '=' as u8;
                }
                if chunk.len() <= 2 {
                    self.buffer[3] = '=' as u8;
                }

                self.buffer_idx = 1;
                Some(self.buffer[0])
            } else {
                None
            }
        }
    }
}

fn encode_chunk(chunk: u32, output: &mut [u8]) {
    for (i, shift) in [18, 12, 6, 0].iter().enumerate() {
        let u: u8 = ((chunk >> shift) as u8) & 0b0011_1111;
        output[i] = match u {
             0...25 => b'A' + u,
            26...51 => b'a' + u - 26,
            52...61 => b'0' + u - 52,
                 62 => b'+',
                 63 => b'/',
                  _ => panic!("Boolean AND is broken!"),
        }
    }
}

pub struct Base64Decoder<'a> {
    chunks: Chunks<'a, u8>,
    buffer: [u8; 3],  // 4 characters generates 3 bytes
    buffer_idx: usize
}

impl <'a> Base64Decoder<'a> {
    pub fn new(input: &'a [u8]) -> Base64Decoder {
        Base64Decoder {
            chunks: input.chunks(4),
            buffer: [0; 3],
            buffer_idx: 3
        }
    }
}

// impl <'a> Iterator for Base64Decoder<'a> {
//     type Item = u8;

//     fn next(&mut self) -> Option<u8> {
//     }
// }

fn decode_chunk(chunk: &[u8], output: &mut [u8]) {
    for (i, value) in chunk.iter().enumerate() {
        output[i] = match value {
            b'A'...b'Z' => value - 0x41,
            b'a'...b'z' => value - 0x47,
            b'0'...b'9' => value + 0x04,
            b'+' | b'-' => 0x3E,
            b'/' | b'_' => 0x3F,
                    _ => 0xFF
        };
    }
}


#[cfg(test)]
mod test {

    use super::*;

    #[test]
    fn test_encoder_basic() {
        let test_wrapper = |s: &str| -> String {
            let encoder = Base64Encoder::new(s.as_bytes());
            String::from_utf8(encoder.collect()).unwrap()
        };
        assert_eq!(test_wrapper(""), "");
        assert_eq!(test_wrapper("f"), "Zg==");
        assert_eq!(test_wrapper("fo"), "Zm8=");
        assert_eq!(test_wrapper("foo"), "Zm9v");
        assert_eq!(test_wrapper("foob"), "Zm9vYg==");
        assert_eq!(test_wrapper("fooba"), "Zm9vYmE=");
        assert_eq!(test_wrapper("foobar"), "Zm9vYmFy");
    }

    // #[test]
    // fn test_to_base64_padding() {
    //     assert_eq!("f".as_bytes().to_base64(Config {pad: false, ..STANDARD}), "Zg");
    //     assert_eq!("fo".as_bytes().to_base64(Config {pad: false, ..STANDARD}), "Zm8");
    // }

    // #[test]
    // fn test_to_base64_url_safe() {
    //     assert_eq!([251, 255].to_base64(URL_SAFE), "-_8");
    //     assert_eq!([251, 255].to_base64(STANDARD), "+/8=");
    // }

    // #[test]
    // fn test_from_base64_basic() {
    //     assert_eq!("".from_base64().unwrap(), b"");
    //     assert_eq!("Zg==".from_base64().unwrap(), b"f");
    //     assert_eq!("Zm8=".from_base64().unwrap(), b"fo");
    //     assert_eq!("Zm9v".from_base64().unwrap(), b"foo");
    //     assert_eq!("Zm9vYg==".from_base64().unwrap(), b"foob");
    //     assert_eq!("Zm9vYmE=".from_base64().unwrap(), b"fooba");
    //     assert_eq!("Zm9vYmFy".from_base64().unwrap(), b"foobar");
    // }

    // #[test]
    // fn test_from_base64_bytes() {
    //     assert_eq!(b"Zm9vYmFy".from_base64().unwrap(), b"foobar");
    // }

    // #[test]
    // fn test_from_base64_newlines() {
    //     assert_eq!("Zm9v\r\nYmFy".from_base64().unwrap(),
    //                b"foobar");
    //     assert_eq!("Zm9vYg==\r\n".from_base64().unwrap(),
    //                b"foob");
    //     assert_eq!("Zm9v\nYmFy".from_base64().unwrap(),
    //                b"foobar");
    //     assert_eq!("Zm9vYg==\n".from_base64().unwrap(),
    //                b"foob");
    // }

    // #[test]
    // fn test_from_base64_urlsafe() {
    //     assert_eq!("-_8".from_base64().unwrap(), "+/8=".from_base64().unwrap());
    // }

    // #[test]
    // fn test_from_base64_invalid_char() {
    //     assert!("Zm$=".from_base64().is_err());
    //     assert!("Zg==$".from_base64().is_err());
    // }

    // #[test]
    // fn test_from_base64_invalid_padding() {
    //     assert!("Z===".from_base64().is_err());
    // }

    // #[test]
    // fn test_base64_random() {
    //     use rand::{thread_rng, Rng};

    //     for _ in 0..1000 {
    //         let times = thread_rng().gen_range(1, 100);
    //         let v = thread_rng().gen_iter::<u8>().take(times)
    //                             .collect::<Vec<_>>();
    //         assert_eq!(v.to_base64(STANDARD)
    //                     .from_base64()
    //                     .unwrap(),
    //                    v);
    //     }
    // }
}

