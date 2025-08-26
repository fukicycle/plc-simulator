import random


class PlcLogic:
    def __init__(self, memory_data):
        self.memory_data = memory_data

    def process_request(self, port, request):
        """
        電文の要求を処理し、応答データを生成します。
        requestのフォーマットは、melsecnet_protocl.pyで定義します。
        """
        # PLCのロジックを処理する
        command = request.get("command")
        command_data = request.get("command_data")
        device_type = request.get("device_type")
        device_code = request.get("device_code")
        address = request.get("address")
        count = request.get("count")

        response_data = {}

        if command == "read_word":
            values = self.read_word(port, device_type, device_code, address, count)
            response_data = {
                "status": "success",
                "values": values,
                "command_data": command_data,
            }
        elif command == "read_bit":
            values = self.read_bit(port, device_type, device_code, address, count)
            response_data = {
                "status": "success",
                "values": values,
                "command_data": command_data,
            }
        elif command == "write_word":
            values = []
            response_data = {
                "status": "success",
                "values": values,
                "command_data": command_data,
            }
        elif command == "write_bit":
            values = []
            response_data = {
                "status": "success",
                "values": values,
                "command_data": command_data,
            }
        else:
            response_data = {"status": "error", "message": "Invalid command"}
        return response_data

    def read_word(self, port, device_type, device_code, address, count):
        """
        指定されたデバイスタイプ、アドレス、カウントに基づいてデータを読み取ります。
        """
        values = []
        for i in range(count):
            key = f"{device_code}{address + i:04d}"
            if key in self.memory_data:
                value = self.memory_data[key]
            else:
                if device_type == "DIGITAL":
                    value = random.choice([0, 1])
                else:
                    value = random.randint(0, 4095)
                self.memory_data[key] = value
            values.append(value)

        return values

    def read_bit(self, port, device_type, device_code, address, count):
        values = []
        for i in range(count):
            value = random.choice([0, 1])
            print(
                f"[{port}] Reading bit from {device_code}{address + i:04d} -> {value}"
            )
            values.append(value)

        return values
