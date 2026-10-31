
import random
import time
import csv
import os
from datetime import datetime

CSV_FILE = "datasets/normal_telemetry.csv"

BATTERY_START = 100
MAX_HEIGHT = 10.0
MAX_SPEED = 5.0

os.makedirs("datasets", exist_ok=True)

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Packet_ID",
            "Timestamp",
            "Battery",
            "Height",
            "Speed",
            "Pitch",
            "Roll",
            "Yaw",
            "Flight_Time",
            "Command",
            "Command_Source",
            "Command_Authorized"
        ])

battery = BATTERY_START
height = 0.0
speed = 0.0
pitch = 0.0
roll = 0.0
yaw = 0.0
flight_time = 0
packet_id = 0

while True:
    packet_id += 1

    height += random.uniform(-0.3, 0.5)
    height = max(0.0, min(height, MAX_HEIGHT))

    speed += random.uniform(-0.5, 0.5)
    speed = max(0.0, min(speed, MAX_SPEED))

    pitch += random.uniform(-2, 2)
    pitch = max(-15.0, min(pitch, 15.0))

    roll += random.uniform(-2, 2)
    roll = max(-15.0, min(roll, 15.0))

    yaw += random.uniform(-10, 10)
    yaw %= 360

    battery -= random.uniform(0.01, 0.05)
    battery = max(0.0, battery)

    flight_time += 1

    telemetry = {
        "Packet_ID": packet_id,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Battery": round(battery, 2),
        "Height": round(height, 2),
        "Speed": round(speed, 2),
        "Pitch": round(pitch, 2),
        "Roll": round(roll, 2),
        "Yaw": round(yaw, 2),
        "Flight_Time": flight_time,
        "Command": "NONE",
        "Command_Source": "NONE",
        "Command_Authorized": False
    }

    print("\n----- NORMAL UAV TELEMETRY -----")

    for key, value in telemetry.items():
        print(f"{key}: {value}")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(telemetry.values())

    time.sleep(1)
