import { assetPresentationFor } from "./asset-availability.mjs";

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

const NORTHLAKE_IDENTITY_KIT = Object.freeze({
  schema_version: "identity-kit-v1",
  id: "northlake",
  label: "Northlake",
  monogram: "NL",
  source: "Visible Northlake system identity",
  equivalent: "Northlake name, mark, monogram, and text label",
  palette: Object.freeze({
    primary: "#315a89",
    secondary: "#7c4d8f",
    ink: "#17232d",
    paper: "#f3f6fa",
  }),
  asset: Object.freeze({
    source_path: "assets/source/visual/identity/northlake-kit.svg",
    release_path: "assets/release/visual/svg/northlake.svg",
  }),
  surfaces: Object.freeze({
    logo_mark: "N geometry with layered lake line",
    monochrome_mark: "Single-color N geometry with layered line",
    compact_marker: "Rounded-square N marker",
    facility_signage: "Northlake Clinic sign treatment",
    report_header: "Northlake public-signal report header",
    compact_badge: "NL text badge",
    audio_motif: "audio.direction-northlake-motif",
  }),
  fallback: Object.freeze({
    id: "generic-institution",
    label: "Institution",
    equivalent: "Institution identity unavailable",
  }),
});

const SUMMIT_IDENTITY_KIT = Object.freeze({
  schema_version: "identity-kit-v1",
  id: "summit",
  label: "Summit",
  monogram: "SM",
  source: "Visible Summit system identity",
  equivalent: "Summit name, mark, monogram, and text label",
  palette: Object.freeze({
    primary: "#6b4e8d",
    secondary: "#c2872f",
    ink: "#17232d",
    paper: "#f8f5fb",
  }),
  asset: Object.freeze({
    source_path: "assets/source/visual/identity/summit-kit.svg",
    release_path: "assets/release/visual/svg/summit.svg",
  }),
  surfaces: Object.freeze({
    logo_mark: "Peak geometry with layered line",
    monochrome_mark: "Single-color peak geometry with layered line",
    compact_marker: "Triangular Summit marker",
    facility_signage: "Summit Center sign treatment",
    report_header: "Summit market-signal report header",
    compact_badge: "SM text badge",
    audio_motif: "audio.direction-summit-motif",
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
  fallback: Object.freeze({
    id: "generic-institution",
    label: "Institution",
    equivalent: "Institution identity unavailable",
  }),
});

export const IDENTITY_KITS = Object.freeze({
  riverside: RIVERSIDE_IDENTITY_KIT,
  northlake: NORTHLAKE_IDENTITY_KIT,
  summit: SUMMIT_IDENTITY_KIT,
  "generic-institution": GENERIC_IDENTITY_KIT,
});

export function identityKitFor(id) {
  return IDENTITY_KITS[id] ?? GENERIC_IDENTITY_KIT;
}

export function identityPresentationFor(id, availability = "loaded") {
  const kit = identityKitFor(id);
  return Object.freeze({
    ...assetPresentationFor({
      id: kit.id,
      label: kit.label,
      source: kit.source,
      equivalent: kit.equivalent,
      release_path: kit.asset.release_path,
      fallback: kit.fallback,
    }, availability),
    identity_id: kit.id,
  });
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
