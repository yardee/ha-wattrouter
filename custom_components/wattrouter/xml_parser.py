import xml.etree.ElementTree as ET
from array import array

from custom_components.wattrouter.time_schedule_mode_parser import (
    TimeScheduleArgs,
    parse_time_schedule,
)

from .state import (
    MeasurementData,
    SSRState,
    SettingsData,
    TimePlanSettings,
    TimePlanState,
    DayStats,
)


class XmlParser:
    def parse_measurement(self, xml: str) -> MeasurementData:
        root = ET.fromstring(xml)
        return MeasurementData(
            i1_power=float(root.find("I1").find("P").text),
            i2_power=float(root.find("I2").find("P").text),
            i3_power=float(root.find("I3").find("P").text),
            ssr1=self.__get_ssr_state("O1", root),
            ssr2=self.__get_ssr_state("O2", root),
            ssr3=self.__get_ssr_state("O3", root),
            ssr4=self.__get_ssr_state("O4", root),
            ssr5=self.__get_ssr_state("O5", root),
            ssr6=self.__get_ssr_state("O6", root),
            rele1=self.__get_ssr_state("O7", root),
            rele2=self.__get_ssr_state("O8", root),
            temperature1=float(root.find("DQ1").text),
            temperature2=float(root.find("DQ2").text),
            temperature3=float(root.find("DQ3").text),
            temperature4=float(root.find("DQ4").text),
        )

    def parse_setting(self, xml: str) -> SettingsData:
        root = ET.fromstring(xml)
        return SettingsData(time_plans=self.get_time_plans(root))

    def parse_day_stats(self, xml: str) -> DayStats:
        root = ET.fromstring(xml)
        return DayStats(
            L1_reverse_energy=float(root.find("SDS1").text),
            L2_reverse_energy=float(root.find("SDS2").text),
            L3_reverse_energy=float(root.find("SDS3").text),
            total_reverse_energy=float(root.find("SDS4").text),
            L1_forward_low_tariff_energy=float(root.find("SDL1").text),
            L2_forward_low_tariff_energy=float(root.find("SDL2").text),
            L3_forward_low_tariff_energy=float(root.find("SDL3").text),
            total_forward_low_tariff_energy=float(root.find("SDL4").text),
            L1_forward_high_tariff_energy=float(root.find("SDH1").text),
            L2_forward_high_tariff_energy=float(root.find("SDH2").text),
            L3_forward_high_tariff_energy=float(root.find("SDH3").text),
            total_forward_high_tariff_energy=float(root.find("SDH4").text),
            L1_production_energy=float(root.find("SDP1").text),
            L2_production_energy=float(root.find("SDP2").text),
            L3_production_energy=float(root.find("SDP3").text),
            total_production_energy=float(root.find("SDP4").text),
            SSR1_energy=float(root.find("SDO1").text),
            SSR2_energy=float(root.find("SDO2").text),
            SSR3_energy=float(root.find("SDO3").text),
            SSR4_energy=float(root.find("SDO4").text),
            SSR5_energy=float(root.find("SDO5").text),
            SSR6_energy=float(root.find("SDO6").text),
            rele1_energy=float(root.find("SDO7").text),
            rele2_energy=float(root.find("SDO8").text),
            wsl1_energy=float(root.find("SDO9").text),
            wsl2_energy=float(root.find("SDO10").text),
            wsl3_energy=float(root.find("SDO11").text),
            wsl4_energy=float(root.find("SDO12").text),
            wsl5_energy=float(root.find("SDO13").text),
            wsl6_energy=float(root.find("SDO14").text),
            andi1_energy=float(root.find("SDI1").text),
            andi2_energy=float(root.find("SDI2").text),
            andi3_energy=float(root.find("SDI3").text),
            andi4_energy=float(root.find("SDI4").text),
        )

    def get_time_plans(self, root: ET.Element) -> array:
        time_plans = []
        for ssr_index in range(1, 17):
            for plan_index in range(1, 5):
                name = f"TS{ssr_index}{plan_index}"
                time_plan = root.find(name)
                time_plans.append(
                    parse_time_schedule(
                        TimeScheduleArgs(
                            name=name,
                            mode=int(time_plan.find("M").text),
                            start_str=time_plan.find("N").text,
                            end_str=time_plan.find("F").text,
                            energy_limit=float(time_plan.find("Li").text),
                            power_percentage=float(time_plan.find("P").text),
                            temperature_input=int(time_plan.find("TI").text),
                            temperature_threshold=float(time_plan.find("TT").text),
                        )
                    )
                )

        return time_plans

    def __get_ssr_state(self, input_name: str, root: ET.Element) -> SSRState:
        input = root.find(input_name)
        return SSRState(
            power=float(input.find("P").text),
            energy=float(input.find("E").text),
            combiwatt_active=bool(int(input.find("HC").text)),
            forced_active=bool(int(input.find("HE").text)),
            limit_active=bool(int(input.find("HR").text)),
            regulated=bool(int(input.find("HN").text)),
            test_active=bool(int(input.find("T").text)),
        )
