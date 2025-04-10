import streamlit as st
from tinydb import TinyDB
import pandas as pd
import plotly.graph_objs as go

from src.utils import db

# Load DB
data = db.all()

# Get companies
companies = [doc["name"] for doc in data]

# App layout
st.set_page_config(layout="centered")
st.title("📊 Company Shareholder Viewer")

st.markdown("""
Welcome to the **Company Shareholder Viewer**!

Explore shareholder ownership across time. Warnings are shown when:
- 📉 Shareholder count changes by over **20% or 50%**
- 🏢 Corporate shareholders make up over **10% or 25%**

> All data shown is sample-based and read from a TinyDB backend.
""")

# Company selection
selected_company = st.selectbox("Select a company", ["-- Select --"] + companies)

if selected_company != "-- Select --":
    company_data = next((doc for doc in data if doc["name"] == selected_company), None)

    if company_data:
        period_blocks = company_data.get("reporting_periods", [])
        period_map = {list(p.keys())[0]: p[list(p.keys())[0]] for p in period_blocks}
        sorted_periods = sorted(period_map.keys())

        # Calculate shareholder counts and corp ratio
        count_data = []
        for period in sorted_periods:
            shareholders = period_map[period]
            total = len(shareholders)
            corp_count = sum(1 for s in shareholders if s["entity_type"] == "corporate")
            corp_ratio = corp_count / total if total else 0
            count_data.append({
                "period": period,
                "total": total,
                "corporate_ratio": corp_ratio,
            })

        # Warnings — Shareholder count change
        if len(count_data) >= 2:
            prev, curr = count_data[-2], count_data[-1]
            delta = curr["total"] - prev["total"]
            pct_change = abs(delta) / prev["total"] * 100 if prev["total"] else 0

            if pct_change > 50:
                color, emoji, level = "red", "🚨", "High change (>50%)"
            elif pct_change > 20:
                color, emoji, level = "yellow", "⚠️", "Moderate change (>20%)"
            else:
                color, emoji, level = "green", "✅", "Stable (<20%)"

            with st.expander(f"{emoji} Shareholder Count Change Warning ({level})", expanded=True):
                st.markdown(f"""
                <div style="background-color:{color};padding:10px;border-radius:10px;">
                    <b>{selected_company}</b> had:
                    <ul>
                        <li><b>{prev['total']}</b> shareholders in <b>{prev['period']}</b></li>
                        <li><b>{curr['total']}</b> shareholders in <b>{curr['period']}</b></li>
                    </ul>
                    Change: <b>{delta:+}</b> shareholders ({pct_change:.2f}%)
                </div>
                """, unsafe_allow_html=True)

        # Warnings — Corporate ratio
        if len(count_data) >= 1:
            corp_ratio = count_data[-1]["corporate_ratio"]
            corp_pct = corp_ratio * 100

            if corp_pct > 25:
                color, emoji, level = "red", "🏢❌", "High corporate ownership (>25%)"
            elif corp_pct > 10:
                color, emoji, level = "yellow", "🏢⚠️", "Moderate corporate ownership (>10%)"
            else:
                color, emoji, level = "green", "🏢✅", "Low corporate ownership"

            with st.expander(f"{emoji} Corporate Shareholder Ratio Warning ({level})", expanded=True):
                st.markdown(f"""
                <div style="background-color:{color};padding:10px;border-radius:10px;">
                    In the most recent period <b>{count_data[-1]['period']}</b>, 
                    <b>{corp_pct:.2f}%</b> of shareholders were corporate entities.
                </div>
                """, unsafe_allow_html=True)
# 📈 Plotly graph
        st.subheader("📈 Shareholder Count Over Time")
        periods = [c["period"] for c in count_data]
        counts = [c["total"] for c in count_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=periods,
            y=counts,
            mode="lines+markers",
            name="Shareholders",
            line=dict(color="royalblue"),
            marker=dict(size=10)
        ))

        fig.update_layout(
            xaxis_title="Reporting Period",
            yaxis_title="Number of Shareholders",
            title=f"Shareholders Over Time – {selected_company}",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        
        # Period selection
        selected_period = st.selectbox("Select reporting period", ["-- Select --"] + sorted_periods)

        if selected_period != "-- Select --":
            shareholders = period_map.get(selected_period, [])
            if shareholders:
                df = pd.DataFrame(shareholders)
                df = df.rename(columns={
                    "shareholder_name": "Shareholder",
                    "entity_type": "Type",
                    "percent_of_ownership": "Ownership (%)"
                })
                st.subheader(f"Shareholders – {selected_company} ({selected_period})")
                st.dataframe(df.sort_values(by="Ownership (%)", ascending=False), use_container_width=True)
            else:
                st.info("No shareholder data found.")
