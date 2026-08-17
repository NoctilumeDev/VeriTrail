# M12 Visual Reference Contract 1.0

> Status: `APPROVED_FOR_IMPLEMENTATION`
> Date: 2026-08-15
> Scope: `L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> Precedence: This contract refines the visual direction in document 46. It does not alter any M0-M11 data, evidence, URL, keyboard, or security contract.

## 1. Purpose

The following user-supplied desktop references are the visual acceptance target for M12. They define composition, hierarchy, spacing, materials, typography scale, and decorative restraint. They are not runtime page backgrounds, data sources, or permission to introduce controls without real behavior.

| Surface | Reference | Decision |
| --- | --- | --- |
| Runs / Catalog | `design-references/m12/01-runs-catalog.png` | Adopted |
| Run Detail | `design-references/m12/02-run-detail-topnav.png` | Adopted |
| Run Detail, side-index variant | `design-references/m12/03-run-detail-sidenav-alternative.png` | Retained as an alternative only; not in the M12 implementation baseline |
| Rerun Comparison | `design-references/m12/04-rerun-comparison.png` | Adopted |
| Paired Analysis | `design-references/m12/05-paired-analysis.png` | Adopted |
| Batch Analysis | `design-references/m12/06-batch-analysis.png` | Adopted |
| Browser Evidence | `design-references/m12/07-browser-evidence.png` | Adopted |

## 2. Shared Shell

- Catalog is the public forecourt: full masthead, four-view courtyard navigation, cloud-water threshold, title, command gate, then continuous ledger.
- Run Detail and all three derived-analysis views use the compact dark lacquer top bar, real global view navigation, and an action area only for operations the product already supports.
- Paper is warm and materially present. Dark lacquer, mineral gold, structural vermilion, and water-blue have positional roles; they are not generic decorative colors.
- A section is a room in one continuous surface. It may have fine gold corners and a heading rail, but repeated card elevation, large radii, and stacked framed surfaces are prohibited.
- Cloud-water and landscape line art remain at transitions, edge fields, or large empty surfaces. They never obscure hashes, tables, verdicts, focus indicators, or actions.

## 3. Non-Negotiable Runtime Boundaries

- Reproduce the reference with semantic HTML, CSS, local ornamental/texture assets, and real controls. Do not use a reference screenshot as a page background or substitute it for live UI.
- Do not add fake settings, accounts, exports, or directory operations. If a reference control has no existing behavior, its visual space may be rebalanced with truthful static boundary text rather than a false interactive element.
- Preserve existing URL/history behavior, imported-file semantics, `data-testid` values, keyboard contracts, focus restoration, verdict authority, bundle verification, and browser-evidence semantics.
- Desktop reference fidelity is implemented first. Responsive composition is a subsequent, explicit adaptation step; it must not be a desktop screenshot scaled down.

## 4. Implementation Order

1. Fully reproduce the adopted Catalog desktop composition against reference 01 before making novel visual decisions.
2. Build the compact inner-page shell shared by the adopted Run Detail, Comparison, Pairing, Batch, and Browser Evidence references.
3. Recompose each real data surface onto that shell without changing its data model or interaction contract.
4. Run desktop visual review with real positive, negative, local Catalog, and derived-analysis evidence.
5. Only then implement responsive behavior, keyboard/focus verification, forced colors, and M12-F gates.

This document is a design acceptance contract, not a claim that M12 is complete or frozen.
