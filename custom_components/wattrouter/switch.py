from homeassistant.config_entries import ConfigEntry
import logging

from homeassistant.components.switch import (
    SwitchEntity
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .entity import (
    BaseWattrouterSensorEntityDescription,
    IntegrationWattrouterEntity,
    SSRSensorEntityDescription,
)
from .coordinator import WattrouterUpdateCoordinator

from typing import (
    Any,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

async def async_setup_entry(
    hass, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Setup switch platform."""
    coordinator: WattrouterUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("Setup switch platform.")
    if coordinator.data is None:
        _LOGGER.error("Input booleans not added. Data not available.")
        return

    entities = []
    i = 1
    entities.append(
        WattrouterModbusSwitch(
            coordinator=coordinator, entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_regulated",
                    name=f"SSR{i} Regulated",
                    state_getter=lambda s: s.regulated,
                ), config_entry=entry
        )
    )

    async_add_devices(entities)

class WattrouterModbusSwitch(IntegrationWattrouterEntity, SwitchEntity):
    """Base class for all input booleans modbus entities."""

    @property
    def is_on(self):
        """Return true if the input boolean is on."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        return coordinator.data.measurement.ssr1.limit_active

    @property
    def turn_on(self, **kwargs: Any):
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        coordinator.modbus_hub.write_input_register(8, 1000, autorepeat=True)

    @property
    def turn_off(self, **kwargs: Any):
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        coordinator.modbus_hub.write_input_register(8, 0)
        coordinator.modbus_hub.cancel_autorepeat(8)