from datetime import datetime, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import WattrouterApiClient
from .state import WattrouterStateData
from .settings import WattrouterSettings
from .const import DOMAIN
from .wattrouter_modbus_hub import WattrouterModbusHub

SCAN_INTERVAL = timedelta(seconds=1)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class WattrouterUpdateCoordinator(DataUpdateCoordinator[WattrouterStateData]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: WattrouterApiClient,
        settings: WattrouterSettings,
        modbus_hub: WattrouterModbusHub,
    ) -> None:
        """Initialize."""
        self.api = client
        self.settings = settings
        self.platforms = []
        self.modbus_hub = modbus_hub

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> WattrouterStateData:
        """Update data via library."""
        try:
            self.modbus_hub.write_all_autorepeated()
        except Exception as exception:
            _LOGGER.error("Error auto repeat modbus data: %s", exception)

        try:
            state = WattrouterStateData(
                measurement=await self.api.get_measurement(),
                settings=await self.api.get_configuration(),
                day_stats=await self.api.get_day_stats(),
            )
            return state
        except Exception as exception:
            _LOGGER.error("Error fetching data: %s", exception)
            raise UpdateFailed() from exception


