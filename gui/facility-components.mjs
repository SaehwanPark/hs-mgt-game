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
  fallback: null,
});

export const FACILITY_COMPONENTS = Object.freeze({
  "general-hospital-base": GENERAL_HOSPITAL_BASE,
  "patient-tower": PATIENT_TOWER,
  "emergency-department": EMERGENCY_DEPARTMENT,
  "ambulatory-center": AMBULATORY_CENTER,
  "specialty-center": SPECIALTY_CENTER,
  "generic-facility": GENERIC_FACILITY,
});

export function facilityComponentFor(id) {
  return FACILITY_COMPONENTS[id] ?? GENERIC_FACILITY;
}

export function facilityLayerSummary(id = "general-hospital-base") {
  const component = facilityComponentFor(id);
  return component.layers.map((layer) => ({
    ...layer,
    component: component.label,
    equivalent: component.equivalent,
  }));
}
