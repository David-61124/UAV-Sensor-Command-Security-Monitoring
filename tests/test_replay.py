from detectors.replay import detect_replay

def test_first_packet():

    current_packet = {
        "Packet_ID": 1,
        "Battery": 99.9,
        "Height": 1.2,
        "Speed": 0.8,
        "Pitch": 1.0,
        "Roll": 0.5,
        "Yaw": 20.0,
        "Flight_Time": 1
    }

    result = detect_replay(
        current_packet,
        None
    )

    assert result["detected"] is False

    print("Test 1 passed: First packet is not a replay.")

def test_normal_packet():

    previous_packet = {
        "Packet_ID": 1,
        "Battery": 99.9,
        "Height": 1.2,
        "Speed": 0.8,
        "Pitch": 1.0,
        "Roll": 0.5,
        "Yaw": 20.0,
        "Flight_Time": 1
    }

    current_packet = {
        "Packet_ID": 2,
        "Battery": 99.8,
        "Height": 1.5,
        "Speed": 1.0,
        "Pitch": 1.5,
        "Roll": 0.7,
        "Yaw": 25.0,
        "Flight_Time": 2
    }

    result = detect_replay(
        current_packet,
        previous_packet
    )

    assert result["detected"] is False

    print("Test 2 passed: Normal packet is not a replay.")

def test_replay_packet():

    previous_packet = {
        "Packet_ID": 10,
        "Battery": 95.5,
        "Height": 4.2,
        "Speed": 2.1,
        "Pitch": 2.0,
        "Roll": -1.0,
        "Yaw": 120.0,
        "Flight_Time": 10
    }

    replayed_packet = {
        "Packet_ID": 11,
        "Battery": 95.5,
        "Height": 4.2,
        "Speed": 2.1,
        "Pitch": 2.0,
        "Roll": -1.0,
        "Yaw": 120.0,
        "Flight_Time": 10
    }

    result = detect_replay(
        replayed_packet,
        previous_packet
    )

    assert result["detected"] is True
    assert result["threat"] == "Replay Attack"

    print("Test 3 passed: Replay attack detected.")

if __name__ == "__main__":

    test_first_packet()
    test_normal_packet()
    test_replay_packet()

    print("\nAll replay detection tests passed successfully! ✅")