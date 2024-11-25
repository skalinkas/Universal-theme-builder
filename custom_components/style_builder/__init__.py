import os
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import async_register_built_in_panel
from homeassistant.helpers.service import async_register_admin_service

import yaml
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Style Builder integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Style Builder from a config entry."""
    hass.data[DOMAIN] = config_entry.data

    # Serve frontend files
    hass.http.register_static_path(
        "/style-builder-frontend",
        hass.config.path("custom_components/style_builder/frontend"),
        cache_headers=False,
    )

    # Add sidebar panel
    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Style Builder",
        sidebar_icon="mdi:palette",
        frontend_url_path="style-builder",
        config={"url": "/style-builder-frontend/index.html"},
    )

    # Add services for reading and saving themes
    def read_theme(theme_name: str):
        theme_path = hass.config.path(f"{config_entry.data['theme_directory']}/{theme_name}.yaml")
        if os.path.exists(theme_path):
            with open(theme_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        return None

    def save_theme(theme_name: str, theme_data: dict):
        theme_path = hass.config.path(f"{config_entry.data['theme_directory']}/{theme_name}.yaml")
        with open(theme_path, "w", encoding="utf-8") as file:
            yaml.dump(theme_data, file, default_flow_style=False, allow_unicode=True)

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

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN in hass.data:
        del hass.data[DOMAIN]
    return True
