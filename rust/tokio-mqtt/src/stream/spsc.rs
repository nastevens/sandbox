//! A signle-producer, single-consumer, futures-aware, FIFO queue with back
//! pressure, for use communicating within a single type.

use std::any::Any;
use std::collections::VecDeque;
use std::error::Error;
use std::fmt;
use std::mem;

use futures::task::{self, Task};
use futures::{Async, AsyncSink, Poll, StartSend, Sink, Stream};

/// Creates a bounded in-memory channel with buffered storage.
///
/// This method creates concrete implementations of the `Stream` and `Sink`
/// traits which can be used to communicate a stream of values between tasks
/// with backpressure. The channel capacity is exactly `buffer`. On average,
/// sending a message through this channel performs no dynamic allocation.
pub fn channel<T>(buffer: usize) -> SpscQueue<T> {
    channel_(Some(buffer))
}

fn channel_<T>(buffer: Option<usize>) -> SpscQueue<T> {
    SpscQueue {
        buffer: VecDeque::new(),
        capacity: buffer,
        blocked_senders: VecDeque::new(),
        blocked_recv: None,
        state: State::Open,
    }
}

/// Possible states of a receiver. We're either Open (can receive more messages)
/// or we're closed with a list of messages we have left to receive.
#[derive(Debug)]
enum State<T> {
    Open,
    Closed(VecDeque<T>),
}

#[derive(Debug)]
pub struct SpscQueue<T> {
    buffer: VecDeque<T>,
    capacity: Option<usize>,
    blocked_senders: VecDeque<Task>,
    blocked_recv: Option<Task>,
    state: State<T>,
}

impl<T> SpscQueue<T> {
    fn do_send(&mut self, msg: T) -> StartSend<T, SendError<T>> {
        match self.capacity {
            Some(capacity) if self.buffer.len() == capacity => {
                self.blocked_senders.push_back(task::park());
                Ok(AsyncSink::NotReady(msg))
            }
            _ => {
                self.buffer.push_back(msg);
                if let Some(task) = self.blocked_recv.take() {
                    task.unpark();
                }
                Ok(AsyncSink::Ready)
            }
        }
    }

    /// Closes the receiving half
    ///
    /// This prevents any further messages from being sent on the channel while
    /// still enabling the receiver to drain messages that are buffered.
    pub fn close(&mut self) {
        let (blockers, items) = match self.state {
            State::Open => {
                let items = mem::replace(&mut self.buffer, VecDeque::new());
                let blockers = mem::replace(&mut self.blocked_senders, VecDeque::new());
                (blockers, items)
            }
            State::Closed(_) => return,
        };
        self.state = State::Closed(items);
        for task in blockers {
            task.unpark();
        }
    }
}

impl<T> Sink for SpscQueue<T> {
    type SinkItem = T;
    type SinkError = SendError<T>;

    fn start_send(&mut self, msg: T) -> StartSend<T, SendError<T>> {
        self.do_send(msg)
    }

    fn poll_complete(&mut self) -> Poll<(), SendError<T>> {
        Ok(Async::Ready(()))
    }

    fn close(&mut self) -> Poll<(), SendError<T>> {
        Ok(Async::Ready(()))
    }
}

impl<T> Stream for SpscQueue<T> {
    type Item = T;
    type Error = ();

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        if let State::Closed(ref mut items) = self.state  {
            return Ok(Async::Ready(items.pop_front()))
        }

        if let Some(msg) = self.buffer.pop_front() {
            if let Some(task) = self.blocked_senders.pop_front() {
                task.unpark();
            }
            Ok(Async::Ready(Some(msg)))
        } else {
            self.blocked_recv = Some(task::park());
            Ok(Async::NotReady)
        }
    }
}

impl<T> Drop for SpscQueue<T> {
    fn drop(&mut self) {
        self.close();
    }
}

/// The transmission end of an unbounded channel.
///
/// This is created by the `unbounded` function.
#[derive(Debug)]
pub struct UnboundedSpscQueue<T>(SpscQueue<T>);

impl<T> Sink for UnboundedSpscQueue<T> {
    type SinkItem = T;
    type SinkError = SendError<T>;

    fn start_send(&mut self, msg: T) -> StartSend<T, SendError<T>> {
        self.0.start_send(msg)
    }
    fn poll_complete(&mut self) -> Poll<(), SendError<T>> {
        Ok(Async::Ready(()))
    }
    fn close(&mut self) -> Poll<(), SendError<T>> {
        Ok(Async::Ready(()))
    }
}

impl<T> UnboundedSpscQueue<T> {
    /// Sends the provided message along this channel.
    ///
    /// This is an unbounded sender, so this function differs from `Sink::send`
    /// by ensuring the return type reflects that the channel is always ready to
    /// receive messages.
    pub fn send(&mut self, msg: T) -> Result<(), SendError<T>> {
        self.0.buffer.push_back(msg);
        if let Some(task) = self.0.blocked_recv.take() {
            task.unpark();
        }
        Ok(())
    }

    pub fn close(&mut self) {
        self.0.close();
    }
}

impl<T> Stream for UnboundedSpscQueue<T> {
    type Item = T;
    type Error = ();

    fn poll(&mut self) -> Poll<Option<Self::Item>, Self::Error> {
        self.0.poll()
    }
}

/// Creates an unbounded in-memory channel with buffered storage.
///
/// Identical semantics to `channel`, except with no limit to buffer size.
pub fn unbounded<T>() -> UnboundedSpscQueue<T> {
    UnboundedSpscQueue(channel_(None))
}

/// Error type for sending, used when the receiving end of a channel is
/// dropped
pub struct SendError<T>(T);

impl<T> fmt::Debug for SendError<T> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.debug_tuple("SendError")
            .field(&"...")
            .finish()
    }
}

impl<T> fmt::Display for SendError<T> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "send failed because receiver is gone")
    }
}

impl<T: Any> Error for SendError<T> {
    fn description(&self) -> &str {
        "send failed because receiver is gone"
    }
}

impl<T> SendError<T> {
    /// Returns the message that was attempted to be sent but failed.
    pub fn into_inner(self) -> T {
        self.0
    }
}
