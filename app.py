
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
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hawa_Mahal_2.jpg/1200px-Hawa_Mahal_2.jpg", use_column_width=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hawa_Mahal_2.jpg/1200px-Hawa_Mahal_2.jpg", use_column_width=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hawa_Mahal_2.jpg/1200px-Hawa_Mahal_2.jpg", use_column_width=True)


st.markdown(
    """
    ## Live Civic Health Dashboard

    **One glance should tell a resident what's happening
    in their neighborhood — and why it matters.**

    ⚠️ **Hackathon prototype:** the displayed civic measurements
    are synthetic demonstration data.
    """
)


# ---------------------------------------------------------
# SIMULATION TIME
# ---------------------------------------------------------

available_times = sorted(
    dashboard_df["time_window"].unique()
)

st.markdown("### 🕐 Simulation Control")

auto_play = st.toggle(
    "▶️ Live Simulation",
    value=False
)

if auto_play:

    refresh_count = st_autorefresh(
        interval=3000,
        key="citypulse_live"
    )

    selected_time = available_times[
        refresh_count % len(available_times)
    ]

    st.info(
        f"🔴 LIVE SIMULATION — "
        f"{pd.Timestamp(selected_time).strftime("%H:%M")}"
    )

else:

    selected_time = st.select_slider(
        "🕐 Simulation Time",
        options=available_times,
        value=available_times[-1]
    )


current_df = dashboard_df[
    dashboard_df["time_window"] == selected_time
].copy()


# ---------------------------------------------------------
# TOP-LEVEL KPIs
# ---------------------------------------------------------

average_pulse = current_df[
    "civic_pulse_score"
].mean()

active_events = (
    current_df["anomaly_count"] >= 2
).sum()

high_activity = (
    current_df["civic_pulse_score"] >= 70
).sum()

total_areas = current_df["area"].nunique()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Civic Pulse",
        f"{average_pulse:.0f}/100"
    )


with col2:

    st.metric(
        "Active Events",
        active_events
    )


with col3:

    st.metric(
        "High Activity Areas",
        high_activity
    )


with col4:

    st.metric(
        "Monitoring Areas",
        total_areas
    )


st.divider()


# ---------------------------------------------------------
# CITY MAP
# ---------------------------------------------------------

st.subheader("🗺️ Jaipur Civic Pulse")

st.caption(
    "Approximate locality monitoring points. "
    "Measurements are synthetic."
)


fig_map = px.scatter(
    current_df,

    x="longitude",
    y="latitude",

    size="civic_pulse_score",
    color="civic_pulse_score",

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
        "longitude": False,
        "latitude": False
    },

    size_max=35
)


fig_map.update_traces(
    textposition="top center"
)


fig_map.update_layout(
    height=600,

    xaxis_title="Longitude",
    yaxis_title="Latitude",

    xaxis=dict(
        scaleanchor="y",
        scaleratio=1
    ),

    margin={
        "l": 0,
        "r": 0,
        "t": 20,
        "b": 0
    }
)


st.plotly_chart(
    fig_map,
    use_container_width=True
)



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

st.subheader("📡 Data Feed Health")


feed_data = pd.DataFrame({

    "Feed": [
        "Weather",
        "Traffic",
        "Civic Incidents"
    ],

    "Status": [
        "🟢 Online",
        "🟢 Online",
        "🟢 Online"
    ],

    "Type": [
        "Synthetic",
        "Synthetic",
        "Synthetic"
    ]
})


st.dataframe(
    feed_data,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "CityPulse Jaipur | Civic Data Fusion Hackathon Prototype | "
    "Synthetic demonstration data"
)
