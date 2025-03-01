from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_NAME
import logging

_LOGGER = logging.getLogger(__name__)

class CarPlateRecognitionConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Car Plate Recognition."""
    VERSION = 1

    def __init__(self):
        """Initialize."""
        self.host = None
        self.code_project_host = None
        self.cameras = []

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input:
            self.host = user_input[CONF_HOST]
            self.code_project_host = user_input['code_project_host']
            self.cameras = user_input['cameras']
            return self.async_create_entry(
                title="Car Plate Recognition",
                data={
                    CONF_HOST: self.host,
                    'code_project_host': self.code_project_host,
                    'cameras': self.cameras
                }
            )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required('code_project_host'): str,
                vol.Required('cameras'): list,
            })
        )
