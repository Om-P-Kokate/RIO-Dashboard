"""CU Boulder–Meta Alignment · Interactive Companion (Streamlit rebuild).

A 1:1 port of CUB-Meta Alignment_Interactive Companion.html. All data comes from
data.py; all interpretive text is quoted from the source report, the working
deck, or the researcher briefing.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridOptionsBuilder
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_option_menu import option_menu

import data as D

# CU Boulder official brand palette, in the roles fixed by the brand
# accessibility guide. These pairings are pre-vetted — do not recombine them.
#   NAV_GOLD (#CFB87C) is legible only on CUB Dark Blue (6.35:1); on white it is
#   1.94:1 and fails AA, which is why GOLD (#8D7334, 4.53:1 on white) is the
#   accent used everywhere in the page body, including charts.
WHITE = "#FFFFFF"        # page background
BLACK = "#000000"        # body text
DARKBLUE = "#0A3758"     # headings / section titles / nav bar background
GOLD = "#8D7334"         # Accessible CU Gold — KPI numbers, chart highlight
SKY = "#096FAE"          # CUB Sky Blue — links, interactive, secondary accent
NAV_GOLD = "#CFB87C"     # CU Gold — eyebrow text on the dark-blue bar ONLY

# Derived neutrals/tints for chart use only (borders, muted series, fills).
# Kept greyscale or brand-derived so no new hues enter the palette.
GOLD_TINT = "#E4DCC6"    # light fill under GOLD series
SKY_TINT = "#D6E7F2"     # light fill under SKY series
MUTED = "#9A9A9A"        # de-emphasised / "no route" series
LINE = "#D9D9D9"         # hairline borders
SKY_HOVER = "#EAF2F7"    # sky-derived hover wash for nav items
# Gold ramp for the 1-5 scoring heatmap, terminating at GOLD. Black labels clear
# AA against every step (4.63:1 at the darkest).
GOLD_RAMP = [[0.0, "#F2F0EA"], [0.5, "#DCD2B8"], [0.75, "#B9A472"], [1.0, GOLD]]
FONT_STACK = '"Helvetica Neue", Helvetica, Arial, sans-serif'

# Hide Plotly's floating toolbar — it overlapped the chart titles and is not
# useful for a read-only report.
PLOTLY_CONFIG = {"displayModeBar": False, "scrollZoom": False}

st.set_page_config(page_title="CU Boulder–Meta Alignment · Interactive Companion",
                   page_icon="◆", layout="wide")

# Global brand CSS. config.toml sets the theme fonts/colors; this enforces the
# typeface on component iframes and elements Streamlit's theme does not reach,
# and applies the CU Boulder heading/nav colors.
st.markdown(f"""
<style>
html, body, [class*="st-"], button, input, select, textarea,
.ag-theme-alpine, .ag-theme-alpine * {{
    font-family: {FONT_STACK} !important;
}}
/* ...but never on icon spans: forcing a text font onto a Material ligature
   makes it render as the literal glyph name ("keyboard_double_arrow_left"). */
/* Material icon spans hold a ligature name ("keyboard_double_arrow_left") as
   their text. The icon font is not always available, in which case that name
   renders as literal text. Restore the icon font where it exists, and hide the
   span entirely so the raw name can never leak into the page. */
[data-testid="stIconMaterial"], [data-testid*="Icon"],
span[class*="material-symbols"], span[class*="material-icons"] {{
    font-family: "Material Symbols Rounded", "Material Symbols Outlined",
                 "Material Icons" !important;
}}
[data-testid="stIconMaterial"] {{ display: none !important; }}
body, .stMarkdown p, .stMarkdown li {{ color: {BLACK}; }}

/* Headings / section titles — CUB Dark Blue */
h1, h2, h3, h4, h5, h6,
[data-testid="stHeading"] h1, [data-testid="stHeading"] h2,
[data-testid="stHeading"] h3 {{
    color: {DARKBLUE} !important;
    font-family: {FONT_STACK} !important;
}}

/* KPI numbers — Accessible CU Gold */
[data-testid="stMetricValue"] {{ color: {GOLD} !important; }}

/* Links / interactive — CUB Sky Blue */
a, a:visited {{ color: {SKY} !important; }}

/* Card panels (matches the HTML's .card) */
[class*="st-key-card-"] {{
    background-color: {WHITE};
    border: 1px solid {LINE};
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 16px;
}}

/* Header bar — CUB Dark Blue, white title, CU Gold eyebrow */
.cu-header {{
    background-color: {DARKBLUE};
    padding: 20px 26px;
    border-radius: 10px;
    margin-bottom: 22px;
}}
.cu-header .eyebrow {{
    color: {NAV_GOLD};
    font-size: 11px;
    letter-spacing: .16em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 8px;
}}
.cu-header h1 {{
    color: {WHITE} !important;
    font-size: 27px;
    font-weight: 600;
    margin: 0;
}}
.cu-header .meta {{
    color: {WHITE};
    opacity: .85;
    font-size: 12.5px;
    margin-top: 9px;
}}

/* Small static tables rendered as HTML (see Segment economics) */
table.mini {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
}}
table.mini th {{
    text-align: left;
    font-weight: 600;
    color: {DARKBLUE};
    border-bottom: 1px solid {LINE};
    padding: 0 6px 7px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .06em;
}}
table.mini td {{
    padding: 8px 6px;
    border-bottom: 1px solid {LINE};
}}
table.mini tbody tr:last-child td {{ border-bottom: none; }}
table.mini .n {{ text-align: right; font-variant-numeric: tabular-nums; }}

/* Remove the element toolbar's fullscreen/expand control. Expanding a table
   replaced the whole page with no visible way back, which read as being
   navigated off the dashboard. Tables stay inline instead. */
[data-testid="stElementToolbarButton"]:has([data-testid="StyledFullScreenButton"]),
[data-testid="StyledFullScreenButton"] {{
    display: none !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="cu-header">'
    '<div class="eyebrow">CU Boulder · Industry Research Partnerships · '
    'Research &amp; Innovation Office</div>'
    '<h1>CU Boulder – Meta Alignment</h1>'
    '<div class="meta">Alignment Intelligence Report, June 2026 · '
    'Prepared by Lisa Nanstad · For Chris Gustavson</div>'
    '</div>',
    unsafe_allow_html=True)


def _counter():
    i = 0
    while True:
        i += 1
        yield i


_card_ids = _counter()


def card():
    """Bordered white panel matching the HTML's .card style."""
    return st.container(key=f"card-{next(_card_ids)}")


def money(n):
    """Mirrors the HTML's M() helper."""
    return "—" if n == 0 else f"${n / 1e6:.2f}M"


def kpi_row(cards):
    for col, (value, label, note) in zip(st.columns(len(cards)), cards):
        col.metric(label, value)
        if note:
            col.caption(note)
    style_metric_cards(background_color=WHITE, border_left_color=GOLD,
                       border_color=LINE, box_shadow=False)


def quote(prefix, text, suffix=""):
    st.caption(f"{prefix} *“{text}”*{suffix}")


def bar_layout(fig, height, xtitle=None):
    fig.update_layout(height=height, margin=dict(l=0, r=10, t=10, b=10),
                      showlegend=False, xaxis_title=xtitle, yaxis_title=None,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


# Plotly's own default typeface/colors would otherwise bypass the brand CSS.
pio.templates["cu"] = go.layout.Template(layout=dict(
    font=dict(family=FONT_STACK, color=BLACK, size=12),
    colorway=[GOLD, SKY, MUTED, GOLD_TINT, SKY_TINT],
    xaxis=dict(gridcolor=LINE, linecolor=LINE, zerolinecolor=LINE),
    yaxis=dict(gridcolor=LINE, linecolor=LINE, zerolinecolor=LINE),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    hoverlabel=dict(font=dict(family=FONT_STACK)),
))
pio.templates.default = "plotly_white+cu"


# ------------------------------------------------- global route filter state --
# The authoritative route lives under "route", which no widget owns — Streamlit
# forbids assigning to a key bound to a live widget, and chart clicks must be
# able to write it. The selectbox uses its own key and is synced each run.
SECTIONS = ["Overview", "Route detail", "Company signals",
            "CU relationship evidence", "Researchers", "Strategic foresight"]

if "route" not in st.session_state:
    st.session_state.route = "all"
# Survives st.rerun() so filtering never navigates the reader away.
if "section" not in st.session_state:
    st.session_state.section = SECTIONS[0]
if "scen" not in st.session_state:
    st.session_state.scen = "none"


def set_route(key):
    """Called by chart clicks. Returns True if the route actually changed."""
    if key != st.session_state.route:
        st.session_state.route = key
        return True
    return False


ROUTE_LABELS = {"all": "All routes"}
ROUTE_LABELS.update({k: f"{D.R[k]['n']} · {D.R[k]['w']:.1f}" for k in D.O})

with st.sidebar:
    # Title/attribution now live in the dark-blue header bar, not here.
    # The selectbox key embeds the current route, so when a chart click changes
    # the route the widget is re-created with the new value as its default.
    # (Streamlit forbids writing to a key an instantiated widget owns.)
    picked = st.selectbox("Route", list(ROUTE_LABELS), format_func=ROUTE_LABELS.get,
                          index=list(ROUTE_LABELS).index(st.session_state.route),
                          key=f"route_pick_{st.session_state.route}")
    # Selectbox is the other way in: if the user changed it, it wins this run.
    if picked != st.session_state.route:
        st.session_state.route = picked
        st.rerun()
    section = option_menu(
        menu_title=None,
        options=SECTIONS,
        icons=["grid", "diagram-3", "building", "link-45deg", "people", "compass"],
        # Without a key + persisted index, option_menu re-mounts at index 0 on
        # every st.rerun(), throwing the reader back to Overview.
        key="section_menu",
        default_index=SECTIONS.index(st.session_state.section),
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": BLACK, "font-size": "14px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "2px 0",
                         "color": BLACK, "--hover-color": SKY_HOVER},
            "nav-link-selected": {"background-color": DARKBLUE, "color": WHITE,
                                  "font-weight": "600"},
        },
    )
    st.session_state.section = section

    # Reset controls sit at the bottom, out of the reading path — small, side by
    # side, and only offered when there is something to clear.
    st.divider()
    b1, b2 = st.columns(2)
    if b1.button("Clear route", width="stretch",
                 disabled=st.session_state.route == "all",
                 help="Show all routes again"):
        st.session_state.route = "all"
        st.rerun()
    if b2.button("Reset view", width="stretch",
                 help="Clear the route filter and scenario, and return to Overview"):
        st.session_state.route = "all"
        st.session_state.scen = "none"
        st.session_state.section = SECTIONS[0]
        # option_menu holds its own selection under its key; drop it so the
        # menu re-mounts on Overview rather than restoring the old tab.
        st.session_state.pop("section_menu", None)
        st.rerun()

cur = st.session_state.route
is_all = cur == "all"


# --------------------------------------------------------------- overview ----
def render_overview():
    st.header("01 · Overview")
    # The four report-level KPIs always stay visible; a selected route adds its
    # own row beneath rather than replacing them.
    if is_all:
        quote("From the report:", "Meta is not one partner. The report should map CU strengths "
              "against Meta route surfaces, not against ‘Meta’ generally.")
    else:
        st.caption(D.R[cur]["d"])

    kpi_row([("$4.80M", "Awarded value", "19 direct records"),
             ("38", "Confirmed engagements", "386,778 rows scanned"),
             ("44", "Researchers named", "56 route assignments"),
             ("152", "Alumni coded", "routing intelligence")])

    if not is_all:
        r = D.R[cur]
        st.markdown(f"**{r['n']}** — this route")
        kpi_row([(f"{r['w']:.1f}", "Weighted priority", f"rank {D.O.index(cur) + 1} of 8"),
                 (money(D.FUND[cur][0]), "Awarded", f"proposed {money(D.FUND[cur][1])}"),
                 (str(D.JOBS.get(cur, 0)), "Open Meta roles", "of 293 parsed"),
                 (str(D.PAT.get(cur, 0)), "Recent patents", "of 450 parsed")])

    # --- route priority: click a bar to set the global filter ---
    with card():
        st.subheader("Route priority")
        st.caption("weighted score from six dimensions · click a bar to filter the page")
        order = list(reversed(D.O))  # plotly draws horizontal bars bottom-up
        rank = pd.DataFrame({"Route": [D.R[k]["n"] for k in order],
                             "Score": [D.R[k]["w"] for k in order]})
        rank["Label"] = [f"{v:.1f}" for v in rank["Score"]]
        fig = px.bar(rank, x="Score", y="Route", orientation="h", text="Label")
        fig.update_traces(
            marker_color=[GOLD if (is_all or k == cur) else MUTED for k in order],
            textposition="outside",
            hovertemplate="%{y}<br>Weighted score %{x:.1f}<extra></extra>")
        bar_layout(fig, 340, "weighted score, 0 to 5")
        # Lock the axis to the 0-5 scoring scale and drop the gridlines, so the
        # bars read against the rubric rather than an auto-fitted range.
        fig.update_xaxes(range=[0, 5], dtick=1, showgrid=False)
        fig.update_yaxes(showgrid=False)
        ev = st.plotly_chart(fig, key="rank_click", on_select="rerun",
                             selection_mode="points", config=PLOTLY_CONFIG,
                             width="stretch")
        pts = (ev.selection or {}).get("points") if ev else None
        if pts:
            idx = pts[0].get("point_index")
            if idx is not None and 0 <= idx < len(order) and set_route(order[idx]):
                st.rerun()
        st.caption("Weighted from strategic importance, investment signal, market momentum, "
                   "university mechanism clarity, alumni warm path and risk. Risk is scored as "
                   "exposure to manage rather than opportunity.")

    with card():
        st.subheader("Strategic importance compared with university mechanism clarity")
        st.caption("both dimensions scored 1–5")
        order = list(reversed(D.O))
        dumb = pd.DataFrame({
            "Route": [D.R[k]["n"] for k in order] * 2,
            "Score": [D.R[k]["s"][0] for k in order] + [D.R[k]["s"][3] for k in order],
            "Dimension": (["Strategic importance — how much the route matters to Meta"] * len(order)
                          + ["University mechanism clarity — how reachable it is"] * len(order)),
        })
        fig = px.bar(dumb, x="Score", y="Route", color="Dimension", orientation="h",
                     barmode="group", range_x=[0, 5], text="Score",
                     color_discrete_sequence=[GOLD, SKY])
        fig.update_traces(textposition="outside", hovertemplate="%{y}<br>%{x}<extra></extra>")
        if not is_all:
            fig.for_each_trace(lambda t: t.update(
                marker_opacity=[1 if k == cur else 0.28 for k in order]))
        fig.update_layout(height=480, margin=dict(l=0, r=10, t=10, b=10),
                          xaxis_title="score, 1 to 5", yaxis_title=None,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title=None))
        st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
        quote("From the report:", "High-scoring routes are not all equally actionable: "
              "infrastructure is highly durable but poorly routed; trust/safety is highly durable "
              "but sensitive; Reality Labs is the most concrete first handshake.")

    # --- scoring matrix as a clickable Plotly heatmap ---
    with card():
        st.subheader("Scoring matrix")
        st.caption("1–5 per dimension · click any cell to filter the page to that route")
        order = list(reversed(D.O))
        z = [D.R[k]["s"] for k in order]
        fig = go.Figure(go.Heatmap(
            z=z, x=D.DIMS, y=[D.R[k]["n"] for k in order],
            colorscale=GOLD_RAMP,
            zmin=1, zmax=5, showscale=False, xgap=3, ygap=3,
            text=z, texttemplate="%{text}",
            # Black clears AA (>=4.5:1) against every step of the gold ramp.
            textfont=dict(size=13, color=BLACK),
            hovertemplate="%{y}<br>%{x}: %{z}<extra></extra>"))
        fig.update_layout(height=360, margin=dict(l=0, r=10, t=10, b=10),
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          xaxis=dict(side="top"))
        ev = st.plotly_chart(fig, key="hm_click", on_select="rerun",
                             selection_mode="points", config=PLOTLY_CONFIG,
                             width="stretch")
        pts = (ev.selection or {}).get("points") if ev else None
        if pts:
            # Heatmap click returns y = the route name; map it back to a route key.
            yv = pts[0].get("y")
            hit = next((k for k in D.O if D.R[k]["n"] == yv), None)
            if hit and set_route(hit):
                st.rerun()

        meta = pd.DataFrame({
            "Route": [D.R[k]["n"] for k in D.O],
            "Score": [D.R[k]["w"] for k in D.O],
            "Status": [D.R[k]["st"] for k in D.O],
        })
        st.dataframe(meta.style.format({"Score": "{:.1f}"}), hide_index=True, width="stretch")
        if is_all:
            st.caption("Click a heatmap cell, or use the sidebar, to filter the page to a route.")
        else:
            st.caption(f"**{D.R[cur]['n']}** — {D.R[cur]['d']}")


# ----------------------------------------------------------- route detail ----
def render_route_detail():
    if is_all:
        st.header("02 · Route detail")
        st.info("Select a route — in the sidebar, or by clicking the ranking chart or scoring "
                "matrix on the Overview — to see its detail.")
        if st.button("Back to Overview"):
            st.session_state.section = SECTIONS[0]
            st.session_state.pop("section_menu", None)
            st.rerun()
        return
    r = D.R[cur]
    st.header(f"02 · {r['f']}")
    st.caption(r["d"])
    kpi_row([(f"{D.ERA[cur][0]} / {D.ERA[cur][1]}", "Awarded / proposed grant records", ""),
             (str(D.FRP[cur][1]), "Distinct faculty-reported activities", ""),
             (f"{D.SCH[cur][1]} of {D.SCH[cur][0]}", "Confirmed of total scholarly signals", "")])

    left, right = st.columns(2)
    with left:
        with card():
            st.subheader("Score profile")
            st.caption("six dimensions, 1–5")
            fig = go.Figure(go.Scatterpolar(
                r=r["s"] + [r["s"][0]], theta=D.DIMS + [D.DIMS[0]], fill="toself",
                line_color=GOLD, fillcolor="rgba(141,115,52,0.22)",
                hovertemplate="%{theta}: %{r}<extra></extra>"))
            fig.update_layout(height=380, margin=dict(l=40, r=40, t=30, b=30),
                              polar=dict(radialaxis=dict(range=[0, 5], dtick=1),
                                         bgcolor="rgba(0,0,0,0)"),
                              paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")

    with right:
        with card():
            st.subheader("Evidence across streams")
            st.caption("record counts")
            streams = [
                ("Meta job postings", D.JOBS.get(cur, 0), SKY),
                ("Meta patents", D.PAT.get(cur, 0), SKY),
                ("Awarded grant records", D.ERA[cur][0], GOLD),
                ("Proposed grant records", D.ERA[cur][1], GOLD),
                ("Faculty-reported activities", D.FRP[cur][1], GOLD),
                ("Confirmed scholarly signals", D.SCH[cur][1], GOLD),
                ("Alumni by job function", D.ALUMR.get(cur, 0), MUTED),
            ]
            streams = list(reversed(streams))
            sdf = pd.DataFrame({
                "Stream": [s[0] for s in streams],
                "Count": [s[1] for s in streams],
                "Total": [D.STREAM_TOTALS[s[0]] for s in streams],
                "color": [s[2] for s in streams],
            })
            sdf["Label"] = sdf["Count"].astype(str) + " of " + sdf["Total"].astype(str)
            fig = px.bar(sdf, x="Count", y="Stream", orientation="h", text="Label")
            fig.update_traces(marker_color=sdf["color"], textposition="outside",
                              customdata=sdf[["Total"]],
                              hovertemplate="%{y}<br>%{x} of %{customdata[0]}<extra></extra>")
            st.plotly_chart(bar_layout(fig, 380, "records"), config=PLOTLY_CONFIG, width="stretch")
            st.caption("Sage = Meta-side signal · gold = CU-side evidence · grey = alumni. "
                       "Each count is shown out of its total possible.")

    with card():
        st.subheader("Near-term use")
        st.caption("from the route-coded evidence matrix")
        st.markdown(f"*“{r['u']}”* — status: {r['st']}")


# --------------------------------------------------------- company signals ---
def render_company():
    st.header("03 · Company signals")
    st.caption("Evidence underlying Section 1 of the report: what Meta says it is investing in, "
               "what it is hiring for, and what it is patenting.")

    c1, c2, c3 = st.columns(3)
    with c1:
        with card():
            st.subheader("Revenue share by segment")
            st.caption("FY2025")
            fig = go.Figure(go.Pie(
                labels=[p[0] for p in D.SEGMENT_SHARE], values=[p[1] for p in D.SEGMENT_SHARE],
                hole=0.58, sort=False, marker_colors=[GOLD, SKY],
                hovertemplate="%{label}<br>$%{value}SKY<extra></extra>"))
            fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0),
                              paper_bgcolor="rgba(0,0,0,0)",
                              annotations=[dict(text="98.9%<br>Family of Apps",
                                                showarrow=False, font_size=14)],
                              legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
            quote("From the report:", "The financial imbalance between the two segments is the "
                  "central company fact.")

    with c2:
        with card():
            st.subheader("Segment economics")
            st.caption("FY2025")
            # Three columns in a one-third-width column get clipped by
            # st.dataframe's fixed layout, so this small static table is plain
            # HTML — it wraps, and has no fullscreen control to get lost in.
            rows = "".join(
                f"<tr><td>{r[0]}</td><td class='n'>{r[1]}</td>"
                f"<td class='n'>{r[2] if r[2] else ''}</td></tr>"
                for r in D.SEGMENT_ECONOMICS)
            st.markdown(
                "<table class='mini'><thead><tr><th>Segment</th>"
                "<th class='n'>Revenue</th><th class='n'>Operating result</th>"
                f"</tr></thead><tbody>{rows}</tbody></table>",
                unsafe_allow_html=True)
            st.caption("Family of Apps: *“Cash engine; funds AI, infrastructure, safety, product, "
                       "and long-term platform bets.”* Reality Labs: *“Long-term "
                       "next-computing-platform bet; strategically important but economically "
                       "exposed.”*")

    with c3:
        with card():
            st.subheader("Global XR share")
            st.caption("2025, IDC")
            fig = go.Figure(go.Pie(
                labels=[p[0] for p in D.XR_SHARE], values=[p[1] for p in D.XR_SHARE],
                hole=0.58, sort=False, marker_colors=[GOLD, LINE],
                hovertemplate="%{label}<br>%{value}%<extra></extra>"))
            fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0),
                              paper_bgcolor="rgba(0,0,0,0)",
                              annotations=[dict(text="72.2%<br>Meta", showarrow=False,
                                                font_size=14)],
                              legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
            quote("From the report:", "IDC reports Meta led the global XR market in 2025 with "
                  "72.2% share… while Meta Quest VR headset shipments declined 42.3% year over "
                  "year.")

    with card():
        st.subheader("Meta total revenue and net income, FY2023 to FY2025")
        st.caption("US$ billions · full financial year")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=D.FIN_YEARS, y=D.FIN_REVENUE, name="Revenue",
                                 mode="lines+markers", line_color=GOLD, fill="tozeroy",
                                 fillcolor="rgba(141,115,52,0.12)",
                                 hovertemplate="%{x}<br>Revenue $%{y}SKY<extra></extra>"))
        fig.add_trace(go.Scatter(x=D.FIN_YEARS, y=D.FIN_NET_INCOME, name="Net income",
                                 mode="lines+markers", line_color=SKY,
                                 hovertemplate="%{x}<br>Net income $%{y}SKY<extra></extra>"))
        fig.update_layout(height=330, margin=dict(l=0, r=10, t=10, b=10),
                          yaxis_title="US$SKY", plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title=None))
        st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
        st.caption("Revenue grew from $134.9B to $201.0B across three years; net income from "
                   "$39.1B to $75.7B. From the report: *“Meta’s Q1 2026 outlook raised 2026 capex "
                   "guidance to $125B–$145B, citing higher component pricing and additional data "
                   "center costs to support future capacity.”*")

    left, right = st.columns(2)
    with left:
        with card():
            st.subheader("Open roles and recent patents by route")
            st.caption("293 job cards · 450 patent records")
            labels = list(reversed(D.JP_LABELS))
            jp = pd.DataFrame({
                "Route": [l[1] for l in labels] * 2,
                "Count": ([D.JOBS.get(l[0], 0) for l in labels]
                          + [D.PAT.get(l[0], 0) for l in labels]),
                "Series": ["Job postings"] * len(labels) + ["Patents"] * len(labels),
            })
            fig = px.bar(jp, x="Count", y="Route", color="Series", orientation="h",
                         barmode="group", text="Count", color_discrete_sequence=[SKY, GOLD])
            fig.update_traces(textposition="outside", hovertemplate="%{y}<br>%{x}<extra></extra>")
            if not is_all:
                fig.for_each_trace(lambda t: t.update(
                    marker_opacity=[1 if l[0] == cur else 0.3 for l in labels]))
            fig.update_layout(height=460, margin=dict(l=0, r=30, t=10, b=10),
                              xaxis_title="records", yaxis_title=None,
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                                          title=None))
            st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
            quote("From the working deck:", "Jobs → infrastructure. Patents → Reality Labs / "
                  "wearables. This means Chris should ask whether the university partnership lead "
                  "can route both lanes — the AI/data-center owners may be different from Reality "
                  "Labs or Meta AI research owners.")

    with right:
        with card():
            st.subheader("Technology themes in recent patent titles")
            st.caption("term frequency")
            terms = pd.DataFrame(list(reversed(D.TERMS)), columns=["Term", "Count"])
            fig = go.Figure()
            for _, row in terms.iterrows():
                fig.add_trace(go.Scatter(x=[0, row["Count"]], y=[row["Term"]] * 2, mode="lines",
                                         line=dict(color=GOLD_TINT, width=3), hoverinfo="skip",
                                         showlegend=False))
            fig.add_trace(go.Scatter(x=terms["Count"], y=terms["Term"], mode="markers+text",
                                     marker=dict(color=GOLD, size=11), text=terms["Count"],
                                     textposition="middle right", showlegend=False,
                                     hovertemplate="%{y}<br>%{x} mentions<extra></extra>"))
            fig.update_layout(height=460, margin=dict(l=0, r=40, t=10, b=10),
                              xaxis_title="term frequency in patent titles",
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
            quote("From the briefing report:", "Meta’s newest filings are hardware, not social "
                  "features — a direct read on sustained Reality Labs R&D.")

    st.caption("Sources: Meta FY2025 Form 10-K; Q1 2026 results; PitchBook (15 Jun 2026); "
               "D&SKY Hoovers; Meta Careers snapshot (June 2026); USPTO and Google Patents "
               "captures; IDC 2025 XR share.")


# --------------------------------------------------- CU relationship evidence -
def render_cu():
    st.header("04 · CU relationship evidence")
    st.caption("From the report: “The goal is not to count every mention of Facebook, Instagram, "
               "WhatsApp, PyTorch, Llama, AR/VR, or ‘meta.’ The goal is to separate direct "
               "relationship evidence from capability evidence.”")

    left, right = st.columns(2)
    with left:
        with card():
            st.subheader("Meta-related candidate rows by year")
            st.caption("before exclusion rules · 2019–2025")
            yrs = pd.DataFrame(D.YRS, columns=["Year", "Rows"])
            fig = px.area(yrs, x="Year", y="Rows", markers=True)
            fig.update_traces(line_color=SKY, fillcolor="rgba(9,111,174,0.10)",
                              hovertemplate="%{x}<br>%{y} rows<extra></extra>")
            fig.update_layout(height=320, margin=dict(l=0, r=10, t=10, b=10),
                              yaxis_title="rows", plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)")
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
            st.caption("The source file is labelled 2020–2025 but includes some 2019 rows.")

        with card():
            st.subheader("Signal rate by scholarly source")
            st.caption("Dimensions, 2019–2026")
            sig = pd.DataFrame(D.SIG, columns=["Source", "Scanned", "Signals", "Rate %"])
            st.dataframe(sig.style.format({"Scanned": "{:,}", "Rate %": "{:.2f}%"})
                         .map(lambda v: f"color:{DARKBLUE};font-weight:600" if v == 0.00 else "",
                              subset=["Rate %"]),
                         hide_index=True, width="stretch")
            quote("From the report:", "The scholarly scan also found no direct Meta-linked records "
                  "in the patents dataset (2019–2026)… it only means the reviewed CU patent "
                  "dataset did not surface a CU–Meta patent relationship signal.")

    with right:
        with card():
            st.subheader("Awarded and proposed value by route")
            st.caption("$4.80M awarded · $5.22M proposed")
            funded = [k for k in D.O if D.FUND[k][0] > 0 or D.FUND[k][1] > 0]
            keys = list(reversed(funded + [None]))
            names = [D.R[k]["n"] if k else "Unclassified" for k in keys]
            awarded = [D.FUND[k][0] if k else D.FUND_UNCLASSIFIED[0] for k in keys]
            proposed = [D.FUND[k][1] if k else D.FUND_UNCLASSIFIED[1] for k in keys]
            fund = pd.DataFrame({"Route": names * 2, "Value": awarded + proposed,
                                 "Series": ["Awarded"] * len(names) + ["Proposed"] * len(names)})
            fig = px.bar(fund, x="Value", y="Route", color="Series", orientation="h",
                         barmode="group", color_discrete_sequence=[GOLD, GOLD_TINT])
            fig.update_traces(hovertemplate="%{y}<br>$%{x:,.0f}<extra></extra>")
            if not is_all:
                fig.for_each_trace(lambda t: t.update(
                    marker_opacity=[1 if k == cur else 0.3 for k in keys]))
            fig.update_layout(height=320, margin=dict(l=0, r=10, t=10, b=10),
                              xaxis_title="US$", yaxis_title=None,
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                                          title=None))
            st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
            quote("From the report:", "The formal eRA evidence shows that CU Boulder’s direct Meta "
                  "activity is concentrated in Reality Labs / XR / wearables / displays / human "
                  "interfaces.")

        with card():
            st.subheader("Alumni by job function")
            st.caption("152 coded records · no names")
            alum = pd.DataFrame(list(reversed(D.ALUM)), columns=["Function", "Count"])
            fig = px.bar(alum, x="Count", y="Function", orientation="h", text="Count")
            fig.update_traces(marker_color=MUTED, textposition="outside",
                              hovertemplate="%{y}<br>%{x} alumni<extra></extra>")
            st.plotly_chart(bar_layout(fig, 340, "coded records"), config=PLOTLY_CONFIG, width="stretch")
            quote("From the report:", "Alumni can help identify language, teams, and internal "
                  "routing, but they should not be represented as committed contacts or "
                  "partnership sponsors without validation.")

    with card():
        st.subheader("Route strength across CU-side streams")
        st.caption("record counts")
        rmx = pd.DataFrame({
            "Route": [D.R[k]["n"] for k in D.O] + ["No strategic-route equivalent"],
            "Grants": [(D.ERA[k][0] + D.ERA[k][1]) or None for k in D.O]
                      + [D.RMX_NO_EQUIV["grants"]],
            "Faculty": [D.FRP[k][1] or None for k in D.O] + [D.RMX_NO_EQUIV["faculty"]],
            "Scholarly": [D.SCH[k][1] or None for k in D.O] + [D.RMX_NO_EQUIV["scholarly"]],
            "Alumni": [D.ALUMR.get(k) or None for k in D.O] + [D.RMX_NO_EQUIV["alumni"]],
        })
        if not is_all:
            rmx = rmx[rmx["Route"].isin([D.R[cur]["n"], "No strategic-route equivalent"])]
        st.dataframe(rmx, hide_index=True, width="stretch")
        st.caption("Records under “connectivity / data for good” and “unclassified”, activities "
                   "coded “route unclear”, and alumni in software engineering, general engineering "
                   "and unclear functions have no strategic-route equivalent and are shown "
                   "separately.")

    st.caption("Sources: CUB-Meta Activities_Awards, Proposals, Gifts.xlsx · "
               "CUB-Meta Activities_FRPA.xlsx · CUB-Meta Activities_Scholarly Works.xlsx · "
               "CUB-Meta_Route-Coded Activities.xlsx")


# ------------------------------------------------------------- researchers ---
def render_people():
    st.header("05 · Researchers")
    st.caption("The researchers named in the CU Boulder–Meta researcher briefing, shown by route. "
               "Use the column menus to sort and filter; the sidebar Route filter applies first.")

    rows = []
    for p in D.P:
        for rt in p[4]:
            if not is_all and cur != rt:
                continue
            rows.append({"Researcher": p[0], "Route": D.R[rt]["n"], "Unit": p[1],
                         "Focus": p[2], "Relevance to Meta": p[3],
                         "Evidence": "Relationship" if p[5] else "Capability"})

    if not rows:
        st.info("No researchers match this route.")
        return

    df = pd.DataFrame(rows)
    if not is_all:
        df = df.drop(columns=["Route"])

    # Cross-field search, matching the HTML's single search box. AG Grid's own
    # column filters (menu on each header) handle per-column narrowing.
    q = st.text_input("Search", placeholder="Name, unit or topic",
                      label_visibility="collapsed").lower().strip()
    if q:
        mask = df.apply(lambda r: q in " ".join(str(v) for v in r).lower(), axis=1)
        df = df[mask]
        if df.empty:
            st.info("No researchers match this search.")
            return

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(sortable=True, filter=True, resizable=True,
                                wrapText=True, autoHeight=True)
    gb.configure_column("Researcher", pinned="left", width=150)
    gb.configure_column("Focus", width=260)
    gb.configure_column("Relevance to Meta", width=300)
    # agSetColumnFilter is an AG Grid Enterprise module and renders an empty
    # panel in the community build, so these use the community text filter.
    gb.configure_column("Evidence", filter="agTextColumnFilter", width=130)
    gb.configure_column("Unit", filter="agTextColumnFilter", width=200)
    if "Route" in df.columns:
        gb.configure_column("Route", filter="agTextColumnFilter", width=170)
    gb.configure_grid_options(domLayout="normal", suppressCellFocus=True)

    AgGrid(df, gridOptions=gb.build(), height=520, theme="alpine",
           allow_unsafe_jscode=False, fit_columns_on_grid_load=False,
           columns_auto_size_mode=ColumnsAutoSizeMode.NO_AUTOSIZE,
           key=f"grid_{cur}_{hash(q)}")

    n, u = len(df), df["Researcher"].nunique()
    st.caption(f"{n} assignment{'' if n == 1 else 's'} · {u} researcher"
               f"{'' if u == 1 else 's'} before column filters")
    quote("From the report:", "Names below should be treated as validation candidates for Chris’s "
          "meeting and follow-up. Faculty interest, current title, current unit, and willingness "
          "to be named externally should be validated before sending a list to Meta.")


# -------------------------------------------------------- strategic foresight -
def render_foresight():
    st.header("06 · Strategic foresight")
    st.caption("From the report: “These scenarios are not predictions. They are structured stress "
               "tests.” Select one below to see which routes the report identifies as leading "
               "under that future.")

    cols = st.columns(4)
    for col, s in zip(cols, D.SC):
        with col:
            with card():
                st.markdown(f"**Scenario {s['k']} · {s['t']}**")
                st.caption(s["d"])
                selected = st.session_state.scen == s["k"]
                if st.button("Selected" if selected else "Select",
                             key=f"scen{s['k']}", width="stretch",
                             type="primary" if selected else "secondary"):
                    st.session_state.scen = "none" if selected else s["k"]
                    st.rerun()

    if st.session_state.scen == "none":
        st.info("Select a scenario above to see which routes the report identifies as leading, "
                "and what it cautions about.")
    else:
        s = next(x for x in D.SC if x["k"] == st.session_state.scen)
        with card():
            st.subheader(f"Under scenario {s['k']} · {s['t']}")
            st.write(s["l"])
            order = list(reversed(D.O))
            lead = pd.DataFrame({"Route": [D.R[k]["n"] for k in order],
                                 "Score": [D.R[k]["w"] for k in order]})
            fig = px.bar(lead, x="Score", y="Route", orientation="h", range_x=[0, 5], text="Score")
            fig.update_traces(
                marker_color=[GOLD if k in s["r"] else MUTED for k in order],
                marker_opacity=[1 if k in s["r"] else 0.3 for k in order],
                texttemplate="%{text:.1f}", textposition="outside",
                hovertemplate="%{y}<br>Weighted score %{x:.1f}<extra></extra>")
            st.plotly_chart(bar_layout(fig, 340, "weighted score, 0 to 5"), config=PLOTLY_CONFIG, width="stretch")
            st.caption(f"Leading routes: {', '.join(D.R[k]['n'] for k in s['r'])}.")
            st.warning(f"**Risk or caution.** {s['c']}")

    with card():
        st.subheader("Foresight validation matrix")
        st.caption("durability through 2028")
        st.dataframe(pd.DataFrame(D.FM, columns=[
            "Thrust zone", "Durability", "Evidence", "CU alignment", "Route clarity",
            "Strategic interpretation"]), hide_index=True, width="stretch")
        quote("From the report:", "The same CU capabilities appear in multiple scenarios: AI "
              "evaluation, human-centered AI, accessibility, multimodal perception, "
              "displays/optics, energy systems, water, cybersecurity, privacy, and platform "
              "governance. That makes them better strategic bets than narrower, product-specific "
              "pitches.")

    with card():
        st.subheader("Early-warning indicators")
        st.caption("monitor after the meeting")
        st.dataframe(pd.DataFrame(D.W, columns=["Indicator", "Why it matters", "Route affected"]),
                     hide_index=True, width="stretch")
        quote("From the report:", "The following indicators should be monitored after Chris’s Meta "
              "meeting because they will help determine whether the recommended CU routes are "
              "strengthening, weakening, or shifting.")


# ------------------------------------------------------------------ router ---
{"Overview": render_overview, "Route detail": render_route_detail,
 "Company signals": render_company, "CU relationship evidence": render_cu,
 "Researchers": render_people, "Strategic foresight": render_foresight}[section]()

st.divider()
st.caption("All interpretive text on this page is quoted from the CU Boulder–Meta Alignment "
           "Intelligence Report, its supporting workbooks, and the researcher briefing. Figures "
           "are unchanged from those sources.")
st.caption("Interactive companion · last updated 2 August 2026 · prepared by Om Kokate for review "
           "by Lisa Nanstad, Research Intelligence Strategist, RIO.")
