"""
PLCシミュレータアプリケーションのメインエントリポイントです。
このスクリプトは、複数のPLCサーバインスタンスをスレッドで初期化・起動します。
ローカルJSONファイルからPLCデータを読み込み、ロジックやプロトコルハンドラを設定し、
サーバのライフサイクル管理（正常終了・データ保存）を行います。

関数:
    load_local_data(port): 指定ポートのPLCデータをローカルJSONファイルから読み込みます。
    save_local_data(port, plc_data): 指定ポートのPLCデータをローカルJSONファイルに保存します。

実行フロー:
    - 'data'ディレクトリが存在しなければ作成します。
    - 指定範囲の各ポートについて、PLCデータを読み込み、ロジック・プロトコルハンドラを初期化し、
      PLCサーバを個別スレッドで起動します。
    - ユーザー入力('q')またはKeyboardInterruptで終了を待機します。
    - 終了時にPLCデータをローカルファイルへ保存し、全スレッドをjoinします。

必要モジュール:
    threading, os, json, plc_server, plc_logic, melsecnet_protocol, data

使い方:
    このスクリプトを直接実行するとPLCシミュレータサーバが起動します。
"""

import threading
from plc_server import PlcServer
from plc_logic import PlcLogic
from melsecnet_protocol import MelsecNetProtocol
import os
import json
import data


def load_local_data(port):
    filename = f"data\\plc_data_{port}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_local_data(port, plc_data):
    filename = f"data\\plc_data_{port}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(plc_data, f, ensure_ascii=False, indent=2)


def list_json_files():
    return [f for f in os.listdir("data") if f.endswith(".json")]


if __name__ == "__main__":
    HOST = "172.19.190.101"
    PORT_START = 3001
    PORT_END = 3002

    server_threads = []
    stop_event = threading.Event()

    if not os.path.exists("data"):
        os.makedirs("data")

    # 設定ファイルを読み込む
    settings = list_json_files()
    
    # 設定ファイルを監視するスレッドを立ち上げる
    # TODO　実装書く

    # 指定された分のPLCを起動する
    for port in range(PORT_START, PORT_END + 1):
        data.set_plc_data(port, load_local_data(port))
        plc_logic = PlcLogic()
        protocol_handler = MelsecNetProtocol()
        server = PlcServer(HOST, port, plc_logic, protocol_handler, stop_event)
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_threads.append(server_thread)
        server_thread.start()

    print("すべてのPLCが起動しました。")
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

    # すべてのplc_dataをローカルに保存する
    for port in range(PORT_START, PORT_END + 1):
        plc_data = data.get_plc_data(port)
        save_local_data(port, plc_data)
    print("正常終了しました")
