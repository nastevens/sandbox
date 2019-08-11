// Copyright (c) 2017 SmartThings. All Rights Reserved.

use spin::Mutex as Spinlock;

pub trait RateLimiter {
    /// Attempts to claim a rate-limiting "slot", returning `true` if the
    /// operation can move ahead or `false` if the operation should be delayed.
    fn rate_limit_gate(&self) -> bool;
}

pub struct NoopRateLimiter {
    fn rate_limit_gate(&self) -> bool {
        true
    }
}

pub struct BucketRateLimiter {
    // Interval between adding tokens
    interval: Duration,
    // Tokens to add to the pool per interval
    quantum: usize,
    // Maximum number of tokens to allow in bucket
    capacity: usize,
    // Last update time
    last: Spinlock<Instant>,
    // Bucket
    bucket: AtomicUsize,
}

impl BucketRateLimiter {
    pub fn new(quantum: usize, interval: Duration, capacity: usize) -> BucketRateLimiter {
        BucketRateLimiter {
            interval: interval,
            quantum: quantum,
            capacity: capacity,
            last: Spinlock::new(Instant::now()),
            bucket: 0.0,
        }
    }
    
    fn fill(&self) {
        let now = Instant::now();
        let last = self.last.lock();
        let ticks = self.ticks(self.last.elapsed());
        self.bucket += ticks * (quantum as f64)
    }

    // Calculates the number of quantums that have occurred in the given
    // duration.
    fn ticks(&self, duration: Duration) -> f64 {

    }

    fn acquire_token(&self) -> bool {
        // Since multiple threads can be accessing, it would be possible for
        // two decrements to occur at the same time, leading to values 1->0,
        // 0->-1, which would panic. Order would still be maintained and
        // everything, but the value would be unexpected.
        //
        // So instead, we need to load the value currently in the bucket,
        // decrement it ourselves (checking for 0), and do a swap to try and
        // replace it. That will tell us if someone else has already changed it
        // underneath us, and we re-run the operation.
        // `
        // The reason we can't just do AcqRel on an atomic sub is again because
        // of the zero case. Without checking first that the value > 0, we
        // could panic. But checking and then doing the sub still has the race
        // condition that the value was changed between the check and the
        // update. We prevent this case with the swap.
        loop {
            let current = self.bucket.load(Ordering::Acquire);
            let new = if current > 0 { current - 1 } else { return false };
            let retval = self.bucket.compare_and_swap(current, new, Ordering::AcqRel);
            if retval == current { return true }
        }
    }
}

impl RateLimiter for BucketRateLimiter {
    fn rate_limit_gate(&self) -> bool {
        if self.acquire_token() {
            true
        } else {
            self.fill();
            false
        }
    }
}

    /// Request permission to perform an update, returning true if the update
    /// is allowed based on current rate limits.
    pub fn gate_update(&self) -> bool {
        if let Some(max_rate) = self.max_rate() {
            if self.inner.update_count.load(Ordering::Relaxed) < max_rate {
                self.inner.update_count.fetch_add(1, Ordering::Relaxed);
                true
            } else {
                // See if the update count can be cleared to make space for
                // this update.
                if self.try_clear_update_count() {
                    self.inner.update_count.fetch_add(1, Ordering::Relaxed);
                    true
                } else {
                    false
                }
            }
        } else {
            true
        }
    }

    // See if the update count is due to be cleared, returning `true` if it was
    // cleared.
    fn try_clear_update_count(&self) -> bool {
        let need_clear = self.inner.rate_last_cleared.read().map(|last_cleared| {
            last_cleared.elapsed() > *UPDATE_THROTTLE_PERIOD
        }).unwrap_or(false);

        if need_clear {
            let _ = self.inner.rate_last_cleared.write().map(|mut last_cleared| {
                *last_cleared = Instant::now()
            });
            self.inner.update_count.store(0, Ordering::Relaxed);
            true
        } else {
            false
        }
    }

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
    }
}
