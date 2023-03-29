"""OteEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from .state import WattrouterStateData, SSRState
from homeassistant.components.sensor import (
    SensorEntityDescription,
)
from dataclasses import dataclass
from typing import Callable, TypeVar
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)


from .const import DOMAIN, ATTR_MANUFACTURER, VERSION, ENTITIES_PREFIX
from .coordinator import WattrouterUpdateCoordinator

T = TypeVar("T")


@dataclass
class BaseWattrouterSensorEntityDescription(SensorEntityDescription):
    """base class for ote sensor declarations"""

    state_getter: Callable[[WattrouterStateData], T] = None


class IntegrationWattrouterEntity(CoordinatorEntity):
    """A class for entities using DataUpdateCoordinator."""

    entity_description: BaseWattrouterSensorEntityDescription

    def __init__(
        self,
        coordinator: WattrouterUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_description: BaseWattrouterSensorEntityDescription,
    ):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_description = entity_description
        self._attr_unit_of_measurement = entity_description.unit_of_measurement

    @property
    def key(self):
        """Return a unique key to use for this entity."""
        return f"{ENTITIES_PREFIX}_{self.entity_description.key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{ENTITIES_PREFIX} {self.entity_description.name}"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{ENTITIES_PREFIX}_{self.entity_description.key}"

    @property
    def device_info(self):
        return DeviceInfo(
            name="Wattrouter",
            identifiers={(DOMAIN)},
            manufacturer=ATTR_MANUFACTURER,
            model=VERSION,
        )

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {
            "id": self.key,
            "integration": DOMAIN,
        }
        return attributes


@dataclass
class SSRSensorEntityDescription(SensorEntityDescription):
    """Base class for all sensor entities."""

    state_getter: Callable[[SSRState], T] = None
    ssr_index: int = None
