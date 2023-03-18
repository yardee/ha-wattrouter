import logging
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from dataclasses import dataclass
from .const import DOMAIN, WATT, WATT_HOUR, KILO_WATT, KILO_WATT_HOUR
from .state import SSRState
from .entity import (
    BaseWattrouterSensorEntityDescription,
    IntegrationWattrouterEntity,
    SSRSensorEntityDescription,
)
from .coordinator import WattrouterUpdateCoordinator

from typing import Callable, TypeVar
from datetime import datetime
from homeassistant.components.sensor import (
    SensorDeviceClass,
)
from homeassistant.components.sensor import (
    SensorEntity,
)

T = TypeVar("T")


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Setup sensor platform."""
    coordinator: WattrouterUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for sensor in sensors:
        entities.append(
            BaseWattrouterSensorEntity(
                coordinator=coordinator, entity_description=sensor, config_entry=entry
            )
        )

    for i in [1, 2, 3, 4, 5, 6]:
        entities.append(
            SSRSensorEntity(
                coordinator=coordinator,
                entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_energy",
                    name=f"SSR{i} Energy",
                    state_getter=lambda s: s.energy,
                    unit_of_measurement=KILO_WATT_HOUR,
                    device_class=SensorDeviceClass.ENERGY,
                ),
                config_entry=entry,
            )
        )

        entities.append(
            SSRSensorEntity(
                coordinator=coordinator,
                entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_power",
                    name=f"SSR{i} Power",
                    state_getter=lambda s: s.power,
                    unit_of_measurement=KILO_WATT,
                    device_class=SensorDeviceClass.POWER,
                ),
                config_entry=entry,
            )
        )

    async_add_entities(entities, update_before_add=True)


sensors = [
    BaseWattrouterSensorEntityDescription(
        key="i1_power",
        name="I1 Power",
        state_getter=lambda s: s.measurement.i1_power,
        unit_of_measurement=WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    BaseWattrouterSensorEntityDescription(
        key="i2_power",
        name="I2 Power",
        state_getter=lambda s: s.measurement.i2_power,
        unit_of_measurement=WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    BaseWattrouterSensorEntityDescription(
        key="i3_power",
        name="I3 Power",
        state_getter=lambda s: s.measurement.i3_power,
        unit_of_measurement=WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    BaseWattrouterSensorEntityDescription(
        key="i_total_power",
        name="I Total Power",
        state_getter=lambda s: s.measurement.i1_power
        + s.measurement.i2_power
        + s.measurement.i3_power,
        unit_of_measurement=WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    BaseWattrouterSensorEntityDescription(
        key="i_total_power",
        name="I Total Power",
        state_getter=lambda s: s.measurement.i1_power
        + s.measurement.i2_power
        + s.measurement.i3_power,
        unit_of_measurement=WATT,
        device_class=SensorDeviceClass.POWER,
    ),
]


class SSRSensorEntity(IntegrationWattrouterEntity, SensorEntity):
    """Base class for all sensor entities."""

    def __init__(
        self,
        coordinator: WattrouterUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_description: SSRSensorEntityDescription,
    ):
        super().__init__(coordinator, config_entry, entity_description)
        self._attr_native_unit_of_measurement = entity_description.unit_of_measurement

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        ssr_data = getattr(
            coordinator.data.measurement, f"ssr{self.entity_description.ssr_index}"
        )

        if callable(self.entity_description.state_getter):
            return self.entity_description.state_getter(ssr_data)

        return None


class BaseWattrouterSensorEntity(IntegrationWattrouterEntity, SensorEntity):
    """Base class for all sensor entities."""

    def __init__(
        self,
        coordinator: WattrouterUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_description: BaseWattrouterSensorEntityDescription,
    ):
        super().__init__(coordinator, config_entry, entity_description)
        self._attr_native_unit_of_measurement = entity_description.unit_of_measurement

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        if callable(self.entity_description.state_getter):
            return self.entity_description.state_getter(coordinator.data)

        return None
