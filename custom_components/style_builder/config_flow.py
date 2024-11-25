from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class StyleBuilderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Style Builder."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Check if the integration is already configured
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            # Create the configuration entry
            return self.async_create_entry(
                title="Style Builder",
                data=user_input,
            )

        # Display the configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("theme_directory", default="themes"): str,
                }
            ),
        )
