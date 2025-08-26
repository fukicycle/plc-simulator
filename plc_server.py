import socket
import threading
import extension


class PlcServer:

    def __init__(self, host, port, plc_logic, protocol_handler, stop_event):
        self.host = host
        self.port = port
        self.plc_logic = plc_logic
        self.protocol_handler = protocol_handler
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(1.0)
        self.stop_event = stop_event
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"PLCサーバが{self.host}:{self.port}で起動しました。")

    def start(self):
        while not self.stop_event.is_set():
            try:
                conn, addr = self.server_socket.accept()
                print(f"クライアントが接続しました: {addr}")
                client_handler = threading.Thread(
                    target=self.handle_client, args=(conn,)
                )
                client_handler.start()
            except socket.timeout:
                # タイムアウトが発生したらループを継続
                pass
            except Exception as e:
                print(f"接続待ちでエラーが発生しました: {e}")
                break

    def handle_client(self, conn):
        try:
            while not self.stop_event.is_set():
                data = conn.recv(1024)
                if not data:
                    break
                # print(
                #     f"[{self.port}] 受信したデータ: {extension.hex_to_formatted_string(data)}"
                # )
                request = self.protocol_handler.decode_frame(data)

                if request:
                    response_data = self.plc_logic.process_request(self.port, request)

                    response_frame = self.protocol_handler.create_response_frame(
                        response_data
                    )
                    conn.sendall(response_frame)
                    # print(f"[{self.port}] OK")
                    # print(f"送信したデータ: {extension.hex_to_formatted_string(response_frame)}")
                else:
                    print("無効なリクエストです。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        finally:
            conn.close()
            print(f"クライアントが切断されました")
