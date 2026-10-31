import pandas as pd
import csv
import os
import time

from detectors.replay import detect_replay
from detectors.false_telemetry import detect as detect_false_telemetry

CSV_FILE = "datasets/telemetry.csv"
LOG_FILE = "logs/detection_log.csv"

CHECK_INTERVAL = 1

os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG_FILE):

    with open(LOG_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Packet_ID",
            "Timestamp",
            "Threat_Type",
            "Severity",
            "Detected",
            "Reason"
        ])

print("\n===================================")
print("       UAV LIVE DETECTION ENGINE")
print("===================================")
print("\nWaiting for telemetry...\n")

processed_packets = 0
previous_packet = None

while True:

    try:

        if not os.path.exists(CSV_FILE):

            print("Waiting for telemetry file...")
            time.sleep(CHECK_INTERVAL)
            continue

        data = pd.read_csv(CSV_FILE)

        if data.empty:

            time.sleep(CHECK_INTERVAL)
            continue

        new_data = data.iloc[processed_packets:]

        for _, row in new_data.iterrows():

            current_packet = row.to_dict()

            packet_id = current_packet["Packet_ID"]
            timestamp = current_packet["Timestamp"]

            replay_result = detect_replay(
                current_packet,
                previous_packet
            )

            false_result = detect_false_telemetry(
                current_packet
            )

            threats = []
            reasons = []
            severities = []

            if replay_result["detected"]:

                threats.append(
                    replay_result["threat"]
                )

                reasons.append(
                    replay_result["reason"]
                )

                severities.append(
                    replay_result["severity"]
                )

            if false_result["detected"]:

                threats.append(
                    "False Telemetry"
                )

                reasons.append(
                    false_result["reason"]
                )

                severities.append(
                    false_result["severity"]
                )

            if threats:

                detected = True

                threat = " + ".join(threats)

                reason = " | ".join(reasons)

                severity_priority = {
                    "None": 0,
                    "Low": 1,
                    "Medium": 2,
                    "High": 3,
                    "Critical": 4
                }

                severity = max(
                    severities,
                    key=lambda x: severity_priority.get(
                        x,
                        0
                    )
                )

            else:

                detected = False

                threat = "Normal"

                severity = "None"

                reason = "No threats detected"

            if detected:

                print(
                    f"🚨 Packet {packet_id}: "
                    f"{threat} | "
                    f"Severity: {severity}"
                )

                print(
                    f"   Reason: {reason}"
                )

            else:

                print(
                    f"✅ Packet {packet_id}: Normal"
                )

            with open(LOG_FILE, "a", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    packet_id,
                    timestamp,
                    threat,
                    severity,
                    detected,
                    reason
                ])

            previous_packet = current_packet

            processed_packets += 1

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:

        print("\n\nDetection engine stopped.")
        break

    except Exception as error:

        print(f"\n⚠️ Error: {error}")

        time.sleep(CHECK_INTERVAL)