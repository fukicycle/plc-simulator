import random

_all_data = {}


def get_plc_data(port):
    return _all_data.get(port, {})


def set_plc_data(port, memory_data):
    _all_data[port] = memory_data


def get_point_data(port, device_type, device_code, address):
    key = f"{device_code}{address:04d}"
    target_memory_data = get_plc_data(port)
    if key in target_memory_data:
        return (target_memory_data[key], True)
    else:
        if device_type == "DIGITAL":
            value = random.choice([0, 1])
        else:
            value = random.randint(0, 4095)
        return (value, False)


def set_point_data(port, device_code, address, value):
    key = f"{device_code}{address:04d}"
    target_memory_data = get_plc_data(port)
    target_memory_data[key] = value
