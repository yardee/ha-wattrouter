from datetime import datetime, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import WattrouterApiClient
from .state import WattrouterStateData
from .settings import WattrouterSettings
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=1)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class WattrouterUpdateCoordinator(DataUpdateCoordinator[WattrouterStateData]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: WattrouterApiClient,
        settings: WattrouterSettings,
    ) -> None:
        """Initialize."""
        self.api = client
        self.settings = settings
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> WattrouterStateData:
        """Update data via library."""
        try:
            state = WattrouterStateData(
                measurement=await self.api.get_measurement(),
                settings=await self.api.get_configuration(),
                day_stats=await self.api.get_day_stats(),
            )
            return state
        except Exception as exception:
            _LOGGER.error("Error fetching data: " + exception)
            raise UpdateFailed() from exception
