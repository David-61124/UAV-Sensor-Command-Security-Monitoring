from detectors.unauthorized_command_injection import detect


# ==========================================
# TEST 1: No command
# ==========================================

packet = {
    "Command": "NONE",
    "Command_Source": "",
    "Command_Authorized": False,
}

result = detect(packet)

print("\n===== TEST 1: NO COMMAND =====")
print(result)


# ==========================================
# TEST 2: Legitimate TAKEOFF
# ==========================================

packet = {
    "Command": "TAKEOFF",
    "Command_Source": "GCS",
    "Command_Authorized": True,
}

result = detect(packet)

print("\n===== TEST 2: AUTHORIZED TAKEOFF =====")
print(result)


# ==========================================
# TEST 3: Valid command but unauthorized
# ==========================================

packet = {
    "Command": "TAKEOFF",
    "Command_Source": "UNKNOWN",
    "Command_Authorized": False,
}

result = detect(packet)

print("\n===== TEST 3: UNAUTHORIZED TAKEOFF =====")
print(result)


# ==========================================
# TEST 4: Unknown command
# ==========================================

packet = {
    "Command": "DISABLE_MOTORS",
    "Command_Source": "UNKNOWN",
    "Command_Authorized": False,
}

result = detect(packet)

print("\n===== TEST 4: UNKNOWN COMMAND =====")
print(result)


# ==========================================
# TEST 5: Authorized MOVE
# ==========================================

packet = {
    "Command": "MOVE",
    "Command_Source": "GCS",
    "Command_Authorized": True,
}

result = detect(packet)

print("\n===== TEST 5: AUTHORIZED MOVE =====")
print(result)