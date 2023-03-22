from custom_components.wattrouter.xml_parser import XmlParser


def test_parse_measurement_should_parse_inputs_power():
    with open("tests/measurement1.xml", "r", encoding="utf8") as file:
        xml = file.read()
        measurement = XmlParser().parse_measurement(xml)

        assert measurement.i1_power == 1.01
        assert measurement.i2_power == 20
        assert measurement.i3_power == 4.01


def test_parse_measurement_should_parse_temperatures():
    with open("tests/measurement1.xml", "r", encoding="utf8") as file:
        xml = file.read()
        measurement = XmlParser().parse_measurement(xml)

        assert measurement.temperature1 == 14.0
        assert measurement.temperature2 == 55.0
        assert measurement.temperature3 == 34.0
        assert measurement.temperature4 == 22.2


def test_parse_measurement_should_parse_ssrs():
    with open("tests/measurement1.xml", "r", encoding="utf8") as file:
        xml = file.read()
        measurement = XmlParser().parse_measurement(xml)

        assert measurement.ssr1.power == 1.50
        assert measurement.ssr1.energy == 5.37
        assert measurement.ssr1.combiwatt_active is True
        assert measurement.ssr1.forced_active is True
        assert measurement.ssr1.limit_active is True
        assert measurement.ssr1.regulated is True
        assert measurement.ssr1.test_active is True

        assert measurement.ssr2.power == 0.70
        assert measurement.ssr2.energy == 3.77

        assert measurement.ssr3.power == 0.20
        assert measurement.ssr3.energy == 1.68

'''def test_parse_setting_should_parse_ssr1_time_plans():
    with open("tests/configuration1.xml", "r", encoding="utf8") as file:
        xml = file.read()
        configuration = XmlParser().parse_setting(xml)

        assert configuration.time_plans_ssr1.count() == 4'''

