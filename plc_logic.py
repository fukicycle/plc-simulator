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
        base_number = request.get("base_number")

        # 必須項目にNoneが含まれていればエラーとして扱う
        required_fields = [
            command,
            command_data,
            device_type,
            device_code,
            address,
            count,
        ]
        if any(field is None for field in required_fields):
            return {
                "status": "error",
                "message": "Request contains None in required fields",
            }

        response_data = {}

        if command == "read_word":
            values = self.read(
                port, device_type, device_code, address, base_number, count
            )
            response_data = {
                "status": "success",
                "values": values,
                "command_data": command_data,
            }
        elif command == "read_bit":
            values = self.read(
                port, device_type, device_code, address, base_number, count
            )
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

    def read(self, port, device_type, device_code, address, base_number, count):
        """
        指定されたデバイスタイプ、アドレス、カウントに基づいてデータを読み取ります。
        """
        values = []
        if device_type == "DIGITAL":
            # 先頭アドレスをワード境界に丸める
            start_address = (address // 16) * 16

            for word_index in range(count):
                word_address = start_address + word_index * 16
                word_value = 0

                # 16ビットを集めてワード化（リトルエンディアン）
                for bit_offset in range(16):
                    bit_address = word_address + bit_offset
                    (bit_value, exists) = data.get_point_data(
                        port, device_type, device_code, bit_address, base_number
                    )
                    if not exists:
                        # 初期化（存在しなければ0を登録）
                        bit_value = 0
                        data.set_point_data(
                            port, device_code, bit_address, base_number, bit_value
                        )

                    # ビットをワードに反映
                    word_value |= (bit_value & 1) << bit_offset

                values.append(word_value)
        else:
            for i in range(count):
                (value, exists) = data.get_point_data(
                    port, device_type, device_code, address + i, base_number
                )
                if not exists:
                    data.set_point_data(
                        port, device_code, address + i, base_number, value
                    )
                values.append(value)

        return values
