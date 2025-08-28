import struct
import extension


class MelsecNetProtocol:
    def __init__(self):
        self.device_codes = {
            b"\x20\x4d": "M",  # DIGITAL
            b"\x20\x44": "D",  # WORD
            b"\x20\x42": "B",  # DIGITAL
            b"\x20\x57": "W",  # WORD
            b"\x20\x58": "X",  # DIGITAL
            b"\x20\x59": "Y",  # DIGITAL
        }
        self.device_types = {
            "M": "DIGITAL",
            "D": "WORD",
            "B": "DIGITAL",
            "W": "WORD",
            "X": "DIGITAL",
            "Y": "DIGITAL",
        }
        self.base_numbers = {"M": 10, "D": 10, "B": 16, "W": 16, "X": 16, "Y": 16}

    def decode_frame(self, data):
        if len(data) < 12:
            print("Recived data is too short for a valid frame.")
            return None

        request = {
            "command": None,
            "command_data": None,
            "device_type": None,
            "device_code": None,
            "address": None,
            "count": None,
            "values": None,
            "base_number": None,
        }

        command = data[0:1]
        pc_num = data[1:2]
        acpu_monitor_timer = data[2:4]
        address = data[4:8]
        device_code = data[8:10]
        count = data[10:11]

        # extension.print_hex_to_console(command)
        # extension.print_hex_to_console(pc_num)
        # extension.print_hex_to_console(acpu_monitor_timer)
        # extension.print_hex_to_console(address)
        # extension.print_hex_to_console(device_type)
        # extension.print_hex_to_console(count)

        if command == b"\x00":
            request["command"] = "read_bit"
        elif command == b"\x01":
            request["command"] = "read_word"
        elif command == b"\x02":
            request["command"] = "write_bit"
        elif command == b"\x03":
            request["command"] = "write_word"
        else:
            request["command"] = "not_supported"

        request["command_data"] = command
        request["address"] = int.from_bytes(address, "little")
        request["count"] = int.from_bytes(count, "little")
        request["device_code"] = self.device_codes.get(device_code, None)
        request["device_type"] = self.device_types.get(request["device_code"], None)
        request["base_number"] = self.base_numbers.get(request["device_code"], None)

        return request

    def create_response_frame(self, response_data):
        status = response_data.get("status")
        command_data = response_data.get("command_data")
        response_command_data = (
            int.from_bytes(command_data, "little") | 0x80
        ).to_bytes(len(command_data), "little")
        if status == "success":
            end_code = b"\x00"
            values = response_data.get("values", [])
            value_bytes = b"".join([struct.pack("<H", v) for v in values])

            response_frame = response_command_data

            response_frame += end_code

            response_frame += value_bytes

            return response_frame
        else:
            error_code = b"\x50"
            response_frame = response_command_data
            response_frame += error_code
            return response_frame
