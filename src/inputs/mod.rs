mod resolve;
mod rng;
mod streams;

pub use resolve::resolve_inputs;

#[cfg(test)]
#[path = "resolve_tests.rs"]
mod resolve_tests;
