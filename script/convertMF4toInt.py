"""
このスクリプトは、MF4ファイルから"data"という名前のチャネルを抽出し、
それらのデータをバイト配列に変換します。
その後、1バイトごとにデータを分割し、各分割されたデータを一つの整数として解釈します。
最後に、得られた整数を出力します。
"""

from asammdf import MDF

# MF4ファイルを開く
mdf_file = MDF('output.mf4')

# "data"チャネルからデータを取得
data_signal = mdf_file.get('data')

# データをバイト配列に変換
byte_data = data_signal.samples.tobytes()

# バイト配列を整数に変換
int_data = [int.from_bytes(byte_data[i:i+1], byteorder='big') for i in range(0, len(byte_data))]

# 出力
for i, val in enumerate(int_data):
    print(f"Byte {i+1}: {val}")
