"""Config flow for Phone Tracker."""
from __future__ import annotations

import re
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from . import DOMAIN

IP_REGEX = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


def _validate_ip(ip: str) -> str:
    ip = ip.strip()
    if not IP_REGEX.match(ip):
        raise vol.Invalid("invalid_ip")
    return ip


class PhoneTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                user_input["ip_address"] = _validate_ip(user_input["ip_address"])
                await self.async_set_unique_id(user_input["ip_address"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input.get("device_name", "Telefon"),
                    data=user_input,
                )
            except vol.Invalid:
                errors["ip_address"] = "invalid_ip"

        schema = vol.Schema({
            vol.Required("device_name", default="Telefon"): str,
            vol.Required("ip_address"): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PhoneTrackerOptionsFlow(config_entry)


class PhoneTrackerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self._entry = entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                user_input["ip_address"] = _validate_ip(user_input["ip_address"])
                return self.async_create_entry(title="", data=user_input)
            except vol.Invalid:
                errors["ip_address"] = "invalid_ip"

        current = {**self._entry.data, **self._entry.options}
        schema = vol.Schema({
            vol.Required("device_name", default=current.get("device_name", "Telefon")): str,
            vol.Required("ip_address", default=current.get("ip_address", "")): str,
        })
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
