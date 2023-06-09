import logging
import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_URL,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from .coordinator import WattrouterUpdateCoordinator, WattrouterSettings
from .api import WattrouterApiClient

"""OTE Rate sensor integration."""
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]
_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up platform from a ConfigEntry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info("Wattrouter setup started")

    settings = WattrouterSettings(
        password=config_entry.options[CONF_PASSWORD],
        username=config_entry.options[CONF_USERNAME],
        url=config_entry.options[CONF_URL],
    )

    session = async_get_clientsession(hass)
    client = WattrouterApiClient(session, settings)
    coordinator = WattrouterUpdateCoordinator(hass, client=client, settings=settings)
    await coordinator.async_refresh()

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    # Forward the setup to the sensor platform.
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
