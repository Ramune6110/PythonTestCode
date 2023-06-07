import can
from can.message import Message
from random import randint
import time

# 出力する.ascファイル名を指定
logfile = can.ASCWriter("output.asc", channel=1)

# ランダムなCANメッセージを生成してログファイルに書き込む
start_time = time.time()
for i in range(100):  # 100メッセージを生成
    """
    Message：https://github.com/hardbyte/python-can/blob/develop/can/message.py
    
    Message(
            timestamp=self.timestamp,
            arbitration_id=self.arbitration_id,
            is_extended_id=self.is_extended_id,
            is_remote_frame=self.is_remote_frame,
            is_error_frame=self.is_error_frame,
            channel=self.channel,
            dlc=self.dlc,
            data=self.data,
            is_fd=self.is_fd,
            is_rx=self.is_rx,
            bitrate_switch=self.bitrate_switch,
            error_state_indicator=self.error_state_indicator,
        )
        
    timestamp: メッセージが受信された時間を秒単位で表す浮動小数点数です。この時間は、プログラムの開始時点を基準としたもので、時計の時間とは異なります。
    arbitration_id: メッセージの識別子 (ID) で、メッセージの優先度を決定します。値は通常、整数です。
    is_extended_id: メッセージが拡張ID (29ビット) を使用している場合にTrue、標準ID (11ビット) を使用している場合にFalseを返します。
    is_remote_frame: メッセージがリモートフレームである場合にTrueを返します。リモートフレームは、特定のデータを要求するためのフレームです。
    is_error_frame: メッセージがエラーフレームである場合にTrueを返します。エラーフレームは、通信上の問題を示すためのフレームです。
    channel: メッセージが属するチャネルを示す文字列または整数です。通常、物理インターフェースまたは仮想チャネルを示します。
    dlc: メッセージのデータ長（Data Length Code）です。これはメッセージのペイロード部分に含まれるバイト数を示します。
    data: メッセージのデータペイロードです。これは一般にバイトのリストまたはバイト列です。
    is_fd: メッセージがCAN FDフレームである場合にTrueを返します。CAN FDは、データレートとデータ長が拡張されたCANのバージョンです。
    is_rx: メッセージが受信されたものである場合にTrue、送信されたものである場合にFalseを返します。
    bitrate_switch: CAN FDメッセージがビットレートスイッチを使用している場合にTrueを返します。これはデータ部分が高速ビットレートで送信されていることを示します。
    error_state_indicator: CAN FDメッセージのエラー状態インジケータが有効である場合にTrueを返します。これは送信側のエラー状態を示します。

    """
    msg = Message(timestamp=time.time() - start_time,  # 現在の時間から開始時間を引いたものをタイムスタンプとする
                  arbitration_id=randint(0, 0x7FF),  # 0から0x7FFの間でランダムなIDを選択
                  data=[randint(0, 0xFF) for _ in range(8)],  # 8バイトのランダムなデータを生成
                  is_extended_id=False)  # 標準（11ビット）のCAN識別子を使用
    logfile.write_message(msg, channel="Transmitter")

# ログファイルを閉じる（必須）
logfile.stop()