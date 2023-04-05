import logging
from typing import TypeVar
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.const import UnitOfTemperature, UnitOfPower, UnitOfEnergy

from .const import DOMAIN
from .entity import (
    BaseWattrouterSensorEntityDescription,
    IntegrationWattrouterEntity,
    SSRSensorEntityDescription,
)
from .coordinator import WattrouterUpdateCoordinator


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
                    unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
                    device_class=SensorDeviceClass.ENERGY,
                    state_class=SensorStateClass.TOTAL_INCREASING,
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
                    unit_of_measurement=UnitOfPower.KILO_WATT,
                    device_class=SensorDeviceClass.POWER,
                    state_class=SensorStateClass.MEASUREMENT,
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
        unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BaseWattrouterSensorEntityDescription(
        key="i2_power",
        name="I2 Power",
        state_getter=lambda s: s.measurement.i2_power,
        unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BaseWattrouterSensorEntityDescription(
        key="i3_power",
        name="I3 Power",
        state_getter=lambda s: s.measurement.i3_power,
        unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BaseWattrouterSensorEntityDescription(
        key="i_total_power",
        name="I Total Power",
        state_getter=lambda s: s.measurement.total_power,
        unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L1_reverse_energy",
        name="L1 Reverse Energy",
        state_getter=lambda s: s.day_stats.L1_reverse_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L2_reverse_energy",
        name="L2 Reverse Energy",
        state_getter=lambda s: s.day_stats.L2_reverse_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L3_reverse_energy",
        name="L3 Reverse Energy",
        state_getter=lambda s: s.day_stats.L3_reverse_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="total_reverse_energy",
        name="Total Reverse Energy",
        state_getter=lambda s: s.day_stats.total_reverse_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L1_forward_low_tariff_energy",
        name="L1 Forward Low Tariff Energy",
        state_getter=lambda s: s.day_stats.L1_forward_low_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L2_forward_low_tariff_energy",
        name="L2 Forward Low Tariff Energy",
        state_getter=lambda s: s.day_stats.L2_forward_low_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L3_forward_low_tariff_energy",
        name="L3 Forward Low Tariff Energy",
        state_getter=lambda s: s.day_stats.L3_forward_low_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="total_forward_low_tariff_energy",
        name="Total Forward Low Tariff Energy",
        state_getter=lambda s: s.day_stats.total_forward_low_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L1_forward_high_tariff_energy",
        name="L1 Forward High Tariff Energy",
        state_getter=lambda s: s.day_stats.L1_forward_high_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L2_forward_high_tariff_energy",
        name="L2 Forward High Tariff Energy",
        state_getter=lambda s: s.day_stats.L2_forward_high_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L3_forward_high_tariff_energy",
        name="L3 Forward High Tariff Energy",
        state_getter=lambda s: s.day_stats.L3_forward_high_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="total_forward_high_tariff_energy",
        name="Total Forward High Tariff Energy",
        state_getter=lambda s: s.day_stats.total_forward_high_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="total_forward_energy",
        name="Total Forward Energy",
        state_getter=lambda s: s.day_stats.total_forward_high_tariff_energy
        + s.day_stats.total_forward_low_tariff_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L1_production_energy",
        name="L1 Production Energy",
        state_getter=lambda s: s.day_stats.L1_production_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L2_production_energy",
        name="L2 Production Energy",
        state_getter=lambda s: s.day_stats.L2_production_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="L3_production_energy",
        name="L3 Production Energy",
        state_getter=lambda s: s.day_stats.L3_production_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="total_production_energy",
        name="Total Production Energy",
        state_getter=lambda s: s.day_stats.total_production_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="SSR1_energy",
        name="SSR1 Energy",
        state_getter=lambda s: s.day_stats.SSR1_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="SSR2_energy",
        name="SSR2 Energy",
        state_getter=lambda s: s.day_stats.SSR2_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="SSR3_energy",
        name="SSR3 Energy",
        state_getter=lambda s: s.day_stats.SSR3_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="SSR4_energy",
        name="SSR4 Energy",
        state_getter=lambda s: s.day_stats.SSR4_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="SSR5_energy",
        name="SSR5 Energy",
        state_getter=lambda s: s.day_stats.SSR5_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="SSR6_energy",
        name="SSR6 Energy",
        state_getter=lambda s: s.day_stats.SSR6_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="relay1_energy",
        name="relay1 Energy",
        state_getter=lambda s: s.day_stats.relay1_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="relay2_energy",
        name="relay2 Energy",
        state_getter=lambda s: s.day_stats.relay2_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="wsl1_energy",
        name="WSL1 Energy",
        state_getter=lambda s: s.day_stats.wsl1_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="wsl2_energy",
        name="WSL2 Energy",
        state_getter=lambda s: s.day_stats.wsl2_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="wsl3_energy",
        name="WSL3 Energy",
        state_getter=lambda s: s.day_stats.wsl3_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="wsl4_energy",
        name="WSL4 Energy",
        state_getter=lambda s: s.day_stats.wsl4_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="wsl5_energy",
        name="WSL5 Energy",
        state_getter=lambda s: s.day_stats.wsl5_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="wsl6_energy",
        name="WSL6 Energy",
        state_getter=lambda s: s.day_stats.wsl6_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="andi1_energy",
        name="ANDI1 Energy",
        state_getter=lambda s: s.day_stats.andi1_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="andi2_energy",
        name="ANDI2 Energy",
        state_getter=lambda s: s.day_stats.andi2_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="andi3_energy",
        name="ANDI3 Energy",
        state_getter=lambda s: s.day_stats.andi3_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="andi4_energy",
        name="ANDI4 Energy",
        state_getter=lambda s: s.day_stats.andi4_energy,
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BaseWattrouterSensorEntityDescription(
        key="temperature1",
        name="Temperature 1",
        state_getter=lambda s: s.measurement.temperature1,
        unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BaseWattrouterSensorEntityDescription(
        key="temperature2",
        name="Temperature 2",
        state_getter=lambda s: s.measurement.temperature2,
        unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BaseWattrouterSensorEntityDescription(
        key="temperature3",
        name="Temperature 3",
        state_getter=lambda s: s.measurement.temperature3,
        unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BaseWattrouterSensorEntityDescription(
        key="temperature4",
        name="Temperature 4",
        state_getter=lambda s: s.measurement.temperature4,
        unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
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
