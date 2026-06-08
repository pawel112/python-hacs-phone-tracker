"""Binary sensor for Phone Tracker."""
from __future__ import annotations

import asyncio
from datetime import timedelta, datetime, timezone

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from . import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    config = {**entry.data, **entry.options}
    async_add_entities([PhoneConnectedSensor(hass, entry, config)], update_before_add=True)


class PhoneConnectedSensor(BinarySensorEntity):
    """Binary sensor: phone presence via WiFi ping."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, config: dict) -> None:
        self.hass = hass
        self._entry = entry
        self._ip = config["ip_address"]
        self._device_name = config.get("device_name", "Telefon")
        self._last_seen: datetime | None = None
        self._attr_is_on = None
        self._attr_unique_id = f"phone_tracker_{self._ip.replace('.', '_')}"
        self._attr_name = ""

    @property
    def icon(self) -> str:
        return "mdi:wifi" if self._attr_is_on else "mdi:wifi-off"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._ip)},
            name=self._device_name,
            manufacturer="Telefon",
            model=f"IP: {self._ip}",
            entry_type=None,
        )

    async def async_added_to_hass(self) -> None:
        await self._do_ping()
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._scheduled_ping,
                timedelta(seconds=30),
            )
        )

    @callback
    def _scheduled_ping(self, now=None) -> None:
        self.hass.async_create_task(self._do_ping())

    async def _do_ping(self) -> None:
        try:
            proc = await asyncio.create_subprocess_exec(
                "ping", "-c", "2", "-W", "1", self._ip,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()
            reachable = proc.returncode == 0
        except Exception:
            reachable = False

        if reachable:
            self._last_seen = datetime.now(tz=timezone.utc)
            self._attr_is_on = True
        else:
            self._attr_is_on = False

        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict:
        attrs = {"ip_address": self._ip}
        if self._last_seen:
            attrs["ostatnio_widziany"] = self._last_seen.isoformat()
        return attrs
