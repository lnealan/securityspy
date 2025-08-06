"""Constant definitions for SecSpy Wrapper."""

DEVICE_UPDATE_INTERVAL_SECONDS = 60
WEBSOCKET_CHECK_INTERVAL_SECONDS = 120

CAMERA_MESSAGES = [
    "ARM_A",
    "DISARM_A",
    "ARM_C",
    "DISARM_C",
    "ARM_M",
    "DISARM_M",
]
EVENT_MESSAGES = ["TRIGGER_M", "TRIGGER_A", "MOTION", "CLASSIFY", "MOTION_END", "ONLINE", "OFFLINE"]

RECORDING_TYPE_ACTION = "action"
RECORDING_TYPE_MOTION = "on_motion"
RECORDING_TYPE_CONTINUOUS = "continuous"

RECORDING_MODE_LIST = {
    RECORDING_TYPE_MOTION: "M",
    RECORDING_TYPE_CONTINUOUS: "C",
}

SERVER_ID = "server_id"
SERVER_NAME = "server_name"

# SecuritySpy trigger reason codes (from TRIGGER_M and TRIGGER_A events)
# These are bit flags that can be combined
TRIGGER_REASON_CODES = {
    1: "motion",           # Generic motion
    2: "audio",           # Audio trigger
    4: "applescript",     # AppleScript trigger
    8: "camera",          # Camera trigger
    16: "web",            # Web trigger
    32: "crosscamera",    # Cross-camera motion
    64: "manual",         # Manual trigger
    128: "human",         # AI detected human
    256: "vehicle",       # AI detected vehicle
    512: "animal",        # AI detected animal (SecuritySpy 5.5+)
}

def parse_trigger_reasons(reason_code):
    """Parse numeric reason code into list of reasons."""
    if not reason_code:
        return ["unknown"]
    
    try:
        code = int(reason_code)
    except (ValueError, TypeError):
        return ["unknown"]
    
    reasons = []
    for bit_value, reason_name in TRIGGER_REASON_CODES.items():
        if code & bit_value:
            reasons.append(reason_name)
    
    return reasons if reasons else ["unknown"]
