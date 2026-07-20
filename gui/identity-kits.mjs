const RIVERSIDE_IDENTITY_KIT = Object.freeze({
  schema_version: "identity-kit-v1",
  id: "riverside",
  label: "Riverside",
  monogram: "RV",
  source: "Visible Riverside system identity",
  equivalent: "Riverside name, mark, monogram, and text label",
  palette: Object.freeze({
    primary: "#0b6e69",
    secondary: "#a95226",
    ink: "#17232d",
    paper: "#f4f7f6",
  }),
  asset: Object.freeze({
    source_path: "assets/source/visual/identity/riverside-kit.svg",
    release_path: "assets/release/visual/svg/riverside.svg",
  }),
  surfaces: Object.freeze({
    logo_mark: "R silhouette with river line",
    monochrome_mark: "Single-color R silhouette with river line",
    compact_marker: "Circular R marker",
    facility_signage: "Riverside General sign treatment",
    report_header: "Riverside executive report header",
    compact_badge: "RV text badge",
    audio_motif: "audio.direction-riverside-motif",
  }),
  fallback: Object.freeze({
    id: "generic-institution",
    label: "Institution",
    equivalent: "Institution identity unavailable",
  }),
});

const GENERIC_IDENTITY_KIT = Object.freeze({
  schema_version: "identity-kit-v1",
  id: "generic-institution",
  label: "Institution",
  monogram: "IN",
  source: "Visible identity fallback",
  equivalent: "Institution identity unavailable",
  palette: Object.freeze({ primary: "#60707b", secondary: "#17232d", ink: "#17232d", paper: "#f4f7f6" }),
  asset: Object.freeze({ source_path: null, release_path: null }),
  surfaces: Object.freeze({
    logo_mark: "Generic diamond marker",
    monochrome_mark: "Generic monochrome diamond marker",
    compact_marker: "Generic circular marker",
    facility_signage: "Institution signage fallback",
    report_header: "Institution report header fallback",
    compact_badge: "IN text badge",
    audio_motif: null,
  }),
  fallback: null,
});

export const IDENTITY_KITS = Object.freeze({
  riverside: RIVERSIDE_IDENTITY_KIT,
  "generic-institution": GENERIC_IDENTITY_KIT,
});

export function identityKitFor(id) {
  return IDENTITY_KITS[id] ?? GENERIC_IDENTITY_KIT;
}

export function identitySurfaceSummary(id = "riverside") {
  const kit = identityKitFor(id);
  return Object.entries(kit.surfaces).map(([surface, treatment]) => ({
    surface,
    treatment,
    label: kit.label,
    equivalent: kit.equivalent,
  }));
}
