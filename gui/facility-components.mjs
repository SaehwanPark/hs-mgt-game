import { assetPresentationFor } from "./asset-availability.mjs";

const GENERAL_HOSPITAL_BASE = Object.freeze({
  schema_version: "facility-component-v1",
  id: "general-hospital-base",
  label: "General hospital base",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "General hospital label, base silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/general-hospital-base.svg",
  release_path: "assets/release/visual/svg/general-hospital-base.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({
    id: "generic-facility",
    label: "Facility",
    equivalent: "Facility label and generic marker",
  }),
});

const ADMINISTRATIVE_HEADQUARTERS = Object.freeze({
  schema_version: "facility-component-v1",
  id: "administrative-headquarters",
  label: "Administrative headquarters",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Administrative headquarters label, stepped office silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/administrative-headquarters.svg",
  release_path: "assets/release/visual/svg/administrative-headquarters.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const PATIENT_TOWER = Object.freeze({
  schema_version: "facility-component-v1",
  id: "patient-tower",
  label: "Patient tower",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Patient tower label, vertical silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/patient-tower.svg",
  release_path: "assets/release/visual/svg/patient-tower.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({
    id: "generic-facility",
    label: "Facility",
    equivalent: "Facility label and generic marker",
  }),
});

const PARKING_STRUCTURE = Object.freeze({
  schema_version: "facility-component-v1",
  id: "parking-structure",
  label: "Parking structure",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Parking structure label, tiered deck silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/parking-structure.svg",
  release_path: "assets/release/visual/svg/parking-structure.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const EMERGENCY_DEPARTMENT = Object.freeze({
  schema_version: "facility-component-v1",
  id: "emergency-department",
  label: "Emergency department",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Emergency department label, entrance-wing silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/emergency-department.svg",
  release_path: "assets/release/visual/svg/emergency-department.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({
    id: "generic-facility",
    label: "Facility",
    equivalent: "Facility label and generic marker",
  }),
});

const UTILITY_PLANT = Object.freeze({
  schema_version: "facility-component-v1",
  id: "utility-plant",
  label: "Utility plant",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Utility plant label, pipe-and-tank silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/utility-plant.svg",
  release_path: "assets/release/visual/svg/utility-plant.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const RESEARCH_EDUCATION_BUILDING = Object.freeze({
  schema_version: "facility-component-v1",
  id: "research-education-building",
  label: "Research and education building",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Research and education building label, wing-and-tower silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/research-education-building.svg",
  release_path: "assets/release/visual/svg/research-education-building.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const CONSTRUCTION_CRANE = Object.freeze({
  schema_version: "facility-component-v1",
  id: "construction-crane",
  label: "Construction crane",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Construction crane label, boom-and-tower silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/construction-crane.svg",
  release_path: "assets/release/visual/svg/construction-crane.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const UNDEVELOPED_PARCEL = Object.freeze({
  schema_version: "facility-component-v1",
  id: "undeveloped-parcel",
  label: "Undeveloped parcel",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Undeveloped parcel label, dashed parcel-boundary silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/undeveloped-parcel.svg",
  release_path: "assets/release/visual/svg/undeveloped-parcel.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const AMBULATORY_CENTER = Object.freeze({
  schema_version: "facility-component-v1",
  id: "ambulatory-center",
  label: "Ambulatory center",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Ambulatory center label, low-rise arc silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/ambulatory-center.svg",
  release_path: "assets/release/visual/svg/ambulatory-center.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const SPECIALTY_CENTER = Object.freeze({
  schema_version: "facility-component-v1",
  id: "specialty-center",
  label: "Specialty center",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Specialty center label, peaked canopy silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/specialty-center.svg",
  release_path: "assets/release/visual/svg/specialty-center.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const RURAL_CLINIC = Object.freeze({
  schema_version: "facility-component-v1",
  id: "rural-clinic",
  label: "Rural clinic",
  source: "Visible facility kind and actor-visible status context",
  equivalent: "Rural clinic label, pitched-roof silhouette, identity badge, and written layer labels",
  source_path: "assets/source/visual/facilities/rural-clinic.svg",
  release_path: "assets/release/visual/svg/rural-clinic.svg",
  grid: "8px",
  view_box: "0 0 760 500",
  css_variables: ["--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"],
  layers: [
    Object.freeze({ id: "base", label: "Base structure", source: "Visible facility kind" }),
    Object.freeze({ id: "identity", label: "System identity layer", source: "Visible owning-system identity" }),
    Object.freeze({ id: "capacity", label: "Capacity/service-line layer", source: "Visible capacity or service-line field" }),
    Object.freeze({ id: "project", label: "Project layer", source: "Visible project status" }),
    Object.freeze({ id: "pressure", label: "Operational-pressure layer", source: "Visible pressure status" }),
    Object.freeze({ id: "selection", label: "Selection/focus layer", source: "Local selected-facility presentation state" }),
    Object.freeze({ id: "uncertainty", label: "Uncertainty/stale-observation layer", source: "Visible observation freshness or missingness" }),
  ],
  fallback: Object.freeze({ id: "generic-facility", label: "Facility", equivalent: "Facility label and generic marker" }),
});

const GENERIC_FACILITY = Object.freeze({
  schema_version: "facility-component-v1",
  id: "generic-facility",
  label: "Facility",
  source: "Missing or unknown visible facility kind",
  equivalent: "Facility label and generic marker",
  source_path: null,
  release_path: null,
  grid: "8px",
  view_box: null,
  css_variables: [],
  layers: [],
  fallback: Object.freeze({
    id: "generic-facility",
    label: "Facility",
    equivalent: "Facility label and generic marker",
  }),
});

export const FACILITY_COMPONENTS = Object.freeze({
  "general-hospital-base": GENERAL_HOSPITAL_BASE,
  "administrative-headquarters": ADMINISTRATIVE_HEADQUARTERS,
  "patient-tower": PATIENT_TOWER,
  "parking-structure": PARKING_STRUCTURE,
  "utility-plant": UTILITY_PLANT,
  "research-education-building": RESEARCH_EDUCATION_BUILDING,
  "construction-crane": CONSTRUCTION_CRANE,
  "undeveloped-parcel": UNDEVELOPED_PARCEL,
  "emergency-department": EMERGENCY_DEPARTMENT,
  "ambulatory-center": AMBULATORY_CENTER,
  "specialty-center": SPECIALTY_CENTER,
  "rural-clinic": RURAL_CLINIC,
  "generic-facility": GENERIC_FACILITY,
});

export function facilityComponentFor(id) {
  return Object.prototype.hasOwnProperty.call(FACILITY_COMPONENTS, id)
    ? FACILITY_COMPONENTS[id]
    : GENERIC_FACILITY;
}

export function facilityPresentationFor(id, availability = "loaded") {
  const component = facilityComponentFor(id);
  return Object.freeze({
    ...assetPresentationFor(component, availability),
    component_id: component.id,
    layer_count: component.layers.length,
  });
}

export function facilityLayerSummary(id = "general-hospital-base") {
  const component = facilityComponentFor(id);
  return component.layers.map((layer) => ({
    ...layer,
    component: component.label,
    equivalent: component.equivalent,
  }));
}
