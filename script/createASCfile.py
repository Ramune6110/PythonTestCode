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
    """
    msg = Message(timestamp=time.time() - start_time,  # 現在の時間から開始時間を引いたものをタイムスタンプとする
                  arbitration_id=randint(0, 0x7FF),  # 0から0x7FFの間でランダムなIDを選択
                  data=[randint(0, 0xFF) for _ in range(8)],  # 8バイトのランダムなデータを生成
                  is_extended_id=False)  # 標準（11ビット）のCAN識別子を使用
    logfile.write_message(msg, channel="Transmitter")

# ログファイルを閉じる（必須）
logfile.stop()