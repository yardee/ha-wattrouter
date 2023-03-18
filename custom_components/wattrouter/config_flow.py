from collections.abc import Mapping
from typing import Any, cast

import voluptuous as vol
from homeassistant.const import (
    CONF_NAME,
)
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_URL,
    DOMAIN,
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL, default=""): str,
        vol.Required(CONF_USERNAME, default="admin"): str,
        vol.Required(CONF_PASSWORD, default="1234"): str,
    }
)

CONFIG_FLOW: dict[str, SchemaFlowFormStep] = {
    "user": SchemaFlowFormStep(CONFIG_SCHEMA),
}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    # Handle a config or options flow for Utility Meter.

    config_flow = CONFIG_FLOW
    options_flow = CONFIG_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        # Return config entry title
        return cast(str, options[CONF_URL]) if CONF_URL in options else ""
