import array
import time
import datetime

from attr import dataclass
from .state import (
    TimePlanSettings,
    TimePlanState,
)


@dataclass
class TimeScheduleArgs:
    name: str
    mode: int
    start_str: str
    end_str: str
    energy_limit: int
    power_percentage: int
    temperature_input: int
    temperature_threshold: int


def parse_time_schedule(args: TimeScheduleArgs) -> TimePlanSettings:
    return TimePlanSettings(
        name=args.name,
        state=TimePlanState.ENFORCE
        if has_flag(args.mode, TIME_MODE_ENFORCE)
        else TimePlanState.RESTRICT
        if has_flag(args.mode, TIME_MODE_RESTRICT)
        else TimePlanState.NOT_SET,
        start=parse_time(args.start_str),
        end=parse_time(args.end_str),
        power_percentage=args.power_percentage,
        temperature_input=args.temperature_input,
        temperature_threshold=args.temperature_threshold,
        temperature_control=has_flag(args.mode, TIME_COND_TEMP),
        temperature_is_lower=has_flag(args.mode, TIME_COND_TEMP_BELOW),
        iso_week_days=get_iso_week_days(args.mode),
        low_tariff=has_flag(args.mode, TIME_COND_LT),
        energy_limit_active=has_flag(args.mode, TIME_COND_ENERGY),
        energy_limit=args.energy_limit,
    )


def get_iso_week_days(mode: int) -> array:
    week_days = []
    for flag, iso_week_day in weeks_days_map.items():
        if has_flag(mode, flag):
            week_days.append(iso_week_day)

    return week_days


def has_flag(mask: int, flag: int):
    return (mask & flag) != 0


def parse_time(time_str: str) -> time:
    time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
    return time_obj


"""
The mode field is a 32 bit unsigned integer.
It is a bit mask.
If the field is used for the checkbox then the checkbox is checked when the corresponding bit is nonzero.
"""


# Time schedule mode:
TIME_MODE_MASK = 0x0000000F  # time schedule mode mask (reserved for up to 15 modes)
# Possible values:
TIME_MODE_UNUSED = 0x00000000  # time schedule is not used
TIME_MODE_RESTRICT = (
    0x00000001  # time schedule restricts output activity to given time interval
)

TIME_MODE_ENFORCE = (
    0x00000002  # time schedule forces output activity to given time interval
)

# Time schedule conditions:
TIME_COND_MASK = 0x000000F0  # time schedule condition mask
# Possible fields:

TIME_COND_LT = 0x00000010  # LT checkbox
TIME_COND_ENERGY = 0x00000020  # energy checkbox
TIME_COND_TEMP_BELOW = 0x00000040  # time schedule is active only if temperature is below TempLimit (for TIME_MODE_ENFORCE mode, Mx only)
TIME_COND_TEMP_ABOVE = 0x00000080  # time schedule is active only if temperature is above TempLimit (for TIME_MODE_ENFORCE mode, Mx only)
TIME_COND_TEMP = (
    TIME_COND_TEMP_BELOW | TIME_COND_TEMP_ABOVE
)  # temperature checkbox (Mx only)

# Time schedule weekdays:
TIME_WEEKDAY_MASK = 0x0000FF00  # time schedule weekday mask
# Possible fields:
TIME_WEEKDAY_ALL = 0x0000FF00  # time schedule is active on all days
TIME_WEEKDAY_MONDAY = 0x00000100  # time schedule is active on Monday
TIME_WEEKDAY_TUESDAY = 0x00000200  # time schedule is active on Tuesday
TIME_WEEKDAY_WEDNESDAY = 0x00000400  # time schedule is active on Wednesday
TIME_WEEKDAY_THURSDAY = 0x00000800  # time schedule is active on Thursday
TIME_WEEKDAY_FRIDAY = 0x00001000  # time schedule is active on Friday
TIME_WEEKDAY_SATURDAY = 0x00002000  # time schedule is active on Saturday
TIME_WEEKDAY_SUNDAY = 0x00004000  # time schedule is active on Sunday


# New for Mx version 2.2, M version 4.1 and ECO version 3.1:

# Start time condition:
TIME_EX_ON_MASK = 0x00030000  # time schedule start time mask
# Possible values:
TIME_EX_ON_TIME = 0x00000000  # time schedule starts at given time
TIME_EX_ON_SUNRISE = 0x00010000  # time schedule starts at sunrise
TIME_EX_ON_SUNSET = 0x00020000  # time schedule starts at sunset

# Stop time condition:
TIME_EX_OFF_MASK = 0x000C0000  # time schedule stop time mask
# Possible values:
TIME_EX_OFF_TIME = 0x00000000  # time schedule stops at given time
TIME_EX_OFF_SUNRISE = 0x00040000  # time schedule stops at sunrise
TIME_EX_OFF_SUNSET = 0x00080000  # time schedule stops at sunset

# Binary input condition:
TIME_EX_BIN_MASK = 0x00700000  # time schedule binary input mask
# Possible fields:
TIME_EX_BIN_INPUT = 0x00100000  # binary input checkbox
TIME_EX_BIN_INPUT_COND = 0x00200000  # binary input condition (0..on, 1..off)
TIME_EX_BIN_INPUT_RESERVED = 0x00400000  # reserved field

weeks_days_map = dict(
    [
        (TIME_WEEKDAY_MONDAY, 1),
        (TIME_WEEKDAY_TUESDAY, 2),
        (TIME_WEEKDAY_WEDNESDAY, 3),
        (TIME_WEEKDAY_THURSDAY, 4),
        (TIME_WEEKDAY_FRIDAY, 5),
        (TIME_WEEKDAY_SATURDAY, 6),
        (TIME_WEEKDAY_SUNDAY, 7),
    ]
)
