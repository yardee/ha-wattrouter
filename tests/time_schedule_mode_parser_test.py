import array
import pytest
from custom_components.wattrouter.state import TimePlanState
from custom_components.wattrouter.time_schedule_mode_parser import parse_time_schedule


@pytest.mark.parametrize(
    "mode, expected_state",
    [
        (32641, TimePlanState.RESTRICT),
        (3970, TimePlanState.ENFORCE),
        (32576, TimePlanState.NOT_SET),
    ],
)
def test_parse_time_schedule_should_parse_state(
    mode: int, expected_state: TimePlanState
):
    time_settings = parse_time_schedule(mode, "12:00", "14:00", 0, 0, 0, 0)

    assert time_settings.state == expected_state


@pytest.mark.parametrize(
    "mode, temperature_threshold, expected_control, expected_is_lower",
    [
        (2882, 55, True, True),
        (11138, 40, True, False),
        (11009, 0, False, False),
    ],
)
def test_parse_time_schedule_should_parse_temperature_controls(
    mode: int,
    temperature_threshold: float,
    expected_control: bool,
    expected_is_lower: bool,
):
    time_settings = parse_time_schedule(
        mode, "12:00", "14:00", 0, 0, 0, temperature_threshold
    )

    assert time_settings.temperature_control == expected_control
    assert time_settings.temperature_is_lower == expected_is_lower
    assert time_settings.temperature_threshold == temperature_threshold


@pytest.mark.parametrize(
    "mode, expected_days",
    [
        (386, [1]),
        (18306, [1, 2, 3, 7]),
        (32642, [1, 2, 3, 4, 5, 6, 7]),
        (6274, [4, 5]),
        (130, []),
    ],
)
def test_parse_time_schedule_should_parse_days(
    mode: int,
    expected_days: array,
):
    time_settings = parse_time_schedule(mode, "12:00", "14:00", 0, 0, 0, 0)

    assert time_settings.iso_week_days == expected_days


@pytest.mark.parametrize(
    "mode, expected_low_tariff",
    [
        (7185, True),
        (7169, False),
    ],
)
def test_parse_time_schedule_should_parse_low_tariff(
    mode: int,
    expected_low_tariff: array,
):
    time_settings = parse_time_schedule(mode, "12:00", "14:00", 0, 0, 0, 0)

    assert time_settings.low_tariff == expected_low_tariff
