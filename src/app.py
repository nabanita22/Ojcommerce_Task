import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calculations import get_customer_metrics

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="QuickKart Dashboard", layout="wide", page_icon="🛒")

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE, "Data", "analysis_data", "master.csv")
    df   = pd.read_csv(path)
    df["created_at"] = pd.to_datetime(df["created_at"])
    for col in ["carrier","delivery_status","city","category","segment","customer_type","rating_bin","route_covered"]:
        df[col] = df[col].fillna("Unknown")
    return df

df               = load_data()
customer_metrics = get_customer_metrics(df)
all_cities       = sorted(df["city"].unique())

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.header("🔧 Filters")

# Date range picker
st.sidebar.subheader("📅 Date Range")
min_date   = df["created_at"].min().date()
max_date   = df["created_at"].max().date()
date_range = st.sidebar.date_input("Select Date Range",
                                    value=(min_date, max_date),
                                    min_value=min_date,
                                    max_value=max_date)

# Year option
year_option = st.sidebar.radio("Year", ["2024", "2025", "Compare (H2 Only)"])

# Other filters
city     = st.sidebar.multiselect("City",     sorted(df["city"].unique()),     default=sorted(df["city"].unique()))
category = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
carrier  = st.sidebar.multiselect("Carrier",  sorted(df["carrier"].unique()),  default=sorted(df["carrier"].unique()))

# Metric selector
metric = st.sidebar.selectbox("📊 Metric Selector",
                               ["GMV", "Orders", "Repeat Rate", "Delayed Order Rate"])

# Breakdown toggle
breakdown = st.sidebar.radio("📍 Breakdown By", ["City", "Carrier"])

# ============================================================
# APPLY FILTERS
# ============================================================
H2_MONTHS      = [7, 8, 9, 10, 11, 12]
delay_statuses = ["Late_1_2d","Late_3_5d","Late_5p","Lost"]
month_order    = ["January","February","March","April","May","June",
                  "July","August","September","October","November","December"]

# Date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["created_at"].dt.date >= start_date) &
            (df["created_at"].dt.date <= end_date)]

# Year filter
if year_option == "2024":
    filtered = df[df["order_year"] == 2024]
elif year_option == "2025":
    filtered = df[df["order_year"] == 2025]
else:
    filtered = df[df["order_month"].isin(H2_MONTHS)]

# Other filters
filtered = filtered[
    (filtered["city"].isin(city))         &
    (filtered["category"].isin(category)) &
    (filtered["carrier"].isin(carrier))
]

# Customer metrics filter by year
if year_option == "2024":
    cm = customer_metrics[customer_metrics["order_year"] == 2024]
elif year_option == "2025":
    cm = customer_metrics[customer_metrics["order_year"] == 2025]
else:
    cm = customer_metrics[customer_metrics["order_month"].isin(H2_MONTHS)]

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def get_timeseries(data):
    grp = ["order_year","order_month","order_monthname"]

    if metric == "GMV":
        ts = (data.groupby(grp)["GMV"].sum() / 1e7).round(2).reset_index()
        ts.rename(columns={"GMV":"value"}, inplace=True)
        y_label = "GMV (₹ Crores)"

    elif metric == "Orders":
        ts = data.groupby(grp)["order_id"].nunique().reset_index()
        ts.rename(columns={"order_id":"value"}, inplace=True)
        y_label = "Number of Orders"

    elif metric == "Repeat Rate":
        ts = cm[["order_year","order_month","order_monthname","repeat_purchase_rate"]].copy()
        ts.rename(columns={"repeat_purchase_rate":"value"}, inplace=True)
        y_label = "Repeat Rate %"

    elif metric == "Delayed Order Rate":
        ts = (data.groupby(grp)
              .apply(lambda x: round(x["delivery_status"].isin(delay_statuses).sum() /
                                     max(len(x),1) * 100, 2))
              .reset_index(name="value"))
        y_label = "Delayed Order Rate %"

    # Fix — convert year to string FIRST then sort then categorical
    ts["order_year"]      = ts["order_year"].astype(str)
    ts                    = ts.sort_values(["order_year","order_month"])
    ts["order_monthname"] = pd.Categorical(ts["order_monthname"],
                                            categories=month_order, ordered=True)
    return ts, y_label


def get_breakdown(data):
    grp_col = "city" if breakdown == "City" else "carrier"

    if metric == "GMV":
        bd = (data.groupby(grp_col)["GMV"].sum() / 1e7).round(2).reset_index()
        bd.rename(columns={"GMV":"value"}, inplace=True)
        y_label = "GMV (₹ Crores)"

    elif metric == "Orders":
        bd = data.groupby(grp_col)["order_id"].nunique().reset_index()
        bd.rename(columns={"order_id":"value"}, inplace=True)
        y_label = "Number of Orders"

    elif metric == "Repeat Rate":
        total  = data.groupby(grp_col)["customer_id"].nunique()
        repeat = (data[data["customer_type"]=="Repeat"]
                  .groupby(grp_col)["customer_id"].nunique())
        bd     = (repeat / total * 100).round(2).reset_index()
        bd.rename(columns={"customer_id":"value"}, inplace=True)
        y_label = "Repeat Rate %"

    elif metric == "Delayed Order Rate":
        bd = (data.groupby(grp_col)["delivery_status"]
              .apply(lambda x: round(x.isin(delay_statuses).sum() / max(len(x),1) * 100, 2))
              .reset_index(name="value"))
        y_label = "Delayed Order Rate %"

    return bd, y_label, grp_col

# ============================================================
# TITLE
# ============================================================
st.title("🛒 QuickKart Analytics Dashboard")

# Dynamic caption
selected_cities = ", ".join(sorted(city)) if len(city) < len(all_cities) else "All Cities"
selected_date   = f"{date_range[0]} → {date_range[1]}" if len(date_range) == 2 else "All Dates"

st.caption(f"📍 {selected_cities}  |  📅 {selected_date}  |  📆 {year_option}")
st.divider()

# ============================================================
# REQUIRED KPI STRIP
# ============================================================
total_gmv   = filtered["GMV"].sum() / 1e7
delay_rate  = round(filtered["delivery_status"].isin(delay_statuses).sum() /
                    max(len(filtered),1) * 100, 2)
repeat_rate = round(cm["repeat_customers"].sum() /
                    max(cm["total_customers"].sum(),1) * 100, 2)

k1, k2, k3 = st.columns(3)
k1.metric("💰 Total GMV",          f"₹{total_gmv:.1f} Cr")
k2.metric("🚚 Delayed Order Rate", f"{delay_rate}%")
k3.metric("🔄 Repeat Rate",        f"{repeat_rate}%")

st.divider()

# ============================================================
# TIME SERIES — dynamic metric
# ============================================================
st.subheader(f"📈 {metric} Trend — {year_option} | {selected_cities}")
ts, y_label = get_timeseries(filtered)
fig_ts = px.line(ts, x="order_monthname", y="value",
                 color="order_year" if year_option == "Compare (H2 Only)" else None,
                 markers=True,
                 labels={"value": y_label, "order_monthname":"Month"},
                 title=f"{metric} by Month")
st.plotly_chart(fig_ts, width="stretch", key="fig_ts")

# ============================================================
# BREAKDOWN CHART — city or carrier toggle
# ============================================================
st.subheader(f"📊 {metric} by {breakdown} — {selected_cities} | {selected_date}")
bd, y_label, grp_col = get_breakdown(filtered)
fig_bar = px.bar(bd.sort_values("value", ascending=False),
                 x=grp_col, y="value", color=grp_col,
                 labels={"value": y_label},
                 title=f"{metric} by {breakdown}")
st.plotly_chart(fig_bar, width="stretch", key="fig_bar")

st.divider()

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📦 GMV & Orders", "🚚 Delivery Performance", "👥 Customer Health"])

# ============================================================
# TAB 1 - GMV & ORDERS
# ============================================================
with tab1:

    total_orders  = filtered["order_id"].nunique()
    avg_order_val = filtered["GMV"].sum() / max(total_orders, 1)
    cancel_rate   = round(filtered[filtered["status"] == "Cancelled"]["order_id"].nunique() /
                          max(total_orders,1) * 100, 2)

    k1, k2, k3 = st.columns(3)
    k1.metric("Total Orders",      f"{total_orders:,}")
    k2.metric("Avg Order Value",   f"₹{avg_order_val:,.0f}")
    k3.metric("Cancellation Rate", f"{cancel_rate}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        city_gmv           = (filtered.groupby("city")["GMV"].sum().reset_index()
                              .sort_values("GMV", ascending=False))
        city_gmv["GMV_cr"] = (city_gmv["GMV"] / 1e7).round(2)
        fig2 = px.bar(city_gmv, x="city", y="GMV_cr", color="city",
                      labels={"GMV_cr":"GMV (₹ Crores)"}, title="GMV by City")
        st.plotly_chart(fig2, width="stretch", key="fig2")

    with col2:
        cat_gmv           = (filtered.groupby("category")["GMV"].sum().reset_index()
                             .sort_values("GMV", ascending=False))
        cat_gmv["GMV_cr"] = (cat_gmv["GMV"] / 1e7).round(2)
        fig3 = px.bar(cat_gmv, x="category", y="GMV_cr", color="category",
                      labels={"GMV_cr":"GMV (₹ Crores)"}, title="GMV by Category")
        st.plotly_chart(fig3, width="stretch", key="fig3")

    # Heatmap
    st.subheader(f"🗺️ GMV Heatmap — City vs Category ({year_option})")
    heatmap_data          = (filtered.groupby(["city","category"])["GMV"].sum().reset_index())
    heatmap_data["GMV_cr"] = (heatmap_data["GMV"] / 1e7).round(2)
    heatmap_pivot          = heatmap_data.pivot(index="city", columns="category",
                                                 values="GMV_cr").fillna(0)
    fig_heat = go.Figure(data=go.Heatmap(
        z             = heatmap_pivot.values,
        x             = heatmap_pivot.columns.tolist(),
        y             = heatmap_pivot.index.tolist(),
        colorscale    = "YlOrRd",
        text          = heatmap_pivot.values.round(2),
        texttemplate  = "%{text}",
        showscale     = True
    ))
    fig_heat.update_layout(
        title      = f"GMV by City & Category (₹ Crores) — {year_option} | {selected_cities}",
        xaxis_title = "Category",
        yaxis_title = "City"
    )
    st.plotly_chart(fig_heat, width="stretch", key="fig_heat")

    st.info("""
    💡 **Key Insights:**
    - Mumbai + Delhi + Bangalore = 47% of total GMV
    - Electronics drives ~80% of GMV — single point of failure
    - GMV is flat with no consistent growth momentum
    - Kochi GMV declining -15.87% YoY
    """)

# ============================================================
# TAB 2 - DELIVERY PERFORMANCE
# ============================================================
with tab2:

    avg_hours = round(filtered["diff_hours"].mean(), 2)
    avg_cost  = round(filtered["shipping_cost"].mean(), 2)
    ontime    = round(100 - delay_rate, 2)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("OnTime Rate",        f"{ontime}%")
    k2.metric("Delay Rate",         f"{delay_rate}%")
    k3.metric("Avg Delivery Hours", f"{avg_hours} hrs")
    k4.metric("Avg Shipping Cost",  f"₹{avg_cost}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        carrier_grp = (filtered.groupby("carrier")["delivery_status"]
                       .apply(lambda x: round(x.isin(delay_statuses).sum() / len(x) * 100, 2))
                       .reset_index().rename(columns={"delivery_status":"delay_pct"}))
        fig4 = px.bar(carrier_grp.sort_values("delay_pct", ascending=False),
                      x="carrier", y="delay_pct",
                      color="delay_pct", color_continuous_scale=["green","red"],
                      labels={"delay_pct":"Delay %"}, title="Delay % by Carrier")
        st.plotly_chart(fig4, width="stretch", key="fig4")

    with col2:
        city_grp = (filtered.groupby("city")["delivery_status"]
                    .apply(lambda x: round(x.isin(delay_statuses).sum() / len(x) * 100, 2))
                    .reset_index().rename(columns={"delivery_status":"delay_pct"}))
        fig5 = px.bar(city_grp.sort_values("delay_pct", ascending=False),
                      x="city", y="delay_pct",
                      color="delay_pct", color_continuous_scale=["green","red"],
                      labels={"delay_pct":"Delay %"}, title="Delay % by City")
        st.plotly_chart(fig5, width="stretch", key="fig5")

    st.subheader("⚠️ Top 10 Worst City + Carrier Combinations")
    combo = (filtered.groupby(["city","carrier"])["delivery_status"]
             .apply(lambda x: round(x.isin(delay_statuses).sum() / len(x) * 100, 2))
             .reset_index().rename(columns={"delivery_status":"delay_pct"}))
    combo["total"] = filtered.groupby(["city","carrier"]).size().values
    st.dataframe(combo.sort_values("delay_pct", ascending=False).head(10),
                 width="stretch")

    st.error("""
    🚨 **Critical Finding:**
    - Jaipur + Delhivery → 82% delayed
    - Lucknow + Delhivery → 82% delayed
    - InHouse is 4x better than any third party carrier
    """)

# ============================================================
# TAB 3 - CUSTOMER HEALTH
# ============================================================
with tab3:

    total_cust  = cm["total_customers"].sum()
    repeat_cust = cm["repeat_customers"].sum()
    new_cust    = cm["first_time_customers"].sum()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Customers",  f"{total_cust:,}")
    k2.metric("Repeat Customers", f"{repeat_cust:,}")
    k3.metric("New Customers",    f"{new_cust:,}")
    k4.metric("Repeat Rate",      f"{repeat_rate}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        cm_melt = cm.melt(id_vars=["order_year","order_month","order_monthname"],
                          value_vars=["repeat_purchase_rate","first_purchase_rate"],
                          var_name="type", value_name="rate")
        cm_melt["order_year"]      = cm_melt["order_year"].astype(str)
        cm_melt["order_monthname"] = pd.Categorical(cm_melt["order_monthname"],
                                                     categories=month_order, ordered=True)
        cm_melt["type"] = cm_melt["type"].map({"repeat_purchase_rate":"Repeat %",
                                                "first_purchase_rate": "First Time %"})
        fig6 = px.line(cm_melt, x="order_monthname", y="rate",
                       color="type",
                       line_dash="order_year" if year_option == "Compare (H2 Only)" else None,
                       markers=True,
                       labels={"rate":"%","order_monthname":"Month"},
                       title="Repeat vs First Time Customer %")
        st.plotly_chart(fig6, width="stretch", key="fig6")

    with col2:
        seg  = filtered.groupby("segment")["customer_id"].nunique().reset_index()
        fig7 = px.pie(seg, names="segment", values="customer_id",
                      title="Customer Segment Mix")
        st.plotly_chart(fig7, width="stretch", key="fig7")

    st.warning("""
    ⚠️ **Key Insights:**
    - Repeat rate 66% → 91% in 2025 — excellent retention
    - Only 167 new customers in Dec 2025 — acquisition dying
    - Same ~4,900 customers ordering every month
    - Urgent need for customer acquisition strategy
    """)