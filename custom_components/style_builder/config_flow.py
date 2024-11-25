from homeassistant import config_entries
from homeassistant.core import callback
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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Define the options flow handler."""
        return StyleBuilderOptionsFlow(config_entry)


class StyleBuilderOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Style Builder."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Save the updated options
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        # Display the options form
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "theme_directory",
                        default=self.config_entry.options.get(
                            "theme_directory", self.config_entry.data.get("theme_directory", "themes")
                        ),
                    ): str,
                }
            ),
        )
