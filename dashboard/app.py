import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="EV Market Poland",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS — Power BI Dark Theme
# =========================

st.markdown("""
<style>
    /* ── Base & Background ── */
    .stApp {
        background-color: #1a1a2e;
        color: #e0e0e0;
    }
    .stApp > header {
        background-color: #1a1a2e;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #16213e;
        border-right: 1px solid #0f3460;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #a0c4ff !important;
    }

    /* ── Title ── */
    h1 {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #a0c4ff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem !important;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border: 1px solid #0f3460;
        border-left: 4px solid #00d4ff;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 0.72rem;
        color: #8899aa;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }
    .kpi-delta {
        font-size: 0.78rem;
        color: #4ade80;
        margin-top: 4px;
    }

    /* ── Section Divider ── */
    .section-title {
        background-color: #0f3460;
        border-left: 4px solid #00d4ff;
        padding: 8px 16px;
        border-radius: 4px;
        margin: 24px 0 16px 0;
        color: #ffffff !important;
        font-size: 0.85rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Info Boxes ── */
    [data-testid="stAlert"] {
        background-color: #16213e;
        border: 1px solid #0f3460;
        border-radius: 6px;
        color: #c0d8f0 !important;
    }

    /* ── Metric widget override ── */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #8899aa !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
    }

    /* ── Plotly chart containers ── */
    .js-plotly-plot {
        border-radius: 8px;
        border: 1px solid #0f3460;
    }

    /* ── Horizontal rule ── */
    hr {
        border-color: #0f3460 !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Footer caption ── */
    .stCaption {
        color: #556677 !important;
        font-size: 0.72rem !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# PLOTLY THEME
# =========================

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="#16213e",
        plot_bgcolor="#1a1a2e",
        font=dict(color="#c0d8f0", size=12),
        title=dict(font=dict(color="#ffffff", size=14), x=0.02),
        xaxis=dict(
            gridcolor="#1e3a5f",
            linecolor="#0f3460",
            tickfont=dict(color="#8899aa")
        ),
        yaxis=dict(
            gridcolor="#1e3a5f",
            linecolor="#0f3460",
            tickfont=dict(color="#8899aa")
        ),
        legend=dict(
            bgcolor="#16213e",
            bordercolor="#0f3460",
            borderwidth=1,
            font=dict(color="#c0d8f0")
        ),
        margin=dict(t=50, l=10, r=10, b=10),
        colorway=["#00d4ff", "#7b61ff", "#4ade80", "#fb923c", "#f472b6"]
    )
)

def apply_theme(fig):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    return fig

# =========================
# LOAD DATA
# =========================

@st.cache_data
def load_data():
    df = pd.read_csv("data/electric_car_sales.csv")
    return df

df = load_data()

# Recent data (2023-2026) — define manually since not in CSV
recent_df = pd.DataFrame({
    "year": [2023, 2024, 2025],
    "bev_sales": [17_200, 29_400, 43_100]
})

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown("## ⚡ EV Poland")
    st.markdown("---")
    st.markdown("### Filtry")

    country = st.selectbox(
        "Kraj",
        sorted(df["region"].unique()),
        index=sorted(df["region"].unique()).index("Poland")
    )

    powertrain_filter = st.multiselect(
        "Typ napędu",
        ["BEV", "PHEV"],
        default=["BEV", "PHEV"]
    )

    st.markdown("---")
    st.caption("Dane: IEA · PSNM · PZPM\nAktualizacja: 2026")

# =========================
# KPI CALCULATIONS
# =========================

latest_sales = df[
    (df["region"] == country)
    & (df["parameter"] == "EV sales")
    & (df["year"] == 2023)
]["value"].sum()

latest_share = df[
    (df["region"] == country)
    & (df["parameter"] == "EV sales share")
    & (df["powertrain"] == "EV")
]["value"].max()

# =========================
# HEADER
# =========================

st.markdown(
    f"<h1>⚡ EV Market Poland &nbsp;&nbsp;"
    f"<span style='font-size:0.9rem;color:#8899aa;font-weight:400'>"
    f"Dashboard · Market Snapshot 2026</span></h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# =========================
# KPI CARDS — HTML custom style
# =========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">EV Market Share (2023)</div>
        <div class="kpi-value">{latest_share:.1f}%</div>
        <div class="kpi-delta">▲ vs. 2022</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:#7b61ff;">
        <div class="kpi-label">Passenger EVs (2026)</div>
        <div class="kpi-value">252 338</div>
        <div class="kpi-delta">▲ +18% YoY</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:#4ade80;">
        <div class="kpi-label">Charging Points (2026)</div>
        <div class="kpi-value">12 431</div>
        <div class="kpi-delta">▲ +2 104 vs. 2025</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:#fb923c;">
        <div class="kpi-label">EV Sales (2023)</div>
        <div class="kpi-value">{int(latest_sales):,}</div>
        <div class="kpi-delta">BEV + PHEV</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# HISTORICAL SALES
# =========================

st.markdown(
    f'<div class="section-title">📈 Historical EV Sales — {country} (2010–2023)</div>',
    unsafe_allow_html=True
)

sales_data = df[
    (df["region"] == country)
    & (df["parameter"] == "EV sales")
    & (df["powertrain"].isin(powertrain_filter))
]

fig = px.line(
    sales_data,
    x="year",
    y="value",
    color="powertrain",
    markers=True,
    labels={"value": "Liczba pojazdów", "year": "Rok", "powertrain": "Napęd"}
)
fig = apply_theme(fig)
fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
st.plotly_chart(fig, use_container_width=True)

with st.expander("💬 Komentarz rynkowy"):
    st.info(
        f"Rynek EV w **{country}** znacznie przyspieszył po 2020 roku. "
        f"Wykres pokazuje dynamikę sprzedaży BEV vs PHEV, "
        f"co pozwala ocenić czy konsumenci preferują pojazdy w pełni elektryczne "
        f"czy hybrydy plug-in."
    )

# =========================
# COUNTRY VS EUROPE
# =========================

st.markdown(
    f'<div class="section-title">🌍 {country} vs Europa — udział EV w rynku</div>',
    unsafe_allow_html=True
)

comparison = df[
    (df["region"].isin([country, "Europe"]))
    & (df["parameter"] == "EV sales share")
    & (df["powertrain"] == "EV")
]

fig2 = px.line(
    comparison,
    x="year",
    y="value",
    color="region",
    markers=True,
    labels={"value": "Udział (%)", "year": "Rok", "region": "Region"}
)
fig2 = apply_theme(fig2)
fig2.update_traces(line=dict(width=2.5), marker=dict(size=6))
st.plotly_chart(fig2, use_container_width=True)

# =========================
# RECENT MARKET PERFORMANCE
# =========================

st.markdown(
    '<div class="section-title">📊 Recent Performance — rejestracje BEV (2023–2025)</div>',
    unsafe_allow_html=True
)

fig_recent = go.Figure(go.Bar(
    x=recent_df["year"].astype(str),
    y=recent_df["bev_sales"],
    marker_color=["#00d4ff", "#7b61ff", "#4ade80"],
    text=recent_df["bev_sales"].apply(lambda x: f"{x:,}"),
    textposition="outside",
    textfont=dict(color="#ffffff")
))
fig_recent.update_layout(
    **PLOTLY_TEMPLATE["layout"],
    showlegend=False,
    yaxis_title="Rejestracje BEV",
    xaxis_title="Rok"
)
st.plotly_chart(fig_recent, use_container_width=True)

st.info(
    "Rejestracje BEV wzrosły z ~17 000 w 2023 r. do ponad 43 000 w 2025 r. "
    "Dane za 2026 r. sugerują dalszy wzrost rynku."
)

# =========================
# INFRASTRUCTURE 2026
# =========================

st.markdown(
    '<div class="section-title">🔌 Infrastruktura ładowania — stan 2026</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="kpi-card" style="border-left-color:#4ade80; margin-top:12px;">
        <div class="kpi-label">Punkty ładowania</div>
        <div class="kpi-value">12 431</div>
    </div>
    <div class="kpi-card" style="border-left-color:#fb923c; margin-top:8px;">
        <div class="kpi-label">EV / punkt ładowania</div>
        <div class="kpi-value">20.3</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    charging = pd.DataFrame({
        "Typ": ["AC (wolne)", "DC (szybkie)"],
        "Liczba": [6541, 5890]
    })
    fig3 = go.Figure(go.Bar(
        x=charging["Typ"],
        y=charging["Liczba"],
        marker_color=["#00d4ff", "#7b61ff"],
        text=charging["Liczba"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(color="#ffffff")
    ))
    fig3.update_layout(**PLOTLY_TEMPLATE["layout"], showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# INFRASTRUCTURE 2030
# =========================

st.markdown(
    '<div class="section-title">🔮 Prognoza infrastruktury — 2030</div>',
    unsafe_allow_html=True
)

forecast_chargers = pd.DataFrame({
    "Scenariusz": ["500k EV", "750k EV", "1M EV"],
    "Potrzebne punkty": [24_631, 36_946, 49_261]
})

fig4 = go.Figure(go.Bar(
    x=forecast_chargers["Scenariusz"],
    y=forecast_chargers["Potrzebne punkty"],
    marker=dict(
        color=forecast_chargers["Potrzebne punkty"],
        colorscale=[[0, "#0f3460"], [0.5, "#00d4ff"], [1, "#4ade80"]],
        showscale=False
    ),
    text=forecast_chargers["Potrzebne punkty"].apply(lambda x: f"{x:,}"),
    textposition="outside",
    textfont=dict(color="#ffffff")
))
fig4.update_layout(**PLOTLY_TEMPLATE["layout"], showlegend=False)
st.plotly_chart(fig4, use_container_width=True)

# =========================
# KEY INSIGHTS
# =========================

st.markdown(
    '<div class="section-title">💡 Key Insights</div>',
    unsafe_allow_html=True
)

ins1, ins2, ins3 = st.columns(3)
with ins1:
    st.success(f"**Wzrost po 2020**\n\nRynek EV w {country} znacznie przyspieszył — sprzedaż BEV rosła średnio >40% rocznie.")
with ins2:
    st.info(f"**Udział rynkowy**\n\nUdział EV wyniósł **{latest_share:.1f}%** w ostatnim dostępnym roku — poniżej średniej europejskiej.")
with ins3:
    st.warning("**Infrastruktura**\n\nRozbudowa sieci ładowania będzie kluczowa — przy 1M EV potrzeba ~49 tys. punktów.")

# =========================
# FOOTER / SOURCES
# =========================

st.markdown("---")
st.caption(
    "Źródła: International Energy Agency (IEA) · "
    "Polish New Mobility Association (PSNM) · "
    "Polish Automotive Industry Association (PZPM) · "
    "Dashboard v2.0 — 2026"
)
