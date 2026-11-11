//! When the desktop moves on to another theme, and which one the lock screen shows.
//!
//! Neither type reads a clock or draws random numbers itself: the caller passes the time that went by
//! and a function `pick(n)` that returns a number below `n`. That keeps the rules testable and the
//! crate free of dependencies.

use std::time::Duration;

use crate::tokens::THEME_CYCLE;

/// Another index than `current`, out of `count`, with every other index equally likely.
/// With fewer than two themes it returns `current`.
pub fn other(current: usize, count: usize, pick: &mut impl FnMut(usize) -> usize) -> usize {
    if count < 2 {
        return current;
    }
    let r = pick(count - 1) % (count - 1);
    if r >= current { r + 1 } else { r }
}

/// The desktop theme cycle: every `period` (10 minutes) another theme, unless the theme is kept.
///
/// The count goes on while the theme is kept. Keeping a theme and letting it go again therefore
/// does not change the theme at once; it changes when the running period is over.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Cycle {
    period: Duration,
    elapsed: Duration,
    current: usize,
    count: usize,
    kept: bool,
}

impl Cycle {
    /// A cycle over `count` themes, starting at `current`, with the period of the design system.
    pub fn new(current: usize, count: usize) -> Self {
        Self::with_period(current, count, THEME_CYCLE)
    }

    pub fn with_period(current: usize, count: usize, period: Duration) -> Self {
        assert!(!period.is_zero(), "a cycle needs a period");
        Self { period, elapsed: Duration::ZERO, current, count, kept: false }
    }

    pub fn current(&self) -> usize {
        self.current
    }

    pub fn kept(&self) -> bool {
        self.kept
    }

    /// Keep the theme (the K key in the theme picker) or let it go. The count is not touched.
    pub fn set_kept(&mut self, kept: bool) {
        self.kept = kept;
    }

    /// Time until the running period is over.
    pub fn remaining(&self) -> Duration {
        self.period - self.elapsed
    }

    /// A theme chosen by hand. It starts a new period.
    pub fn choose(&mut self, index: usize) {
        self.current = index;
        self.elapsed = Duration::ZERO;
    }

    /// Lets `dt` go by. Returns the new theme when the period ran out and the theme is not kept.
    /// After a long pause (suspend) it changes once, not once for every period that was missed.
    pub fn tick(&mut self, dt: Duration, pick: &mut impl FnMut(usize) -> usize) -> Option<usize> {
        self.elapsed += dt;
        if self.elapsed < self.period {
            return None;
        }
        self.elapsed = Duration::from_nanos((self.elapsed.as_nanos() % self.period.as_nanos()) as u64);
        if self.kept {
            return None;
        }
        self.current = other(self.current, self.count, pick);
        Some(self.current)
    }
}

/// The lock screen: another theme at every lock, never the same twice in a row.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct LockRotation {
    last: Option<usize>,
}

impl LockRotation {
    pub fn new() -> Self {
        Self::default()
    }

    /// The theme for this lock.
    pub fn next(&mut self, count: usize, pick: &mut impl FnMut(usize) -> usize) -> usize {
        let i = match self.last {
            Some(last) => other(last, count, pick),
            None => pick(count.max(1)) % count.max(1),
        };
        self.last = Some(i);
        i
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const MIN: Duration = Duration::from_secs(60);

    fn first(n: usize) -> usize {
        let _ = n;
        0
    }

    #[test]
    fn other_never_returns_current_and_reaches_all() {
        for current in 0..8 {
            let mut seen = [false; 8];
            for r in 0..7 {
                let i = other(current, 8, &mut |_| r);
                assert_ne!(i, current);
                seen[i] = true;
            }
            assert_eq!(seen.iter().filter(|s| **s).count(), 7);
        }
        assert_eq!(other(0, 1, &mut first), 0);
    }

    #[test]
    fn changes_every_ten_minutes() {
        let mut c = Cycle::new(0, 8);
        assert_eq!(c.tick(9 * MIN, &mut first), None);
        assert_eq!(c.tick(MIN, &mut first), Some(1));
        assert_eq!(c.remaining(), 10 * MIN);
    }

    #[test]
    fn keeping_and_releasing_does_not_change_at_once() {
        let mut c = Cycle::new(0, 8);
        c.tick(4 * MIN, &mut first);
        c.set_kept(true);
        c.set_kept(false);
        assert_eq!(c.current(), 0);
        assert_eq!(c.remaining(), 6 * MIN);
    }

    #[test]
    fn the_count_goes_on_while_kept() {
        let mut c = Cycle::new(0, 8);
        c.set_kept(true);
        assert_eq!(c.tick(13 * MIN, &mut first), None);
        assert_eq!(c.remaining(), 7 * MIN);
        c.set_kept(false);
        assert_eq!(c.tick(7 * MIN, &mut first), Some(1));
    }

    #[test]
    fn choosing_by_hand_starts_a_new_period() {
        let mut c = Cycle::new(0, 8);
        c.tick(8 * MIN, &mut first);
        c.choose(5);
        assert_eq!(c.current(), 5);
        assert_eq!(c.remaining(), 10 * MIN);
    }

    #[test]
    fn a_long_pause_changes_once() {
        let mut c = Cycle::new(3, 8);
        let mut calls = 0;
        let mut pick = |n: usize| {
            calls += 1;
            n - 1
        };
        assert_eq!(c.tick(65 * MIN, &mut pick), Some(7));
        assert_eq!(calls, 1);
        assert_eq!(c.remaining(), 5 * MIN);
    }

    #[test]
    fn the_lock_screen_never_repeats() {
        let mut lock = LockRotation::new();
        let mut last = lock.next(8, &mut first);
        for r in [0, 6, 3, 0, 0, 6] {
            let i = lock.next(8, &mut |_| r);
            assert_ne!(i, last);
            last = i;
        }
    }
}
