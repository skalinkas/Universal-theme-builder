import os
import yaml
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.service import async_register_admin_service

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Style Builder integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Style Builder from a config entry."""
    hass.data[DOMAIN] = config_entry.data

    def read_theme(theme_name: str):
        """Read a theme file from the themes directory."""
        theme_path = hass.config.path(f"{config_entry.data['theme_directory']}/{theme_name}.yaml")
        if os.path.exists(theme_path):
            try:
                with open(theme_path, "r", encoding="utf-8") as file:
                    return yaml.safe_load(file)
            except yaml.YAMLError as error:
                hass.logger.error("Error reading theme file '%s': %s", theme_name, error)
                return None
        hass.logger.warning("Theme file '%s' does not exist", theme_name)
        return None

    def save_theme(theme_name: str, theme_data: dict):
        """Save a theme file to the themes directory."""
        theme_path = hass.config.path(f"{config_entry.data['theme_directory']}/{theme_name}.yaml")
        try:
            with open(theme_path, "w", encoding="utf-8") as file:
                yaml.dump(theme_data, file, default_flow_style=False, allow_unicode=True)
            hass.logger.info("Theme '%s' saved successfully", theme_name)
        except (OSError, yaml.YAMLError) as error:
            hass.logger.error("Error saving theme '%s': %s", theme_name, error)

    async_register_admin_service(
        hass,
        DOMAIN,
        "read_theme",
        lambda call: {"theme": read_theme(call.data["theme_name"])},
        schema=None,
    )

    async_register_admin_service(
        hass,
        DOMAIN,
        "save_theme",
        lambda call: save_theme(call.data["theme_name"], call.data["theme_data"]),
        schema=None,
    )

    hass.logger.info("Style Builder integration has been set up.")
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN in hass.data:
        del hass.data[DOMAIN]
    return True
