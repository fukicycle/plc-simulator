import random
import data


class PlcLogic:
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
            values = self.read(port, device_type, device_code, address, count)
            response_data = {
                "status": "success",
                "values": values,
                "command_data": command_data,
            }
        elif command == "read_bit":
            values = self.read(port, device_type, device_code, address, count)
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

    def read(self, port, device_type, device_code, address, count):
        """
        指定されたデバイスタイプ、アドレス、カウントに基づいてデータを読み取ります。
        """
        values = []
        for i in range(count):
            (value, exists) = data.get_point_data(
                port, device_type, device_code, address + i
            )
            if not exists:
                data.set_point_data(port, device_code, address + i, value)
            values.append(value)

        return values
