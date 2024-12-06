from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.http.static import StaticPathConfig
from homeassistant.components.frontend import async_register_built_in_panel, async_remove_panel
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Style Builder integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Style Builder from a config entry."""
    hass.data[DOMAIN] = config_entry.data

    # Serve frontend files
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            url_path="/style-builder-frontend",
            local_path=hass.config.path("custom_components/style_builder/frontend"),
            cache=False,
        )
    ])

    # Register the panel
    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Style Builder",
        sidebar_icon="mdi:palette",
        frontend_url_path="style-builder",
        config={"url": "/style-builder-frontend/index.html"},
        require_admin=True,  # Optional: restrict access to admin users
    )

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await async_remove_panel(hass, "style-builder")

    if DOMAIN in hass.data:
        del hass.data[DOMAIN]

    return True
