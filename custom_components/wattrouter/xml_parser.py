import xml.etree.ElementTree as ET
from array import array

from custom_components.wattrouter.time_schedule_mode_parser import parse_time_schedule

from .state import (
    MeasurementData,
    SSRState,
    SettingsData,
    TimePlanSettings,
    TimePlanState,
)


class XmlParser:
    def parse_measurement(self, xml: str) -> MeasurementData:
        root = ET.fromstring(xml)
        return MeasurementData(
            i1_power=float(root.find("I1").find("P").text),
            i2_power=float(root.find("I2").find("P").text),
            i3_power=float(root.find("I3").find("P").text),
            ssr1=self.get_ssr_state("O1", root),
            ssr2=self.get_ssr_state("O2", root),
            ssr3=self.get_ssr_state("O3", root),
            ssr4=self.get_ssr_state("O4", root),
            ssr5=self.get_ssr_state("O5", root),
            ssr6=self.get_ssr_state("O6", root),
            rele1=self.get_ssr_state("O7", root),
            rele2=self.get_ssr_state("O8", root),
            temperature1=float(root.find("DQ1").text),
            temperature2=float(root.find("DQ2").text),
            temperature3=float(root.find("DQ3").text),
            temperature4=float(root.find("DQ4").text),
        )

    def get_ssr_state(self, input_name: str, root: ET.Element) -> SSRState:
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

    def parse_setting(self, xml: str) -> SettingsData:
        root = ET.fromstring(xml)
        return SettingsData(
            time_plans_ssr1=self.get_time_plans("TS1", root),
            time_plans_ssr2=self.get_time_plans("O1", root),
            time_plans_ssr3=self.get_time_plans("O1", root),
            time_plans_ssr4=self.get_time_plans("O1", root),
            time_plans_ssr5=self.get_time_plans("O1", root),
            time_plans_ssr6=self.get_time_plans("O1", root),
            time_plans_rele1=self.get_time_plans("O1", root),
            time_plans_rele2=self.get_time_plans("O1", root),
        )

    def get_time_plans(self, input_name: str, root: ET.Element) -> array:
        time_plans = []
        for i in [1, 2, 3, 4]:
            time_plan = root.find(f"{input_name}{i}")
            time_plans.append(
                parse_time_schedule(
                    int(time_plan.find("M").text),
                    time_plan.find("N").text,
                    time_plan.find("F").text,
                    float(time_plan.find("Li").text),
                    float(time_plan.find("P").text),
                    int(time_plan.find("TI").text),
                    float(time_plan.find("TT").text),
                )
            )

        return time_plans
