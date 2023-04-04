import asyncio
import logging
import threading
from datetime import datetime, timedelta
from typing import Optional
#import importlib.util, sys
import importlib
from time import time
import json

from pymodbus.client import ModbusTcpClient, ModbusSerialClient

_LOGGER = logging.getLogger(__name__)

class WattrouterModbusHub:
    """Wrapper class for pymodbus."""
    def __init__(
        self,
        hass,
        name,
        host,
        port,
        modbus_addr,
        serial_port,
        baudrate,
        scan_interval,
        plugin,
        config
    ):
        """Initialize the Modbus hub."""
        _LOGGER.debug(f"Wattrouter modbus hub creation baudrate: {baudrate}")
        self._hass = hass
        self._client = ModbusTcpClient(host=host, port=port, timeout=5)

        self._lock = threading.Lock()
        self._name = name
        self._modbus_addr = modbus_addr
        self._seriesnumber = 'still unknown'
        self.read_serial_port = serial_port
        self._baudrate = int(baudrate)
        self._scan_interval = timedelta(seconds=scan_interval)
        self._unsub_interval_method = None
        self._sensors = []
        self.inputBlocks = {}
        self.holdingBlocks = {}
        self.computedSensors = {}
        self.computedButtons = {}
        self.writeLocals = {} # key to description lookup dict for write_method = WRITE_DATA_LOCAL entities
        self.sleepzero = [] # sensors that will be set to zero in sleepmode
        self.sleepnone = [] # sensors that will be cleared in sleepmode
        self.writequeue = {} # queue requests when inverter is in sleep mode
        _LOGGER.debug(f"{self.name}: ready to call plugin to determine inverter type")
        self.plugin = plugin.plugin_instance #getPlugin(name).plugin_instance
        self.wakeupButton = None
        self._invertertype = self.plugin.determineInverterType(self, config)
        self._lastts = 0  # timestamp of last polling cycle
        self.localsUpdated = False
        self.localsLoaded = False
        _LOGGER.debug("solax modbushub done %s", self.__dict__)