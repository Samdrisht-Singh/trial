
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="CityPulse Jaipur",
    page_icon="🏙️",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "citypulse_jaipur_dashboard.csv"
    )

    df["time_window"] = pd.to_datetime(
        df["time_window"]
    )

    return df


dashboard_df = load_data()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🏙️ CityPulse Jaipur")

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hawa_Mahal_2.jpg/1200px-Hawa_Mahal_2.jpg",
    use_container_width=True
)

st.markdown(
    """
    ### Your real-time window into Jaipur's urban health.

    CityPulse fuses real-time weather, traffic, and civic incident data
    to detect unusual activity and identify relationships between urban signals.
    This dashboard provides a snapshot of civic well-being across different areas.

    ⚠️ **Note:** This is a hackathon prototype using synthetic data for demonstration purposes.
    """
)
st.divider()


# ---------------------------------------------------------
# CITY MAP
# ---------------------------------------------------------

st.subheader("🗺️ Jaipur Civic Pulse Map", help="Visualizes the Civic Pulse Score across Jaipur. Higher scores (larger, brighter markers) indicate greater civic activity or disruption.")

st.caption(
    "Live geographic view of Jaipur civic conditions. "
    "Marker size and intensity represent the Civic Pulse score. "
    "Monitoring points are approximate and data is synthetic." # Updated caption
)


fig_map = px.scatter_map(
    current_df,

    lat="latitude",
    lon="longitude",

    size="civic_pulse_score",
    color="civic_pulse_score",
    color_continuous_scale=px.colors.sequential.Plasma, # Changed color scale

    text="area",
    hover_name="area",

    hover_data={
        "civic_pulse_score": ":.1f",
        "pulse_status": True,
        "event_status": True,
        "anomaly_count": True,
        "rainfall_mm": ":.1f",
        "delay_minutes": ":.1f",
        "congestion_percent": ":.1f",
        "incident_count": True,
        "latitude": False,
        "longitude": False
    },

    zoom=11,
    center={
        "lat": 26.895,
        "lon": 75.800
    },

    height=600,
    size_max=40,

    map_style="open-street-map"
)

fig_map.update_traces(
    textposition="top center",
    marker=dict(line=dict(width=1, color='DarkSlateGrey')) # Added marker border
)

fig_map.update_layout(
    margin={"l": 0, "r": 0, "t": 10, "b": 0},
    coloraxis_colorbar=dict(
        title="Civic Pulse",
        thicknessmode="pixels", thickness=15,
        lenmode="pixels", len=200,
        yanchor="top", y=1,
        xanchor="left", x=0
    ) # Added color bar title
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)


st.divider()



# ---------------------------------------------------------
# CIVIC INSIGHTS
# ---------------------------------------------------------

st.subheader("🧠 Civic Insights", help="Identified correlations between different civic signals in each area.")

# Load correlation data
correlation_df = pd.read_csv("citypulse_correlations.csv")

def interpret_correlation(value):
    if pd.isna(value):
        return "Insufficient data"
    absolute_value = abs(value)
    if absolute_value >= 0.7:
        return "Strong association"
    elif absolute_value >= 0.4:
        return "Moderate association"
    elif absolute_value >= 0.2:
        return "Weak association"
    else:
        return "Little association"

correlation_df["rainfall_traffic_relation"] = correlation_df["rainfall_traffic_corr"].apply(interpret_correlation)
correlation_df["rainfall_incident_relation"] = correlation_df["rainfall_incidents_corr"].apply(interpret_correlation)
correlation_df["traffic_incident_relation"] = correlation_df["traffic_incidents_corr"].apply(interpret_correlation)

st.dataframe(
    correlation_df[
        [
            "area",
            "rainfall_traffic_relation",
            "rainfall_incident_relation",
            "traffic_incident_relation"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------------------------------------------------
# ALERT CENTER
# ---------------------------------------------------------

st.subheader("🚨 Alert Center", help="Shows areas with significant multi-signal anomalies.")

current_alerts = current_df[
    current_df["anomaly_count"] >= 2
].copy()

current_alerts = current_alerts.sort_values(
    "civic_pulse_score",
    ascending=False
)


if len(current_alerts) == 0:

    st.success(
        "No multi-signal alerts detected "
        "at the current simulation time."
    )

else:

    st.caption(
        "Alerts are generated when multiple civic signals "
        "deviate from their local baseline."
    )

    for _, alert in current_alerts.head(5).iterrows():

        signals = []

        if alert["weather_score"] >= 40:
            signals.append("🌧️ Weather")

        if alert["traffic_score"] >= 40:
            signals.append("🚗 Traffic")

        if alert["incident_score"] >= 40:
            signals.append("🚨 Civic incidents")


        signal_text = " · ".join(signals)

        with st.container(border=True):

            st.markdown(
                f"### 🚨 {alert['area']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Status",
                    alert["event_status"]
                )

            with col2:

                st.metric(
                    "Civic Pulse",
                    f"{alert['civic_pulse_score']:.0f}"
                )

            with col3:

                st.metric(
                    "Evidence",
                    alert["evidence_level"]
                )

            st.markdown(
                f"**Contributing Signals:** {signal_text}"
            )

            st.write(
                alert["summary"]
            )

            st.caption(
                "Correlation indicates temporal association, "
                "not confirmed causation."
            )


st.divider()

# ---------------------------------------------------------
# ACTIVE EVENTS
# ---------------------------------------------------------

st.subheader("🚨 Active Civic Events")


active_df = current_df[
    current_df["anomaly_count"] >= 2
].copy()


active_df = active_df.sort_values(
    "civic_pulse_score",
    ascending=False
)


if len(active_df) == 0:

    st.success(
        "No multi-signal civic events detected "
        "at this simulation time."
    )

else:

    for _, event in active_df.iterrows():

        with st.container(border=True):

            st.markdown(
                f"### 🚨 {event['area']}"
            )

            st.write(
                f"**Status:** {event['event_status']}"
            )

            st.write(
                f"**Civic Pulse:** "
                f"{event['civic_pulse_score']:.0f}/100"
            )

            st.write(
                event["summary"]
            )

            st.caption(
                f"Evidence level: "
                f"{event['evidence_level']}"
            )


st.divider()


# ---------------------------------------------------------
# AREA EXPLORER
# ---------------------------------------------------------

st.subheader("🔎 Live Area Explorer")

# Current areas at the selected simulation time
available_current_areas = current_df["area"].tolist()

# Find areas with active multi-signal events
active_current = current_df[
    current_df["anomaly_count"] >= 2
].copy()

if len(active_current) > 0:

    # Automatically focus on the strongest current event
    active_current = active_current.sort_values(
        "civic_pulse_score",
        ascending=False
    )

    recommended_area = active_current.iloc[0]["area"]

else:

    # If there is no active event, use the highest Civic Pulse area
    recommended_area = current_df.sort_values(
        "civic_pulse_score",
        ascending=False
    ).iloc[0]["area"]


# Allow manual exploration, but make the live event the default
selected_area = st.selectbox(
    "Select a Jaipur area",
    sorted(dashboard_df["area"].unique()),
    index=sorted(
        dashboard_df["area"].unique()
    ).index(recommended_area)
)


# Historical data for selected area
area_data = dashboard_df[
    dashboard_df["area"] == selected_area
].copy()


# Current data for selected simulation time
current_area_data = area_data[
    area_data["time_window"] == selected_time
]


if len(current_area_data) == 0:

    st.warning(
        "No data is available for this area "
        "at the selected simulation time."
    )

else:

    current_area = current_area_data.iloc[0]


    # -----------------------------------------------------
    # AREA METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Civic Pulse",
            f"{current_area['civic_pulse_score']:.0f}"
        )


    with col2:

        st.metric(
            "Rainfall",
            f"{current_area['rainfall_mm']:.1f} mm"
        )


    with col3:

        st.metric(
            "Traffic Delay",
            f"{current_area['delay_minutes']:.1f} min"
        )


    with col4:

        st.metric(
            "Civic Incidents",
            int(current_area["incident_count"])
        )


    # -----------------------------------------------------
    # WHY AM I SEEING THIS?
    # -----------------------------------------------------

    st.markdown(
        "### 🧠 Why am I seeing this?"
    )

    st.info(
        current_area["pulse_explanation"]
    )


    # -----------------------------------------------------
    # HISTORICAL CIVIC PULSE
    # -----------------------------------------------------

    st.subheader(
        f"📈 Civic Pulse History — {selected_area}"
    )

    fig_history = px.line(
        area_data,
        x="time_window",
        y="civic_pulse_score",
        markers=True,
        labels={
            "time_window": "Time",
            "civic_pulse_score": "Civic Pulse"
        }
    )

    # Highlight the current simulation time
    fig_history.add_vline(
        x=selected_time,
        line_dash="dash",
        annotation_text="Current"
    )

    fig_history.add_hline(
        y=40,
        line_dash="dash",
        annotation_text="Elevated"
    )

    fig_history.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="High"
    )

    fig_history.update_yaxes(
        range=[0, 100]
    )

    st.plotly_chart(
        fig_history,
        use_container_width=True
    )


    # -----------------------------------------------------
    # SIGNAL BREAKDOWN
    # -----------------------------------------------------

    st.subheader(
        f"📊 Signal Breakdown — {selected_area}"
    )

    signal_data = area_data[
        [
            "time_window",
            "weather_score",
            "traffic_score",
            "incident_score"
        ]
    ].melt(
        id_vars="time_window",
        value_vars=[
            "weather_score",
            "traffic_score",
            "incident_score"
        ],
        var_name="Signal",
        value_name="Intensity"
    )

    fig_signal = px.line(
        signal_data,
        x="time_window",
        y="Intensity",
        color="Signal",
        markers=True
    )

    # Highlight current simulation time
    fig_signal.add_vline(
        x=selected_time,
        line_dash="dash",
        annotation_text="Current"
    )

    fig_signal.update_yaxes(
        range=[0, 100]
    )

    st.plotly_chart(
        fig_signal,
        use_container_width=True
    )


st.divider()


# ---------------------------------------------------------
# FEED HEALTH
# ---------------------------------------------------------

st.subheader("📡 Data Feed Health", help="Status and freshness of incoming data feeds.")

feed_health = pd.read_csv("citypulse_feed_health.csv")

# Load freshness data (assuming this is generated and saved as well)
# For now, let's re-calculate or assume a freshness_df exists from elsewhere if not saved.
# As this is a Streamlit app, it's better to load the required dataframes directly.

# Let's mock freshness data for demonstration if it's not explicitly passed or saved
try:
    freshness_df = pd.read_csv("citypulse_freshness.csv")
    freshness_df["Latest Observation"] = pd.to_datetime(freshness_df["Latest Observation"])
except FileNotFoundError:
    # Fallback if freshness_df is not saved as a separate CSV
    latest_weather = dashboard_df["time_window"].max() # Simplified, ideally from original weather_live
    latest_traffic = dashboard_df["time_window"].max() # Simplified, ideally from original traffic_live
    latest_incidents = dashboard_df["time_window"].max() # Simplified, ideally from original incidents_live

    freshness_df = pd.DataFrame({
        "Feed": [
            "Weather",
            "Traffic",
            "Civic Incidents"
        ],
        "Latest Observation": [
            latest_weather,
            latest_traffic,
            latest_incidents
        ]
    })

merged_health = pd.merge(feed_health, freshness_df, on="Feed", how="left")

merged_health["Status"] = merged_health["Status"].apply(lambda s: "🟢 " + s if s == "Online" else "🔴 " + s)
merged_health["Freshness"] = merged_health["Latest Observation"].dt.strftime('%Y-%m-%d %H:%M')

st.dataframe(
    merged_health[["Feed", "Status", "Freshness"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "CityPulse Jaipur © 2026 | Urban Health Dashboard Prototype | "
    "Data generated for demonstration purposes only. Not representative of actual conditions." # Updated footer
)
