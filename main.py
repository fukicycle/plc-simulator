import threading
from plc_server import PlcServer
from plc_logic import PlcLogic
from melsecnet_protocol import MelsecNetProtocol
import sys

if __name__ == "__main__":
    HOST = "172.19.190.101"
    PORTS = [3001, 3002, 3003, 3004, 3005]

    server_threads = []

    for port in PORTS:
        plc_logic = PlcLogic()
        protocol_handler = MelsecNetProtocol()
        server = PlcServer(HOST, port, plc_logic, protocol_handler)

        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_threads.append(server_thread)
        server_thread.start()

    print("すべてのPLCが起動しました。")
    while True:
        n = input()
        if n == "q":
            print("Terminate")
            sys.exit()