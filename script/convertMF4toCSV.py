import csv
from asammdf import MDF

# MF4ファイルを開く
mdf_file = MDF('output.mf4')

# 各信号を取得
timestamp_signal = mdf_file.get('timestamp')
channel_signal = mdf_file.get('channel')
dlc_signal = mdf_file.get('dlc')
data_signal = mdf_file.get('data')

# データをバイト配列に変換し，整数に変換
int_data = []
for sample, dlc in zip(data_signal.samples, dlc_signal.samples):
    byte_data = sample.tobytes()
    int_sample = [int.from_bytes(byte_data[i:i+1], byteorder='big') for i in range(0, min(len(byte_data), dlc))]
    int_data.append(int_sample)

# timestamp, channel, int_dataを組み合わせてリストを作成
output_data = list(zip(timestamp_signal.samples, channel_signal.samples, int_data))

# CSVファイルへ出力
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Channel', 'Data'])  # header
    for row in output_data:
        writer.writerow(row)
