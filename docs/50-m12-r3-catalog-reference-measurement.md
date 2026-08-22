# M12-R3 Catalog Reference Measurement 0.1

> Status: `R3-A / MEASURED / ADOPTED_AND_VALIDATED`
>
> Date: 2026-08-15
>
> Scope: `L0_PRESENTATION`; no Vue, CSS, route, data, or interaction implementation
>
> Parent: [M12-R3 reference-first Catalog rebuild contract](49-m12-r3-reference-first-catalog-rebuild.md)
>
> Visual authority: `docs/design-references/m12/01-runs-catalog.png`
>
> Closeout: the measured geometry was adopted, implemented, and confirmed in the final browser review; integrated
> evidence is recorded in [M12-F final validation facts](51-m12-f-final-validation-facts.md).

## 1. Purpose

This is a measurement record for the first R3-A review. It turns the adopted Catalog reference into spatial
constraints before any component, CSS, generated material, or local asset is connected to the Workbench.

It does not grant permission to copy the reference screenshot, add controls without behavior, change M11 facts,
or treat a measurement as a completed UI.

## 2. Desktop Reference Geometry

The adopted image is `1448 x 1086 px`. Measurements below are intentionally expressed as bands and proportions,
not as an attempt to reproduce a static screenshot at every viewport.

| Reading band | Reference Y range | Approx. share | Required role in R3 |
| --- | ---: | ---: | --- |
| Main hall | `0-153 px` | `14.1%` | One full-width deep-lacquer identity shell; no nested status cards or local controls |
| Central threshold | `150-166 px` | overlap | One small centered gold transition joining hall and courtyard |
| Courtyard navigation | `166-326 px` | `14.7%` | Four truthful public-view entries; names and active state remain primary, illustration secondary |
| Title court | `327-452 px` | `11.6%` | Unframed view identity and breathing room, not a generic hero card |
| Command gate | `453-531 px` | `7.3%` | One real operation group: three fixture choices plus the existing local file import |
| Intercourt interval | `532-549 px` | `1.7%` | Deliberate separation before the ledger hall; no extra panel |
| Catalog eave | `550-578 px` | `2.6%` | A single building-scale threshold above the Catalog, never repeated at row scale |
| Catalog title hall | `579-675 px` | `8.9%` | Deep-lacquer title rail and one truthful snapshot boundary |
| Continuous ledger | `676-1086 px` | `37.8%` | One paper data surface with rows, separators, state marks, long IDs, and entry affordances |

At the reference desktop width, the content edges sit at approximately `44 px` from either side (`3.0%` of width).
The command gate and Catalog hall share that structural alignment. They do not share the same height, fill, or
visual weight.

The four courtyard entry centers are approximately at `x = 198, 558, 886, 1216 px`. This is a four-part reading
rhythm, not a collection of four cards: there is no outer navigation card and no per-entry elevation.

## 3. Boundary Budget

The reference has three building-scale boundaries and one continuous data surface:

```text
main hall       = global identity boundary
command gate    = existing source/import operation boundary
Catalog hall    = catalog-wide ledger boundary
Run row         = separator + left fact mark + compact state mark, never a card
```

The following compositions are therefore rejected before implementation:

- a dark masthead containing a second framed navigation widget;
- a command gate wrapped in another generic toolbar card;
- a Catalog hall containing individual Run cards or independently framed status cells;
- a texture, gold eave, cloud-water banner, or frame reused at multiple semantic scales.

## 4. Material Targets

Single-pixel samples are only calibration points from the adopted image; final materials must preserve contrast,
text legibility, forced-colors fallback, and the separate warning-state semantics already defined by M12.

| Positional token | Sampled reference color | Intended responsibility |
| --- | --- | --- |
| Deep lacquer | `#0A2428` | Main hall and Catalog title rail only |
| Paper field | `#EDE3D7` | Courtyard and broad page field, with visible but low-contrast fibre |
| Ledger paper | `#F1E8DD` | Continuous Catalog reading surface |
| Structural gold | `#A7875D` | Thresholds, limited architectural corners, and fine hierarchy lines |
| Command vermilion | `#8A2919` | The one real local-import action surface; never a verdict color |

`FAIL`/`ERROR` remains a separate semantic warning token. It cannot reuse command vermilion merely because both
are red. The proof sheet must show the distinction under normal color, grayscale, and forced-colors fallback.

## 5. Proof Sheet Deliverables

No material enters the Workbench directly. The proof sheet must independently show these unlabeled, local,
non-watermarked components against warm paper and deep lacquer calibration fields:

| Component | Required form | One allowed responsibility |
| --- | --- | --- |
| Paper fibre tile | seamless, low-contrast material | page and ledger substrate |
| Lacquer tile | seamless dark material with no border | masthead and Catalog title rail |
| Cloud-water transition | transparent, wide, quiet linework | one courtyard transition below navigation |
| Gold threshold | left cap, repeatable middle, right cap | one large-scale roof/eave transition |
| Command gate | sliced corners/edges/center or equivalent | existing source and import control group |
| Catalog hall frame | corners, rails, inner paper field separated | one Catalog-wide building boundary |
| Navigation marks | four small location marks | public-view orientation only; names remain accessible text |

The proof sheet must expose tile seams, alpha edges, repeatable middles, dark-background assumptions, and
small-size degradation. A full screenshot, a complete precomposed frame, text, logos, watermarks, fake buttons,
or reference image pixels are prohibited.

## 6. R3-A Review Gates

- [x] Adopted reference geometry measured and recorded.
- [x] External layout precedents reduced to non-visual rules in document 49.
- [ ] Proof sheet materials reviewed against the reference for hue, weight, texture, and edge quality.
- [ ] User confirms that proof sheet materials belong to the same visual world before any Vue/CSS connection.
- [ ] Only after both checks may R3-B rebuild the `1448 px` Catalog desktop composition with real data.

R3-A is deliberately not a visual completion claim. It is the point at which the old overlay-first path is prevented
from returning under a new filename.
