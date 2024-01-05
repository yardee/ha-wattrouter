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
        # modbus_addr,
        # serial_port,
        baudrate,
        scan_interval
    ):
        """Initialize the Modbus hub."""
        _LOGGER.debug(f"Wattrouter modbus hub creation baudrate: {baudrate}")
        self._hass = hass
        self._client = ModbusTcpClient(host=host, port=port, timeout=5)

        self._lock = threading.Lock()
        self._name = name
        # self._modbus_addr = modbus_addr
        self._seriesnumber = 'still unknown'
        # self.read_serial_port = serial_port
        self._baudrate = int(baudrate)
        self._scan_interval = timedelta(seconds=scan_interval)
        self.autorepeat_queue = {} # queue requests when inverter is in sleep mode

        self._unsub_interval_method = None
        self._sensors = []
        self.inputBlocks = {}
        self.holdingBlocks = {}
        self.computedSensors = {}
        self.computedButtons = {}


        self.wakeupButton = None
        self._lastts = 0  # timestamp of last polling cycle
        self.localsUpdated = False
        self.localsLoaded = False
        _LOGGER.debug("solax modbushub done %s", self.__dict__)

    def read_input_register(self, address: int): # -> int:
        """Read a single input register."""
        with self._lock:
            result = self._client.read_input_registers(address, 1)
            if result.isError():
                _LOGGER.error("Error reading input register %s: %s", address, result)
                return None

            _LOGGER.debug("Read input register %s: %s", address, result.registers)
            return result.registers[0]

    def write_input_register(self, address: int, value: int, autorepeat: bool = False): # -> int:
        """Read a single input register."""

        _LOGGER.debug(f"Write input register {address}: {value}. Auto repeat: {autorepeat}")
        with self._lock:
            if (autorepeat):
                self.autorepeat_queue[address] = value
                _LOGGER.debug(f"Write input register {address}: {value} added to autorepeat queue")
                return None

            result = self._client.write_register(address, value)
            if result.isError():
                _LOGGER.error("Error writing input register %s: %s", address, result)
                return None

    def write_all_autorepeated(self):
        _LOGGER.debug(f"write_all_autorepeated")
        for address, value in self.autorepeat_queue.items():
            self.write_input_register(address, value)

    def cancel_autorepeat(self, address: int):
        with self._lock:
            if address in self.autorepeat_queue:
                del self.autorepeat_queue[address]