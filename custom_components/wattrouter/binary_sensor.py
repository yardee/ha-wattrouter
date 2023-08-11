"""Binary sensors platform for ote rates."""
from homeassistant.config_entries import ConfigEntry
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .entity import (
    BaseWattrouterSensorEntityDescription,
    IntegrationWattrouterEntity,
    SSRSensorEntityDescription,
)
from .coordinator import WattrouterUpdateCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)

async def async_setup_entry(
    hass, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Setup binary_sensor platform."""
    coordinator: WattrouterUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    if coordinator.data is None:
        _LOGGER.error("Binary sensors not added. Data not available.")
        return

    entities = []

    for sensor in sensors:
        entities.append(
            BaseOteBinarySensorEntity(
                coordinator=coordinator, entity_description=sensor, config_entry=entry
            )
        )

    for i in [1, 2, 3, 4, 5, 6]:
        entities.append(
            SSRBinarySensorEntity(
                coordinator=coordinator,
                entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_combiwatt",
                    name=f"SSR{i} CombiWatt",
                    state_getter=lambda s: s.combiwatt_active,
                ),
                config_entry=entry,
            )
        )

        entities.append(
            SSRBinarySensorEntity(
                coordinator=coordinator,
                entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_forced",
                    name=f"SSR{i} Forced",
                    state_getter=lambda s: s.forced_active,
                ),
                config_entry=entry,
            )
        )

        entities.append(
            SSRBinarySensorEntity(
                coordinator=coordinator,
                entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_limit",
                    name=f"SSR{i} Limit",
                    state_getter=lambda s: s.limit_active,
                ),
                config_entry=entry,
            )
        )

        entities.append(
            SSRBinarySensorEntity(
                coordinator=coordinator,
                entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_regulated",
                    name=f"SSR{i} Regulated",
                    state_getter=lambda s: s.regulated,
                ),
                config_entry=entry,
            )
        )

        entities.append(
            SSRBinarySensorEntity(
                coordinator=coordinator,
                entity_description=SSRSensorEntityDescription(
                    ssr_index=i,
                    key=f"ssr{i}_test",
                    name=f"SSR{i} Test",
                    state_getter=lambda s: s.test_active,
                ),
                config_entry=entry,
            )
        )

    async_add_devices(entities)


sensors = [
    BaseWattrouterSensorEntityDescription(
        key="low_tariff_active",
        name="Low tariff active",
        state_getter=lambda s: s.measurement.low_tariff_active,
    ),
    BaseWattrouterSensorEntityDescription(
        key="test_active",
        name="Test active",
        state_getter=lambda s: s.measurement.test_active,
    ),
    BaseWattrouterSensorEntityDescription(
        key="combiwatt_active",
        name="CombiWATT active",
        state_getter=lambda s: s.measurement.combiwatt_active,
    ),
]


class SSRBinarySensorEntity(IntegrationWattrouterEntity, BinarySensorEntity):
    """Base class for all sensor entities."""

    def __init__(
        self,
        coordinator: WattrouterUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_description: SSRSensorEntityDescription,
    ):
        super().__init__(coordinator, config_entry, entity_description)

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        ssr_data = getattr(
            coordinator.data.measurement, f"ssr{self.entity_description.ssr_index}"
        )
        if hasattr(self.entity_description, "state_getter"):
            return self.entity_description.state_getter(ssr_data)

        return None


class BaseOteBinarySensorEntity(IntegrationWattrouterEntity, BinarySensorEntity):
    """Base class for all binary sensor entities."""

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        if hasattr(self.entity_description, "state_getter"):
            return self.entity_description.state_getter(coordinator.data)

        return None

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        if hasattr(self.entity_description, "state_getter"):
            return self.entity_description.state_getter(coordinator.data)

        return None


class BaseOteBinarySensorEntity(IntegrationWattrouterEntity, BinarySensorEntity):
    """Base class for all binary sensor entities."""

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        if hasattr(self.entity_description, "state_getter"):
            return self.entity_description.state_getter(coordinator.data)

        return None

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        coordinator: WattrouterUpdateCoordinator = self.coordinator
        if hasattr(self.entity_description, "state_getter"):
            return self.entity_description.state_getter(coordinator.data)

        return None
