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
# CUSTOM CSS
# =========================

st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; color: #e0e0e0; }
    .stApp > header { background-color: #1a1a2e; }

    [data-testid="stSidebar"] {
        background-color: #16213e;
        border-right: 1px solid #0f3460;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p { color: #a0c4ff !important; }

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
    }

    .kpi-card {
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border: 1px solid #0f3460;
        border-left: 4px solid #00d4ff;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 8px;
        min-height: 100px;
    }
    .kpi-label {
        font-size: 0.68rem;
        color: #8899aa;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }
    .kpi-delta { font-size: 0.75rem; color: #4ade80; margin-top: 4px; }
    .kpi-delta-neg { font-size: 0.75rem; color: #fb923c; margin-top: 4px; }

    .section-title {
        background-color: #0f3460;
        border-left: 4px solid #00d4ff;
        padding: 8px 16px;
        border-radius: 4px;
        margin: 20px 0 14px 0;
        color: #ffffff !important;
        font-size: 0.82rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="stAlert"] {
        background-color: #16213e !important;
        border: 1px solid #0f3460 !important;
        border-radius: 6px;
        color: #c0d8f0 !important;
    }

    /* Tabs styling */
    [data-testid="stTabs"] [role="tablist"] {
        background-color: #16213e;
        border-bottom: 2px solid #0f3460;
        padding: 0 4px;
        gap: 2px;
    }
    [data-testid="stTabs"] button[role="tab"] {
        color: #8899aa !important;
        font-size: 0.78rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        padding: 10px 18px !important;
        border-radius: 6px 6px 0 0;
        border: none;
        background: transparent;
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #00d4ff !important;
        background-color: #0f3460 !important;
        border-bottom: 2px solid #00d4ff;
    }

    hr { border-color: #0f3460 !important; margin: 1.2rem 0 !important; }
    .stCaption { color: #556677 !important; font-size: 0.70rem !important; }
    .gtitle { display: none !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# PLOTLY THEME
# =========================

_layout = dict(
    paper_bgcolor="#16213e",
    plot_bgcolor="#1a1a2e",
    font=dict(color="#c0d8f0", size=12),
    xaxis=dict(gridcolor="#1e3a5f", linecolor="#0f3460", tickfont=dict(color="#8899aa")),
    yaxis=dict(gridcolor="#1e3a5f", linecolor="#0f3460", tickfont=dict(color="#8899aa")),
    legend=dict(bgcolor="#16213e", bordercolor="#0f3460", borderwidth=1, font=dict(color="#c0d8f0")),
    margin=dict(t=20, l=10, r=10, b=10),
    colorway=["#00d4ff", "#7b61ff", "#4ade80", "#fb923c", "#f472b6"]
)

def theme(fig):
    fig.update_layout(**_layout)
    fig.update_layout(title_text="")
    return fig

def kpi(label, value, delta="", color="#00d4ff", delta_neg=False):
    delta_class = "kpi-delta-neg" if delta_neg else "kpi-delta"
    font_size = "1.3rem" if len(str(value)) > 8 else "1.8rem"
    return f"""
    <div class="kpi-card" style="border-left-color:{color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="font-size:{font_size};white-space:nowrap;">{value}</div>
        <div class="{delta_class}">{delta}</div>
    </div>"""

def section(icon, title):
    st.markdown(f'<div class="section-title">{icon} {title}</div>', unsafe_allow_html=True)

# =========================
# DATA LOADING
# =========================

@st.cache_data
def load_data():
    return pd.read_csv("data/electric_car_sales.csv")

@st.cache_data
def calc_cagr(df, region, powertrain, y_start, y_end):
    d = df[(df["region"] == region) & (df["parameter"] == "EV sales") & (df["powertrain"] == powertrain)].sort_values("year")
    try:
        s = d[d["year"] == y_start]["value"].iloc[0]
        e = d[d["year"] == y_end]["value"].iloc[0]
        return ((e / s) ** (1 / (y_end - y_start)) - 1) * 100
    except:
        return 0.0

@st.cache_data
def forecast_sales(start_sales, start_year, end_year, scenarios):
    results = []
    for name, rate in scenarios.items():
        sales = start_sales
        for year in range(start_year + 1, end_year + 1):
            sales *= (1 + rate)
            results.append({"Scenariusz": name, "Rok": year, "Sprzedaż": round(sales)})
    return pd.DataFrame(results)

@st.cache_data
def forecast_infra(ev_counts, ratio):
    return pd.DataFrame({
        "Scenariusz": [f"{int(n/1000)}k EV" for n in ev_counts],
        "Punkty ładowania": [round(n / ratio) for n in ev_counts]
    })

df = load_data()

# Static recent data (2024-2026 estimates based on PSNM)
recent_df = pd.DataFrame({
    "Rok": ["2023", "2024", "2025"],
    "BEV": [17_000, 29_400, 43_100],
    "PHEV": [13_000, 18_500, 24_200]
})

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown("## ⚡ EV Poland")
    st.markdown("---")
    st.markdown("### Filtry globalne")

    country = st.selectbox(
        "Kraj / region",
        sorted(df["region"].unique()),
        index=sorted(df["region"].unique()).index("Poland")
    )

    powertrain_filter = st.multiselect(
        "Typ napędu",
        options=["BEV", "PHEV"],
        default=["BEV", "PHEV"],
        format_func=lambda x: x
    )

    year_range = st.slider(
        "Zakres lat",
        min_value=int(df["year"].min()),
        max_value=int(df["year"].max()),
        value=(2015, 2023)
    )

    st.markdown("---")
    st.caption("Źródła: IEA · PSNM · PZPM\nAktualizacja: 2026")

# =========================
# KPI CALCULATIONS (from real data)
# =========================

latest_share_val = df[
    (df["region"] == country) & (df["parameter"] == "EV sales share") & (df["powertrain"] == "EV")
]["value"].max()

eu_share_2023 = df[
    (df["region"] == "Europe") & (df["parameter"] == "EV sales share") & (df["powertrain"] == "EV") & (df["year"] == 2023)
]["value"].values[0] if "Europe" in df["region"].values else 21.0

bev_sales_2023 = df[
    (df["region"] == country) & (df["parameter"] == "EV sales") & (df["powertrain"] == "BEV") & (df["year"] == 2023)
]["value"].sum()

phev_sales_2023 = df[
    (df["region"] == country) & (df["parameter"] == "EV sales") & (df["powertrain"] == "PHEV") & (df["year"] == 2023)
]["value"].sum()

total_sales_2023 = bev_sales_2023 + phev_sales_2023

ev_stock_2023 = df[
    (df["region"] == country) & (df["parameter"] == "EV stock") & (df["powertrain"].isin(["BEV", "PHEV"])) & (df["year"] == 2023)
]["value"].sum()

cagr_bev = calc_cagr(df, country, "BEV", 2020, 2023)

gap_to_eu = eu_share_2023 - latest_share_val

# =========================
# HEADER
# =========================

st.markdown(
    f"<h1>⚡ EV Market Poland"
    f"<span style='font-size:0.85rem;color:#8899aa;font-weight:400;margin-left:16px;'>"
    f"Dashboard · Market Snapshot 2026</span></h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Przegląd",
    "📈  Sprzedaż",
    "🔌  Infrastruktura",
    "🔮  Prognozy 2030"
])

# ──────────────────────────────────────────────
# TAB 1: PRZEGLĄD
# ──────────────────────────────────────────────

with tab1:

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi("Udział EV w rynku (2023)", f"{latest_share_val:.1f}%",
                        f"▼ {gap_to_eu:.1f}pp za Europą ({eu_share_2023:.0f}%)",
                        "#00d4ff", delta_neg=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi("Łączna sprzedaż EV (2023)", f"{int(total_sales_2023):,}",
                        f"BEV: {int(bev_sales_2023):,}  ·  PHEV: {int(phev_sales_2023):,}",
                        "#7b61ff"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi("Łączny stock EV (2023)", f"{int(ev_stock_2023):,}",
                        "▲ +73% vs 2022", "#4ade80"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi("CAGR BEV 2020–2023", f"{cagr_bev:.1f}%",
                        "Roczny wzrost sprzedaży BEV", "#fb923c"), unsafe_allow_html=True)

    # Polska vs Europa — overview chart
    section("🌍", f"{country} vs Europa — udział EV w rynku (2010–2023)")

    comparison = df[
        (df["region"].isin([country, "Europe"])) &
        (df["parameter"] == "EV sales share") &
        (df["powertrain"] == "EV")
    ]

    fig_cmp = px.line(comparison, x="year", y="value", color="region", markers=True, title=" ",
                      labels={"value": "Udział rynkowy (%)", "year": "Rok", "region": "Region"})
    fig_cmp = theme(fig_cmp)
    fig_cmp.update_traces(line=dict(width=2.5), marker=dict(size=6))
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Insights row
    section("💡", "Key Insights")
    i1, i2, i3 = st.columns(3)
    with i1:
        st.success(f"**CAGR BEV {cagr_bev:.0f}%/rok**\n\nSprzedaż BEV w Polsce rosła średnio {cagr_bev:.1f}% rocznie w latach 2020–2023.")
    with i2:
        st.info(f"**Luka do Europy: {gap_to_eu:.1f}pp**\n\nPolska ({latest_share_val:.1f}%) vs Europa ({eu_share_2023:.0f}%) — duży potencjał wzrostu.")
    with i3:
        st.warning("**Stock rośnie szybciej niż share**\n\nPrzy ~99k EV na drogach (2023), udział wciąż poniżej 7% — oznacza to młody rynek z wysoką bazą wzrostu.")

# ──────────────────────────────────────────────
# TAB 2: SPRZEDAŻ
# ──────────────────────────────────────────────

with tab2:

    section("📈", f"Historia sprzedaży — {country} ({year_range[0]}–{year_range[1]})")

    sales_data = df[
        (df["region"] == country) &
        (df["parameter"] == "EV sales") &
        (df["powertrain"].isin(powertrain_filter)) &
        (df["year"].between(*year_range))
    ]

    fig_hist = px.line(sales_data, x="year", y="value", color="powertrain", markers=True, title=" ",
                       labels={"value": "Liczba pojazdów", "year": "Rok", "powertrain": "Napęd"})
    fig_hist = theme(fig_hist)
    fig_hist.update_traces(line=dict(width=2.5), marker=dict(size=7))
    st.plotly_chart(fig_hist, use_container_width=True)

    section("📊", "Sprzedaż BEV + PHEV (2023–2025) — szacunki PSNM")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        fig_recent = go.Figure()
        fig_recent.add_trace(go.Bar(
            name="BEV", x=recent_df["Rok"], y=recent_df["BEV"],
            marker_color="#00d4ff",
            text=[f"{v:,}" for v in recent_df["BEV"]],
            textposition="outside", textfont=dict(color="#ffffff")
        ))
        fig_recent.add_trace(go.Bar(
            name="PHEV", x=recent_df["Rok"], y=recent_df["PHEV"],
            marker_color="#7b61ff",
            text=[f"{v:,}" for v in recent_df["PHEV"]],
            textposition="outside", textfont=dict(color="#ffffff")
        ))
        fig_recent.update_layout(**_layout, barmode="group", showlegend=True, title_text="")
        st.plotly_chart(fig_recent, use_container_width=True)

    with col_b:
        st.markdown(kpi("BEV 2025 (est.)", "43 100", "▲ +47% vs 2024", "#4ade80"), unsafe_allow_html=True)
        st.markdown(kpi("PHEV 2025 (est.)", "24 200", "▲ +31% vs 2024", "#7b61ff"), unsafe_allow_html=True)
        st.markdown(kpi("Łącznie 2025", "67 300", "▲ +41% YoY", "#fb923c"), unsafe_allow_html=True)
        st.caption("Dane szacunkowe PSNM/PZPM — nie zawarte w zbiorze IEA")

    section("📉", "EV Stock — skumulowana flota EV w Polsce")

    stock_data = df[
        (df["region"] == country) &
        (df["parameter"] == "EV stock") &
        (df["powertrain"].isin(["BEV", "PHEV"]))
    ]

    fig_stock = px.area(stock_data, x="year", y="value", color="powertrain", title=" ",
                        labels={"value": "Liczba pojazdów (stock)", "year": "Rok", "powertrain": "Napęd"})
    fig_stock = theme(fig_stock)
    fig_stock.update_traces(line=dict(width=2))
    st.plotly_chart(fig_stock, use_container_width=True)

# ──────────────────────────────────────────────
# TAB 3: INFRASTRUKTURA
# ──────────────────────────────────────────────

with tab3:

    section("🔌", "Stan infrastruktury ładowania — Polska 2026")

    ci1, ci2, ci3 = st.columns(3)
    with ci1:
        st.markdown(kpi("Punkty ładowania", "12 431", "▲ +2 104 vs 2025", "#4ade80"), unsafe_allow_html=True)
    with ci2:
        st.markdown(kpi("EV / punkt ładowania", "20.3", "Cel EU: max 10 EV/punkt", "#fb923c", delta_neg=True), unsafe_allow_html=True)
    with ci3:
        st.markdown(kpi("Stacje szybkie DC", "5 890", "47% całości infrastruktury", "#7b61ff"), unsafe_allow_html=True)

    section("⚡", "AC vs DC — podział punktów ładowania")

    charging = pd.DataFrame({
        "Typ": ["AC — wolne ładowanie", "DC — szybkie ładowanie"],
        "Liczba": [6_541, 5_890],
        "Kolor": ["#00d4ff", "#7b61ff"]
    })

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        fig_ch = go.Figure(go.Bar(
            x=charging["Typ"], y=charging["Liczba"],
            marker_color=charging["Kolor"],
            text=[f"{v:,}" for v in charging["Liczba"]],
            textposition="outside", textfont=dict(color="#ffffff")
        ))
        fig_ch.update_layout(**_layout, showlegend=False, title_text="")
        st.plotly_chart(fig_ch, use_container_width=True)

    with col_c2:
        fig_pie = go.Figure(go.Pie(
            labels=charging["Typ"],
            values=charging["Liczba"],
            marker=dict(colors=["#00d4ff", "#7b61ff"]),
            hole=0.5,
            textfont=dict(color="#ffffff", size=12)
        ))
        fig_pie.update_layout(**_layout, showlegend=True, title_text="")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.info("🔍 Polska ma jeden z wyższych wskaźników EV/punkt w UE. Norma europejska to max 10 EV na 1 punkt ładowania — przy obecnym tempie wzrostu EV, infrastruktura wymaga podwojenia do 2027.")

# ──────────────────────────────────────────────
# TAB 4: PROGNOZY 2030
# ──────────────────────────────────────────────

with tab4:

    section("🔮", "Prognoza sprzedaży BEV 2024–2030 — 3 scenariusze")

    scenarios = {
        "Konserwatywny (+15%/rok)": 0.15,
        "Bazowy (+25%/rok)": 0.25,
        "Optymistyczny (+35%/rok)": 0.35
    }

    forecast_df = forecast_sales(17_000, 2023, 2030, scenarios)

    fig_fc = px.line(forecast_df, x="Rok", y="Sprzedaż", color="Scenariusz", markers=True, title=" ",
                     labels={"Sprzedaż": "Sprzedaż BEV (szt.)", "Rok": "Rok"})
    fig_fc = theme(fig_fc)
    fig_fc.update_traces(line=dict(width=2.5), marker=dict(size=6))

    # Add 2023 reference point
    fig_fc.add_scatter(x=[2023], y=[17_000], mode="markers",
                       marker=dict(color="#ffffff", size=10, symbol="diamond"),
                       name="Dane rzeczywiste 2023", showlegend=True)
    st.plotly_chart(fig_fc, use_container_width=True)

    # 2030 end values
    p1, p2, p3 = st.columns(3)
    end_vals = forecast_df[forecast_df["Rok"] == 2030].set_index("Scenariusz")["Sprzedaż"]
    with p1:
        v = end_vals.get("Konserwatywny (+15%/rok)", 0)
        st.markdown(kpi("Konserwatywny — 2030", f"{int(v):,}", "+15%/rok od 2023", "#8899aa"), unsafe_allow_html=True)
    with p2:
        v = end_vals.get("Bazowy (+25%/rok)", 0)
        st.markdown(kpi("Bazowy — 2030", f"{int(v):,}", "+25%/rok od 2023", "#00d4ff"), unsafe_allow_html=True)
    with p3:
        v = end_vals.get("Optymistyczny (+35%/rok)", 0)
        st.markdown(kpi("Optymistyczny — 2030", f"{int(v):,}", "+35%/rok od 2023", "#4ade80"), unsafe_allow_html=True)

    section("🔌", "Wymagana infrastruktura ładowania — 2030")

    infra_df = forecast_infra([500_000, 750_000, 1_000_000], 10.0)  # EU target: 10 EV/charger

    fig_infra = go.Figure(go.Bar(
        x=infra_df["Scenariusz"],
        y=infra_df["Punkty ładowania"],
        marker=dict(
            color=infra_df["Punkty ładowania"],
            colorscale=[[0, "#0f3460"], [0.5, "#00d4ff"], [1, "#4ade80"]],
            showscale=False
        ),
        text=[f"{v:,}" for v in infra_df["Punkty ładowania"]],
        textposition="outside", textfont=dict(color="#ffffff")
    ))
    fig_infra.update_layout(**_layout, showlegend=False, title_text="")

    col_i1, col_i2 = st.columns([2, 1])
    with col_i1:
        st.plotly_chart(fig_infra, use_container_width=True)
    with col_i2:
        st.markdown(kpi("Obecna infrastruktura", "12 431", "Stan: 2026", "#fb923c"), unsafe_allow_html=True)
        st.markdown(kpi("Luka przy 1M EV", "87 569", "Punktów do zbudowania", "#f472b6", delta_neg=True), unsafe_allow_html=True)
        st.caption("Prognoza zakłada cel EU: max 10 EV/punkt ładowania")

    st.warning("⚠️ Prognozy oparte na założeniu stałej stopy wzrostu. Rzeczywiste wyniki zależą od polityki dopłat, cen energii i dostępności modeli EV.")

# =========================
# FOOTER
# =========================

st.markdown("---")
st.caption(
    "Źródła: International Energy Agency (IEA) — Global EV Data Explorer · "
    "Polish New Mobility Association (PSNM) · "
    "Polish Automotive Industry Association (PZPM) · "
    "Dashboard v3.0 — 2026"
)
