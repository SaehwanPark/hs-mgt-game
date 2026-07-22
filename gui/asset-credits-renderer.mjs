import { ASSET_CREDITS } from "./asset-credits.mjs";

function textNode(root, selector, value) {
  const node = root.querySelector(selector);
  if (node) node.textContent = String(value);
  return node;
}

export function renderAssetCredits({ root = document, catalog = ASSET_CREDITS } = {}) {
  const summary = root.querySelector("#asset-credits-summary");
  const list = root.querySelector("#asset-credits-list");
  const entries = Array.isArray(catalog?.entries) ? catalog.entries : [];
  if (!summary || !list) return { ok: false, code: "credits_surface_missing", count: 0 };

  list.replaceChildren();
  textNode(
    root,
    "#asset-credits-summary",
    `${entries.length} registered visual/audio entries · ${catalog.third_party_release_count ?? 0} third-party release assets`,
  );
  textNode(
    root,
    "#asset-credits-limit",
    "This registry projection records provenance and release status. It does not replace a human license audit.",
  );

  if (!entries.length) {
    const empty = root.createElement("li");
    empty.className = "empty";
    empty.textContent = "No asset credits are available.";
    list.append(empty);
    return { ok: true, count: 0 };
  }

  for (const entry of entries) {
    const item = root.createElement("li");
    item.className = "asset-credit";
    const heading = root.createElement("strong");
    heading.textContent = entry.id ?? "Unknown asset";
    const meta = root.createElement("p");
    meta.className = "asset-credit-meta";
    meta.textContent = [
      entry.asset_type,
      `Source: ${entry.source}`,
      `License: ${entry.license}`,
      `Approval: ${entry.approval_status}`,
      `Provenance: ${entry.provenance?.kind ?? "unknown"}`,
      `Source URL: ${entry.provenance?.source_url ?? "repository source"}`,
      `Retrieved: ${entry.provenance?.retrieval_date ?? "not externally retrieved"}`,
      `License reference: ${entry.provenance?.license_reference ?? "not recorded"}`,
      `Release: ${entry.release_status}`,
    ].join(" · ");
    const attribution = root.createElement("p");
    attribution.textContent = `Attribution: ${entry.attribution}`;
    const equivalent = root.createElement("p");
    equivalent.className = "asset-credit-equivalent";
    equivalent.textContent = `Accessible equivalent: ${entry.accessible_equivalent}`;
    item.append(heading, meta, attribution, equivalent);
    list.append(item);
  }
  return { ok: true, count: entries.length };
}
