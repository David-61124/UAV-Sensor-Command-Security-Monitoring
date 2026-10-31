from detectors.abnormal_flight_behaviour import detect


# ==========================================
# TEST 1: Normal Flight
# ==========================================

normal_packet = {
    "Speed": 4.0,
    "Height": 6.0,
    "Pitch": 5.0,
    "Roll": 4.0,
}

result = detect(normal_packet)

print("\n===== TEST 1: NORMAL FLIGHT =====")
print(result)


# ==========================================
# TEST 2: High Speed + Extreme Pitch
# ==========================================

abnormal_packet = {
    "Speed": 10.0,
    "Height": 8.0,
    "Pitch": 50.0,
    "Roll": 5.0,
}

result = detect(abnormal_packet)

print("\n===== TEST 2: HIGH SPEED + EXTREME PITCH =====")
print(result)


# ==========================================
# TEST 3: High Speed + Extreme Roll
# ==========================================

abnormal_packet = {
    "Speed": 10.0,
    "Height": 8.0,
    "Pitch": 5.0,
    "Roll": 50.0,
}

result = detect(abnormal_packet)

print("\n===== TEST 3: HIGH SPEED + EXTREME ROLL =====")
print(result)


# ==========================================
# TEST 4: Aggressive Flight Attitude
# ==========================================

abnormal_packet = {
    "Speed": 5.0,
    "Height": 8.0,
    "Pitch": 40.0,
    "Roll": 40.0,
}

result = detect(abnormal_packet)

print("\n===== TEST 4: AGGRESSIVE ATTITUDE =====")
print(result)


# ==========================================
# TEST 5: Normal Values but Abnormal Pattern
# ==========================================

abnormal_packet = {
    "Speed": 9.0,
    "Height": 22.0,
    "Pitch": 5.0,
    "Roll": 5.0,
}

result = detect(abnormal_packet)

print("\n===== TEST 5: HIGH SPEED + HIGH ALTITUDE =====")
print(result)