pub(crate) fn stream_rng(seed: u64, turn: u32, stream_id: u32) -> u64 {
  let state = seed
    .wrapping_add((turn as u64).wrapping_mul(0x517c_c1b7_2722_0a95))
    .wrapping_add((stream_id as u64).wrapping_mul(0x6c62_272e_07bb_0142));
  splitmix64(state)
}

fn splitmix64(mut z: u64) -> u64 {
  z = z.wrapping_add(0x9e37_79b9_7f4a_7c15);
  z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
  z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
  z ^ (z >> 31)
}

pub(crate) fn bounded_u32(value: u64, lo: u32, hi: u32) -> u32 {
  debug_assert!(lo <= hi, "bounded_u32: hi must be >= lo");
  let span = (hi - lo + 1) as u64;
  lo + (value % span) as u32
}

pub(crate) fn bounded_i32(value: u64, lo: i32, hi: i32) -> i32 {
  debug_assert!(lo <= hi, "bounded_i32: hi must be >= lo");
  let span = (hi - lo + 1) as u64;
  lo + (value % span) as i32
}
