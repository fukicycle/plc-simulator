import socket
import threading
import extension


class PlcServer:

    def __init__(self, host, port, plc_logic, protocol_handler):
        self.host = host
        self.port = port
        self.plc_logic = plc_logic
        self.protocol_handler = protocol_handler
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"PLCサーバが{self.host}:{self.port}で起動しました。")

    def start(self):
        while True:
            conn, addr = self.server_socket.accept()
            print(f"クライアントが接続しました: {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(conn,))
            client_handler.start()

    def handle_client(self, conn):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"受信したデータ: {extension.hex_to_formatted_string(data)}")
                request = self.protocol_handler.decode_frame(data)

                if request:
                    response_data = self.plc_logic.process_request(request)

                    response_frame = self.protocol_handler.create_response_frame(
                        response_data
                    )
                    conn.sendall(response_frame)
                    print(f"送信したデータ: {extension.hex_to_formatted_string(response_frame)}")
                else:
                    print("無効なリクエストです。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        finally:
            conn.close()
            print(f"クライアントが切断されました")
