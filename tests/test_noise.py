from detectors.noise_sensor import detect


# ==========================================
# Test 1: Normal telemetry
# ==========================================

previous_packet = {
    "Battery": 90,
    "Height": 5.0,
    "Speed": 3.0,
    "Pitch": 5.0,
    "Roll": 4.0,
    "Yaw": 100.0,
}

current_packet = {
    "Battery": 89.9,
    "Height": 5.4,
    "Speed": 3.2,
    "Pitch": 6.0,
    "Roll": 5.0,
    "Yaw": 105.0,
}

result = detect(
    current_packet,
    previous_packet
)

print("\n===== TEST 1: NORMAL =====")
print(result)


# ==========================================
# Test 2: Sudden sensor change
# ==========================================

previous_packet = {
    "Battery": 90,
    "Height": 5.0,
    "Speed": 3.0,
    "Pitch": 5.0,
    "Roll": 4.0,
    "Yaw": 100.0,
}

current_packet = {
    "Battery": 89.9,
    "Height": 8.5,
    "Speed": 3.2,
    "Pitch": 6.0,
    "Roll": 5.0,
    "Yaw": 105.0,
}

result = detect(
    current_packet,
    previous_packet
)

print("\n===== TEST 2: NOISE =====")
print(result)


# ==========================================
# Test 3: Yaw wrap-around
# ==========================================

previous_packet = {
    "Battery": 90,
    "Height": 5.0,
    "Speed": 3.0,
    "Pitch": 5.0,
    "Roll": 4.0,
    "Yaw": 359.0,
}

current_packet = {
    "Battery": 89.9,
    "Height": 5.2,
    "Speed": 3.1,
    "Pitch": 5.5,
    "Roll": 4.5,
    "Yaw": 1.0,
}

result = detect(
    current_packet,
    previous_packet
)

print("\n===== TEST 3: YAW WRAP-AROUND =====")
print(result)