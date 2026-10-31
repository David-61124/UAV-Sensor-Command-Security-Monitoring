import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(
    page_title="Secure UAV Monitoring System",
    page_icon="🚁",
    layout="wide"
)

TELEMETRY_FILE = "datasets/telemetry.csv"
LOG_FILE = "logs/detection_log.csv"

REFRESH_INTERVAL = 0.1
CONNECTION_TIMEOUT = 3

st.title("🚁 Secure UAV Monitoring System")

st.caption(
    "Real-Time UAV Telemetry & Cybersecurity Monitoring"
)

st.divider()

if not os.path.exists(TELEMETRY_FILE):

    st.error("❌ Telemetry file not found.")
    st.stop()

telemetry = pd.read_csv(
    TELEMETRY_FILE
)

if telemetry.empty:

    st.warning(
        "⏳ Waiting for telemetry..."
    )

    st.stop()

latest = telemetry.iloc[-1]

packet_id = latest["Packet_ID"]
timestamp = latest["Timestamp"]

battery = latest["Battery"]
height = latest["Height"]
speed = latest["Speed"]

pitch = latest["Pitch"]
roll = latest["Roll"]
yaw = latest["Yaw"]

flight_time = latest["Flight_Time"]

file_modified_time = os.path.getmtime(
    TELEMETRY_FILE
)

current_time = time.time()

time_since_update = (
    current_time - file_modified_time
)

if time_since_update <= CONNECTION_TIMEOUT:

    connection_status = "🟢 LIVE"
    connection_message = "Simulator Connected"

else:

    connection_status = "🔴 DISCONNECTED"
    connection_message = "No telemetry received"

st.subheader("📡 Connection Status")

col1, col2 = st.columns(2)

with col1:

    if connection_status == "🟢 LIVE":

        st.success(
            connection_status
        )

    else:

        st.error(
            connection_status
        )

with col2:

    st.info(
        connection_message
    )

st.divider()

st.subheader("🚁 UAV Status")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "🔋 Battery",
        f"{battery:.2f}%"
    )

with col2:

    st.metric(
        "📏 Altitude",
        f"{height:.2f} m"
    )

with col3:

    st.metric(
        "🚀 Speed",
        f"{speed:.2f} m/s"
    )

with col4:

    st.metric(
        "📦 Packet",
        int(packet_id)
    )

with col5:

    st.metric(
        "⏱ Flight Time",
        f"{int(flight_time)} s"
    )

st.caption(
    f"Last Telemetry Update: {timestamp}"
)

st.divider()

detection_log = pd.DataFrame()

latest_attack = None

if os.path.exists(LOG_FILE):

    detection_log = pd.read_csv(
        LOG_FILE
    )

    if not detection_log.empty:

        detected_rows = detection_log[
            detection_log["Detected"]
            .astype(str)
            .str.lower()
            .isin(
                ["true", "1", "yes"]
            )
        ]

        if not detected_rows.empty:

            latest_attack = (
                detected_rows.iloc[-1]
            )

current_packet_detected = False

current_packet_result = None

if not detection_log.empty:

    current_packet_rows = detection_log[
        detection_log["Packet_ID"] == packet_id
    ]

    if not current_packet_rows.empty:

        current_packet_result = (
            current_packet_rows.iloc[-1]
        )

        current_packet_detected = (
            str(
                current_packet_result[
                    "Detected"
                ]
            ).lower()
            in ["true", "1", "yes"]
        )

st.subheader(
    "🛡️ Current System Status"
)

if current_packet_detected:

    st.error(
        "🔴 UNDER ATTACK"
    )

    if current_packet_result is not None:

        current_threat = (
            current_packet_result[
                "Threat_Type"
            ]
        )

        current_severity = (
            current_packet_result[
                "Severity"
            ]
        )

        st.warning(
            f"Threat: {current_threat} | "
            f"Severity: {current_severity}"
        )

else:

    st.success(
        "🟢 SAFE"
    )

st.caption(
    f"Status based on latest packet: "
    f"{int(packet_id)}"
)

st.divider()

st.subheader(
    "🚨 Last Security Event"
)

if latest_attack is not None:

    threat_type = (
        latest_attack["Threat_Type"]
    )

    severity = (
        latest_attack["Severity"]
    )

    attack_packet = (
        latest_attack["Packet_ID"]
    )

    reason = (
        latest_attack["Reason"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Threat",
            str(threat_type)
        )

    with col2:

        st.metric(
            "Severity",
            str(severity)
        )

    with col3:

        st.metric(
            "Packet",
            int(attack_packet)
        )

    st.warning(
        f"Reason: {reason}"
    )

else:

    st.info(
        "No security threats detected yet."
    )

st.divider()

st.subheader(
    "🧭 Drone Orientation"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Pitch",
        f"{pitch:.2f}°"
    )

with col2:

    st.metric(
        "Roll",
        f"{roll:.2f}°"
    )

with col3:

    st.metric(
        "Yaw",
        f"{yaw:.2f}°"
    )

st.divider()

st.subheader(
    "📊 Live Telemetry"
)

recent = telemetry.tail(30)

col1, col2 = st.columns(2)

with col1:

    st.write("Altitude")

    st.line_chart(
        recent.set_index(
            "Timestamp"
        )["Height"]
    )

with col2:

    st.write("Speed")

    st.line_chart(
        recent.set_index(
            "Timestamp"
        )["Speed"]
    )

col1, col2 = st.columns(2)

with col1:

    st.write("Pitch")

    st.line_chart(
        recent.set_index(
            "Timestamp"
        )["Pitch"]
    )

with col2:

    st.write("Roll")

    st.line_chart(
        recent.set_index(
            "Timestamp"
        )["Roll"]
    )

st.divider()

st.subheader(
    "📋 Detection History"
)

if not detection_log.empty:

    attack_history = detection_log[
        detection_log["Detected"]
        .astype(str)
        .str.lower()
        .isin(
            ["true", "1", "yes"]
        )
    ]

    if not attack_history.empty:

        st.dataframe(
            attack_history.tail(20),
            use_container_width=True
        )

    else:

        st.info(
            "No security attacks detected."
        )

else:

    st.info(
        "Detection log not available."
    )

st.divider()

st.subheader(
    "📡 Latest Telemetry"
)

st.dataframe(
    telemetry.tail(10),
    use_container_width=True
)

time.sleep(
    REFRESH_INTERVAL
)

st.rerun()