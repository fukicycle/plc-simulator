import random
class PlcLogic:

    def process_request(self, request):
        """
        電文の要求を処理し、応答データを生成します。
        requestのフォーマットは、melsecnet_protocl.pyで定義します。
        """
        # PLCのロジックを処理する
        command = request.get("command")
        command_data = request.get("command_data")
        device_type = request.get("device_type")
        address = request.get("address")
        count = request.get("count")

        response_data = {}

        if command == "read_word":
            values = self.read_word(device_type, count)
            response_data = {
                "status": "success",
                "values": values,
                "command_data": command_data,
            }
        elif command == "read_bit":
            response_data = {"status": "success"}
        else:
            response_data = {"status": "error", "message": "Invalid command"}
        return response_data

    def read_word(self, device_type, count):
        """
        指定されたデバイスタイプ、アドレス、カウントに基づいてデータを読み取ります。
        """
        values = []
        for i in range(count):
            value = random.randint(0, 65535)
            values.append(value)

        return values
