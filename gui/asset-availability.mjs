const KNOWN_FAILURES = new Set(["missing", "failed", "malformed", "unavailable"]);

function text(value, fallback = "Unavailable") {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

export function normalizeAssetAvailability(result) {
  if (result === true || result === "loaded") {
    return Object.freeze({ status: "loaded", usable: true, reason: null });
  }
  if (result === null || result === undefined) {
    return Object.freeze({ status: "missing", usable: false, reason: "missing" });
  }
  if (result === false) {
    return Object.freeze({ status: "failed", usable: false, reason: "failed" });
  }
  if (typeof result === "string") {
    const status = result.trim().toLowerCase();
    if (status === "loaded") return Object.freeze({ status, usable: true, reason: null });
    if (KNOWN_FAILURES.has(status)) return Object.freeze({ status, usable: false, reason: status });
    return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
  }
  if (typeof result !== "object") return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
  const hasOwn = (key) => Object.prototype.hasOwnProperty.call(result, key);
  if (hasOwn("ok") && typeof result.ok !== "boolean") {
    return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
  }
  for (const key of ["status", "reason"]) {
    if (!hasOwn(key)) continue;
    const value = result[key];
    if (value !== null && (typeof value !== "string" || value.trim() === "")) {
      return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
    }
  }
  const status = typeof result.status === "string" ? result.status.trim().toLowerCase() : null;
  const reason = typeof result.reason === "string" ? result.reason.trim().toLowerCase() : null;
  const signals = [status, reason].filter(Boolean);
  const hasLoaded = signals.includes("loaded");
  const failures = signals.filter((signal) => KNOWN_FAILURES.has(signal));
  const unknownSignals = signals.filter((signal) => signal !== "loaded" && !KNOWN_FAILURES.has(signal));
  if (unknownSignals.length > 0 || (hasLoaded && failures.length > 0)) {
    return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
  }
  if (result.ok === true) {
    if (failures.length === 0) return Object.freeze({ status: "loaded", usable: true, reason: null });
    return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
  }
  if (result.ok === false) {
    if (hasLoaded) return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
    const failure = failures[0] ?? "failed";
    return Object.freeze({ status: failure, usable: false, reason: failure });
  }
  if (hasLoaded) return Object.freeze({ status: "loaded", usable: true, reason: null });
  if (failures.length > 0) return Object.freeze({ status: failures[0], usable: false, reason: failures[0] });
  return Object.freeze({ status: "malformed", usable: false, reason: "malformed" });
}

export function assetPresentationFor(asset = {}, availability = null) {
  const descriptor = asset && typeof asset === "object" ? asset : {};
  const fallback = descriptor.fallback && typeof descriptor.fallback === "object"
    ? descriptor.fallback
    : { id: "generic-asset", label: "Asset", equivalent: "Asset unavailable" };
  const outcome = normalizeAssetAvailability(availability);
  const loaded = outcome.usable;
  const requestedId = text(descriptor.id, fallback.id);
  const requestedLabel = text(descriptor.label, fallback.label);
  const renderedId = loaded ? requestedId : text(fallback.id, "generic-asset");
  const renderedLabel = loaded ? requestedLabel : text(fallback.label, "Asset");
  const equivalent = loaded
    ? text(descriptor.equivalent, `${requestedLabel} visual or audio asset`)
    : text(fallback.equivalent, `${requestedLabel} unavailable; generic fallback shown`);
  return Object.freeze({
    schema_version: "asset-presentation-v1",
    requested_id: requestedId,
    requested_label: requestedLabel,
    rendered_id: renderedId,
    rendered_label: renderedLabel,
    asset_status: outcome.status,
    display_mode: loaded ? "asset" : "fallback",
    source: loaded
      ? text(descriptor.source, "Local approved release asset")
      : `Visible fallback because the release asset is ${outcome.status}`,
    equivalent,
    release_path: loaded && typeof descriptor.release_path === "string" ? descriptor.release_path : null,
    fallback_reason: loaded ? null : outcome.reason,
  });
}
