from dataclasses import dataclass
from enum import Enum
import time
from array import array
from typing import List


@dataclass
class SSRState:
    """Class for keeping track of date prices."""

    power: float
    energy: float
    regulated: bool
    combiwatt_active: bool
    forced_active: bool
    limit_active: bool
    test_active: bool


@dataclass
class MeasurementData:
    """Class for keeping track of date prices."""

    i1_power: float
    i2_power: float
    i3_power: float

    ssr1: SSRState
    ssr2: SSRState
    ssr3: SSRState
    ssr4: SSRState
    ssr5: SSRState
    ssr6: SSRState
    rele1: SSRState
    rele2: SSRState

    temperature1: float
    temperature2: float
    temperature3: float
    temperature4: float


# class syntax
class TimePlanState(Enum):
    NOT_SET = 0
    RESTRICT = 1
    ENFORCE = 2


@dataclass
class TimePlanSettings:
    """Time plan setting in Wattrouter."""

    name: str
    state: TimePlanState
    start: time
    end: time
    power_percentage: int
    energy_limit: float
    energy_limit_active: bool
    temperature_input: int
    temperature_threshold: float
    temperature_control: bool
    temperature_is_lower: bool
    iso_week_days: List[int]
    low_tariff: bool


@dataclass
class SettingsData:
    """Class for keeping track of date prices."""

    time_plans: List[TimePlanSettings]


"""
<conf>
<TS11><!-- 1. časový plán výstupu 1 (SSR1)-->
 <M>2</M><!-- režim (0=nepoužito, 1=omezen, 2=vynucen) + příznaky NT,
Energie, Teplota a dny v týdnu, detaily poskytneme na vyžádání-->
 <N>15:00</N><!-- čas Od-->
 <F>19:00</F><!-- čas Do-->
 <P>100</P><!-- Výkon v procentech, jen proporcionální výstupy-->
..<Li>8.60</Li><!-- limit energie-->
..<TI>0</TI><!-- přiřazený teplotní vstup (0=D/Q1 až 7=ANDI4)-->
..<TT>60.0</TT><!-- teplotní limit-->
</TS11>
<!-- analogicky pro zbývající výstupy a časové plány (celkem 54 časových
plánů)-->
<DQN1>teplota bojler</DQN1><!-- jmenovka teplotního čidla D/Q1 -->
<!-- analogicky pro zbývající digitální teplotní čidla-->
<RM>0</RM><!-- režim regulace (0=každá fáze samostatně, 1=součet fází)-->
<PO>-0.05</PO><!-- výkonový ofset v kW-->
<PWM>0</PWM><!-- frekvence PWM (0=10kHz až 5=200Hz -->
<VM>1</VM><!-- kalibrace napětí - násobitel-->
<VD>1</VD><!-- kalibrace napětí - dělitel-->
<URC>0</URC><!--optimalizovat spotřebu interních relé (0=ne, 1=ano)-->
<IP>...</IP><!-- IP adresa regulátoru-->
<MSK>...</MSK><!-- maska podsítě regulátoru-->
<DR>...</DR><!-- výchozí brána-->
WATTrouter Mx - uživatelská příručka
www.solarcontrols.cz
Návod k instalaci a nastavení přístroje Stránka 64 z 79
<MAC>...</MAC><!-- fyzická adresa regulátoru (MAC)-->
<HTTP>80</HTTP><!-- port HTTP-->
<UDP>80</UDP><!-- port UDP-->
<CWD>7200.0</CWD><!-- zpoždění CombiWATT v s-->
<CWL>0.02</CWL><!-- limit výroby pro CombiWATT v kW-->
<CWR>0</CWR><!-- reset čítačů výroby (0=východ Slunce až 1=fixní čas)-->
<CWT>6:00</CWT><!-- fixní čas resetu čítačů výroby-->
<LA>50</LA><!-- zeměpisná šířka ve °-->
<LO>15</LO><!-- zeměpisná délka ve °-->
<STC>0</STC><!-- synchronizace data podle klienta (0=neaktivní, 1=aktivní)-
->
<STS>0</STS><!-- pravidelná synchronizace data podle časového serveru
(0=neaktivní, 1=aktivní)-->
<DST>1</DST><!-- používat letní čas (0=neaktivní, 1=aktivní)-->
<TZ>13</TZ><!-- časové pásmo (0=GMT-12 až 25=GMT+14)-->
<TSIP>...</TSIP><!-- IP adresa časového serveru-->
<DT>0</DT><!-- typ digitálních čidel (0=DS18S20, 1=DS18B20)-->
<DFT>1</DFT><!-- výchozí záložka (0=Nastavení vstupů až 4=Statistiky)-->
</conf>
"""


@dataclass
class WattrouterStateData:
    """Class for keeping track of ote states."""

    measurement: MeasurementData
    settings: SettingsData
