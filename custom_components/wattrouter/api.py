"""Sample API Client."""
import logging
import asyncio
import socket
import aiohttp
import async_timeout
import time
from datetime import datetime
import xml.etree.ElementTree as ET
from array import array
from urllib.parse import urljoin

from .state import (
    MeasurementData,
    SSRState,
    SettingsData,
    TimePlanSettings,
    TimePlanState,
    DayStats,
)
from .settings import WattrouterSettings
from .xml_parser import XmlParser

TIMEOUT = 30

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class WattrouterApiClient:
    """API client for Wattrouter."""

    def __init__(
        self, session: aiohttp.ClientSession, settings: WattrouterSettings
    ) -> None:
        self._session = session
        self.settings = settings
        self.parser = XmlParser()

    async def get_configuration(self) -> SettingsData:
        """Get Wattrouter configuration."""
        response_text = await self.__fetch_data("/conf.xml")
        return self.parser.parse_setting(response_text)

    async def get_measurement(self) -> MeasurementData:
        """Get Wattrouter measurement data."""
        response_text = await self.__fetch_data("/meas.xml")
        return self.parser.parse_measurement(response_text)

    async def get_day_stats(self, minus_days: int = 0) -> DayStats:
        """Get Wattrouter measurement data."""
        response_text = await self.__fetch_data(f"/stat_day.xml?day={minus_days}")
        return self.parser.parse_day_stats(response_text)

    async def __fetch_data(self, endpoint: str) -> MeasurementData:
        url = urljoin(self.settings.url, endpoint)
        try:
            async with async_timeout.timeout(TIMEOUT):
                response = await self._session.get(
                    url, headers={"Accept": "application/xml"}
                )

                response_text = await response.text()

                if response.status != 200:
                    raise aiohttp.ClientConnectionError(
                        f"Wattrouter server responded with not success code: '{response.status}'. Response: '{response_text}'"
                    )

                return response_text

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
