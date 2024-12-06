from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.http.static import StaticPathConfig
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Style Builder integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up the Style Builder integration from a config entry."""
    hass.data[DOMAIN] = config_entry.data

    # Serve frontend files
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            url_path="/style-builder-frontend",
            local_path=hass.config.path("custom_components/style_builder/frontend"),
            cache=False,
        )
    ])

    # Add any additional setup logic here

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN in hass.data:
        del hass.data[DOMAIN]
    return True
