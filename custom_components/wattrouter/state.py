from dataclasses import dataclass
from enum import Enum
import time
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
    """Wattrouter configuration."""

    time_plans: List[TimePlanSettings]


@dataclass
class DayStats:
    """Wattrouter day statistics."""

    L1_reverse_energy: float
    L2_reverse_energy: float
    L3_reverse_energy: float
    total_reverse_energy: float

    L1_forward_low_tariff_energy: float
    L2_forward_low_tariff_energy: float
    L3_forward_low_tariff_energy: float
    total_forward_low_tariff_energy: float

    L1_forward_high_tariff_energy: float
    L2_forward_high_tariff_energy: float
    L3_forward_high_tariff_energy: float
    total_forward_high_tariff_energy: float

    L1_production_energy: float
    L2_production_energy: float
    L3_production_energy: float
    total_production_energy: float

    SSR1_energy: float
    SSR2_energy: float
    SSR3_energy: float
    SSR4_energy: float
    SSR5_energy: float
    SSR6_energy: float
    rele1_energy: float
    rele2_energy: float
    wsl1_energy: float
    wsl2_energy: float
    wsl3_energy: float
    wsl4_energy: float
    wsl5_energy: float
    wsl6_energy: float
    andi1_energy: float
    andi2_energy: float
    andi3_energy: float
    andi4_energy: float


@dataclass
class WattrouterStateData:
    """Wattrouter state."""

    measurement: MeasurementData
    settings: SettingsData
    day_stats: DayStats
