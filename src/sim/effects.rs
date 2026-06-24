use crate::model::AttributedEffect;

pub fn push_effect(
  effects: &mut Vec<AttributedEffect>,
  source: &'static str,
  metric: &'static str,
  delta: i32,
) {
  effects.push(AttributedEffect {
    source,
    metric,
    delta,
  });
}
