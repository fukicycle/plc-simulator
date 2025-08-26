from asyncio import sleep
import threading
from plc_server import PlcServer
from plc_logic import PlcLogic
from melsecnet_protocol import MelsecNetProtocol
import os
import json
import queue
import sys


def load_memory_data(port):
    filename = f"data\\memory_data_{port}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_memory_data(port, memory_data):
    filename = f"data\\memory_data_{port}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=2)


def _finalize(server_threads, result_queue):
    try:
        while True:
            print("Enter 'q' to quit:")
            n = input()
            if n == "q":
                print("Terminate")
                break
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Terminating...")
    finally:
        stop_event.set()
        for thread in server_threads:
            thread.join()
        while not result_queue.empty():
            result = result_queue.get()
            save_memory_data(result["port"], result["data"])
        print("正常終了しました")
        sys.exit()


if __name__ == "__main__":
    HOST = "172.19.190.101"
    PORT_START = 3001
    PORT_END = 3002

    server_threads = []
    stop_event = threading.Event()
    result_queue = queue.Queue()

    for port in range(PORT_START, PORT_END + 1):
        plc_logic = PlcLogic(load_memory_data(port))
        protocol_handler = MelsecNetProtocol()
        server = PlcServer(
            HOST, port, plc_logic, protocol_handler, stop_event, result_queue
        )

        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_threads.append(server_thread)
        server_thread.start()

    print("すべてのPLCが起動しました。")

_finalize(server_threads, result_queue)