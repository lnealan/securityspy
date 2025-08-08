"""Base class for securityspy data."""
from __future__ import annotations

import logging
import time

from homeassistant.core import callback
from .const import CONF_MOTION_COOLDOWN

from .pysecspy.errors import RequestError

_LOGGER = logging.getLogger(__name__)


class SecuritySpyData:
    """Coordinate updates."""

    def __init__(self, hass, secspyserver):
        """Initialize an subscriber."""
        super().__init__()
        self._hass = hass
        self._secspyserver = secspyserver
        self.data = {}
        self._subscriptions = {}
        self._unsub_websocket = None
        self.last_update_success = False
        self._last_motion_times = {}  # Track last motion time for each camera

    async def async_setup(self):
        """Subscribe and do the refresh."""
        self._unsub_websocket = self._secspyserver.subscribe_websocket(
            self._async_process_updates
        )
        await self.async_refresh()

    async def async_stop(self):
        """Stop processing data."""
        if self._unsub_websocket:
            self._unsub_websocket()
            self._unsub_websocket = None
        await self._secspyserver.async_disconnect_ws()

    async def async_refresh(self, *_, force_camera_update=False):
        """Update the data."""
        try:
            self._async_process_updates(
                await self._secspyserver.update(force_camera_update=force_camera_update)
            )
            self.last_update_success = True
        except RequestError:
            if self.last_update_success:
                _LOGGER.exception("Error while updating")
            self.last_update_success = False

    @callback
    def _async_process_updates(self, updates):
        """Process update from the securityspy data."""
        if isinstance(updates, dict):
            for device_id, data in updates.items():
                # Work on a copy to avoid mutating the server's processed_data
                event = dict(data)
                if "event_on" in event:
                    _LOGGER.debug(
                        "Processing motion event for %s: event_on=%s, end=%s",
                        device_id,
                        event.get("event_on"),
                        event.get("end"),
                    )

                # Apply motion cooldown if configured (only for motion start events, not end events)
                if event.get("event_on") and not event.get("end"):
                    # Get cooldown setting from config entry options
                    config_entries = self._hass.config_entries.async_entries("securityspy")
                    if config_entries:
                        cooldown = config_entries[0].options.get(CONF_MOTION_COOLDOWN, 0)
                        if cooldown > 0:
                            current_time = time.time()
                            last_motion = self._last_motion_times.get(device_id, 0)
                            remaining = cooldown - (current_time - last_motion)
                            if remaining > 0:
                                # Suppress notifying subscribers for this update
                                _LOGGER.debug(
                                    "Suppressing motion for %s due to cooldown (%.1fs remaining)",
                                    device_id,
                                    remaining,
                                )
                                continue
                            # Motion allowed, update last motion time
                            self._last_motion_times[device_id] = current_time

                # Store the data
                self.data[device_id] = event
                self.async_signal_device_id_update(device_id)
        else:
            _LOGGER.debug("TYPES OF UPDATES: %s", type(updates))

    @callback
    def async_subscribe_device_id(self, device_id, update_callback):
        """Add an callback subscriber."""
        self._subscriptions.setdefault(device_id, []).append(update_callback)

        def _unsubscribe():
            self.async_unsubscribe_device_id(device_id, update_callback)

        return _unsubscribe

    @callback
    def async_unsubscribe_device_id(self, device_id, update_callback):
        """Remove a callback subscriber."""
        self._subscriptions[device_id].remove(update_callback)
        if not self._subscriptions[device_id]:
            del self._subscriptions[device_id]

    @callback
    def async_signal_device_id_update(self, device_id):
        """Call the callbacks for a device_id."""
        if not self._subscriptions.get(device_id):
            return

        for update_callback in self._subscriptions[device_id]:
            update_callback()
