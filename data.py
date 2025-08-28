import random

_all_data = {}


def get_plc_data(port):
    return _all_data.get(port, {})


def set_plc_data(port, memory_data):
    _all_data[port] = memory_data


def get_point_data(port, device_type, device_code, address, base_number):
    key = _get_key(device_code, address, base_number)
    target_memory_data = get_plc_data(port)
    if key in target_memory_data:
        return (target_memory_data[key], True)
    else:
        if device_type == "DIGITAL":
            value = random.choice([0, 1])
        else:
            value = random.randint(0, 65535)
        return (value, False)


def set_point_data(port, device_code, address, base_number, value):
    key = _get_key(device_code, address, base_number)
    target_memory_data = get_plc_data(port)
    target_memory_data[key] = value


def _get_key(device_code, address, base_number):
    if base_number == 16:
        key = f"{device_code}{address:04X}"
    elif base_number == 10:
        key = f"{device_code}{address:04d}"
    else:
        raise ValueError(f"Invalid base number: {base_number}")
    return key
