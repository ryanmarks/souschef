import pint
ureg = pint.UnitRegistry()
def convert_unit(value, current_unit, desired_unit):
    try:
        current = ureg.parse_expression(current_unit)
        desired = ureg.parse_expression(desired_unit)
        measurement = value * current
        return eval("%.2f" % measurement.to(desired).magnitude)
    except:
        pass
