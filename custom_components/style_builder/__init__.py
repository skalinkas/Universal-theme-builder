import os
import yaml
from homeassistant.helpers.service import async_register_admin_service

DOMAIN = "style_builder"

async def async_setup(hass, config):
    def read_theme(theme_name):
        theme_path = hass.config.path(f"themes/{theme_name}.yaml")
        if os.path.exists(theme_path):
            with open(theme_path, "r") as file:
                return yaml.safe_load(file)
        return None

    def save_theme(theme_name, theme_data):
        theme_path = hass.config.path(f"themes/{theme_name}.yaml")
        with open(theme_path, "w") as file:
            yaml.dump(theme_data, file, default_flow_style=False)

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
