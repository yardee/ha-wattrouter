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

test_xml = "<meas><I1><P>1.01</P></I1><I2><P>20.00</P></I2><I3><P>4.01</P></I3><I4><P>0.00</P><E>0.29</E></I4><I5><P>0.00</P><E>0.29</E></I5><I6><P>0.00</P><E>0.29</E></I6><I7><P>0.00</P><E>0.29</E></I7><O1><A>0</A><P>1.00</P><E>5.37</E><HN>1</HN><HC>1</HC><HE>1</HE><HR>1</HR><HX>1</HX><T>1</T><TOT>1</TOT><TFT>1</TFT><TT>1</TT><EX>1</EX></O1><O2><A>0</A><P>0.70</P><E>3.77</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX></O2><O3><A>0</A><P>0.00</P><E>1.68</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX></O3><O4><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX></O4><O5><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX></O5><O6><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX></O6><O7><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX></O7><O8><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX></O8><O9><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O9><O10><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O10><O11><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O11><O12><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O12><O13><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O13><O14><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O14><O15><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O15><O16><A>0</A><P>0.00</P><E>0.00</E><HN>0</HN><HC>0</HC><HE>0</HE><HR>0</HR><HX>0</HX><T>0</T><TOT>0</TOT><TFT>0</TFT><TT>0</TT><EX>0</EX><Ty>0</Ty></O16><DQ1>14.0</DQ1><DQ2>55.0</DQ2><DQ3>0.0</DQ3><DQ4>0.0</DQ4><PPS>0.02</PPS><VAC>237</VAC><DaR>2023-03-16</DaR><TiR>22:56:42</TiR><CW>7038</CW><DC>11.9</DC><FW>2.0</FW><SN>46000DB0</SN><EL1>0</EL1><ETS>0</ETS><ELV>0</ELV><EDC>0</EDC><ESC>0</ESC><ESD>0</ESD><ILT>0</ILT><ICW>0</ICW><ITS>0</ITS><IDST>0</IDST><ISC>0</ISC><SRT>6:11</SRT><DW>3</DW><DIP><B1>192</B1><B2>168</B2><B3>0</B3><B4>200</B4></DIP><DMS><B1>255</B1><B2>255</B2><B3>255</B3><B4>0</B4></DMS><DDR><B1>192</B1><B2>168</B2><B3>0</B3><B4>1</B4></DDR><DDN><B1>192</B1><B2>168</B2><B3>0</B3><B4>1</B4></DDN><WV>6</WV></meas>"


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
        url = self.settings.url + endpoint
        try:
            async with async_timeout.timeout(TIMEOUT):
                response = await self._session.get(
                    url, headers={"Accept": "application/xml"}
                )

                response_text = await response.text()
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
