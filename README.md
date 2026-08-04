# CU Boulder–Meta Alignment · Streamlit Companion

Streamlit rebuild of `../Streamlit/CUB-Meta Alignment_Interactive Companion.html`.
Same data, same charts, same interactivity — Plotly instead of hand-rolled SVG.

Internal/review use only.

## Run

`streamlit-plotly-events` pins an older component API, so a virtualenv is the
safe way to install (and Homebrew Python blocks system-wide installs anyway):

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python -m streamlit run app.py
```

If the venv already exists, just the last line. The theme in
`.streamlit/config.toml` is picked up automatically.

## Deploying to Streamlit Community Cloud

The app is self-contained — all data lives in `data.py`, and nothing reads a
file outside this folder — so only this folder gets published.

**1. Make a repo from THIS FOLDER ONLY.**

> The sibling folders (`../Meta Data/`, `../Outputs/`, `../Meta.zip`) hold
> licensed Frost & Sullivan reports stamped "Unauthorized Distribution
> Prohibited", PitchBook profiles containing executive contact details, and the
> raw source workbooks. **None of that may go into the repo.** Initialise git
> inside `streamlit_companion/`, never in a parent directory.

```bash
cd "Strategic Reports/Meta/streamlit_companion"
git init
git add .
git status          # confirm: only app.py, data.py, test_data.py,
                    # requirements.txt, README.md, .gitignore, .streamlit/
git commit -m "CU Boulder-Meta alignment dashboard"
```

Create an **empty private repo** on GitHub, then:

```bash
git remote add origin https://github.com/<you>/<repo>.git
git branch -M main
git push -u origin main
```

**2. Deploy.** At <https://share.streamlit.io> → *Create app* → pick the repo,
branch `main`, main file `app.py`. First build takes a few minutes.

**3. Restrict access — do this before sharing the link.** In the app's
*Settings → Sharing*, set the app to private and invite viewers by email
address. A Community Cloud app is **public by default**; this dashboard names
44 CU researchers and their funding, so the app must be private before the URL
goes to anyone.

**4. Updating.** Push to `main` and the app redeploys itself:

```bash
git add -A && git commit -m "..." && git push
```

### Version pinning matters here

`requirements.txt` is fully pinned. `streamlit-plotly-events` (0.0.6,
unmaintained) is the fragile piece — click-to-filter breaks silently on some
Streamlit versions. The pinned set was verified end to end on **Python 3.13**,
which is what Community Cloud provides: 54 route × section combinations with no
exceptions, plus a browser test confirming click-to-filter, AG Grid and
navigation all work. Re-run those checks before changing any pin.

To force a specific interpreter, add a `.python-version` file containing `3.13`.

## Files

- `data.py` — every data array transcribed verbatim from the HTML's `<script>`
  block (`R`, `JOBS`, `PAT`, `ERA`, `FRP`, `SCH`, `FUND`, `ALUMR`, `ALUM`, `YRS`,
  `SIG`, `TERMS`, `P`, `SC`, `FM`, `W`) plus the inline figures from its render
  functions. HTML entities decoded. Nothing added, rounded, or estimated.
- `app.py` — the six sections, in source order.
- `test_data.py` — self-check that the transcription still reconciles to the
  headline figures. Run `./.venv/bin/python test_data.py` (prints `ok`).
- `.streamlit/config.toml` — CU Boulder brand theme and typography.

## Brand palette

Official CU Boulder colors, in fixed roles from the brand accessibility guide.
**The pairings are pre-vetted — do not recombine them.**

| Role | Hex | Contrast |
|---|---|---|
| Page background | `#FFFFFF` | — |
| Body text | `#000000` | 21.00:1 on white |
| Headings / section titles | CUB Dark Blue `#0A3758` | 12.35:1 on white |
| Accent — KPI numbers, chart highlight | Accessible CU Gold `#8D7334` | 4.53:1 on white |
| Links / interactive / secondary accent | CUB Sky Blue `#096FAE` | 5.39:1 on white |
| Header bar | `#0A3758` bg, `#FFFFFF` text, CU Gold `#CFB87C` eyebrow | 12.35:1 / 6.35:1 |

**CU Gold `#CFB87C` is header-bar-only.** On white it is 1.94:1 and fails AA,
which is why `#8D7334` is the gold used in the page body and in every chart.
Chart neutrals (`MUTED`, `LINE`, the gold/sky tints, `GOLD_RAMP`) are greyscale
or brand-derived so no new hues enter the palette; heatmap labels are black,
which clears AA against every step of the ramp.

Typography is `'Helvetica Neue', Helvetica, Arial, sans-serif` globally — set in
`config.toml`, reinforced by a CSS override for component iframes (AG Grid,
option-menu) and by a Plotly template so charts match.

## Interactivity

- **Click-to-filter** — clicking a bar in the route-priority chart or a cell in
  the scoring heatmap sets the global route filter, as in the HTML. The sidebar
  selectbox stays in sync both ways.
- **Sidebar selectbox** — the other way to set the same filter, plus a
  "Clear route filter" button.
- **Section nav** — `streamlit-option-menu` in the sidebar.
- **Section 5** — AG Grid with per-column sort/filter menus, plus a cross-field
  search box above the grid.
- **Section 6** — scenario A–D selection.

## Implementation notes worth knowing

- **The route filter lives in `st.session_state["route"]`, which no widget
  owns.** Streamlit raises `StreamlitAPIException` if you assign to a key bound
  to a live widget, so the sidebar selectbox uses a key that embeds the current
  route (`route_pick_<route>`) and is re-created when a chart click changes it.
  Reverting that will break click-to-filter silently.
- **`agSetColumnFilter` is AG Grid Enterprise.** In the community build it
  renders an empty filter panel and logs `error #200`. The grid therefore uses
  `agTextColumnFilter`, and the cross-field search box compensates.
- **`plotly_events` bypasses Streamlit's Plotly template**, so bar labels are
  pre-formatted strings rather than `texttemplate="%{text:.1f}"` — otherwise the
  placeholder renders literally.
- `streamlit-plotly-events` is 0.0.6 and unmaintained. It works on Streamlit
  1.60 (verified by driving a real browser click end to end), but it is the most
  likely thing to break on a future Streamlit upgrade. If it does, the sidebar
  selectbox still provides the same filtering.

## Source-fidelity note

All captions beginning "From the report:" / "From the working deck:" /
"From the briefing report:" are reproduced verbatim and attributed the same way.
No interpretation, insight or recommendation has been added.
