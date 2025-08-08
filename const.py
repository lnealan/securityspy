"""Constant definitions for SecuritySpy Integration."""
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_FILENAME,
)
from .pysecspy.const import (
    RECORDING_TYPE_ACTION,
    RECORDING_TYPE_MOTION,
    RECORDING_TYPE_CONTINUOUS,
)

DOMAIN = "securityspy"
UNIQUE_ID = "unique_id"

DEFAULT_PORT = 8000
DEFAULT_MIN_SCORE = 50
DEFAULT_MOTION_COOLDOWN = 0
DEFAULT_ATTRIBUTION = "Powered by SecuritySpy Server"
DEFAULT_BRAND = "Ben Software"
MIN_SECSPY_VERSION = "5.3.4"

CONF_MODE = "mode"
CONF_ENABLED = "enabled"
CONF_DISABLE_RTSP = "disable_rtsp"
CONF_MIN_SCORE = "min_event_score"
CONF_MOTION_COOLDOWN = "motion_cooldown"
CONFIG_OPTIONS = [
    CONF_DISABLE_RTSP,
    CONF_MIN_SCORE,
    CONF_MOTION_COOLDOWN,
]

ATTR_BRAND = "brand"
ATTR_EVENT_LENGTH = "event_length"
ATTR_EVENT_OBJECT = "event_object"
ATTR_EVENT_SCORE_ANIMAL = "event_score_animal"
ATTR_EVENT_SCORE_HUMAN = "event_score_human"
ATTR_EVENT_SCORE_VEHICLE = "event_score_vehicle"
ATTR_TRIGGER_REASONS = "trigger_reasons"
ATTR_TRIGGER_TYPE = "trigger_type"
ATTR_PRESET_ID = "preset_id"
ATTR_PTZ_CAPABILITIES = "ptz_capabilities"

DEVICE_CLASS_DETECTION = "securityspy__detection"

DEVICE_TYPE_CAMERA = "camera"
DEVICE_TYPE_DOORBELL = "doorbell"
DEVICE_TYPE_LOCAL = "local"
DEVICE_TYPE_MOTION = "motion"
DEVICE_TYPE_NETWORK = "network"

DEVICES_WITH_CAMERA = (
    DEVICE_TYPE_CAMERA,
    DEVICE_TYPE_DOORBELL,
    DEVICE_TYPE_NETWORK,
    DEVICE_TYPE_LOCAL,
)

VALID_MODES = [
    RECORDING_TYPE_MOTION,
    RECORDING_TYPE_CONTINUOUS,
    RECORDING_TYPE_ACTION,
]
SERVICE_DOWNLOAD_LATEST_MOTION_RECORDING = "download_latest_motion_recording"
SERVICE_ENABLE_SCHEDULE_PRESET = "enable_schedule_preset"
SERVICE_SET_ARM_MODE = "set_arm_mode"
DOWNLOAD_LATEST_MOTION_RECORDING_SCHEMA = { vol.Required(ATTR_ENTITY_ID): cv.entity_ids, vol.Required(CONF_FILENAME): cv.string,}
ENABLE_SCHEDULE_PRESET_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_PRESET_ID): cv.string,
    }
)
SET_ARM_MODE_SCHEMA = { vol.Required(ATTR_ENTITY_ID): cv.entity_ids, vol.Required(CONF_MODE): vol.In(VALID_MODES), vol.Required(CONF_ENABLED): cv.boolean,}
SECURITYSPY_PLATFORMS = [
    "camera",
    "binary_sensor",
    "sensor",
    "switch",
    "button",
]

