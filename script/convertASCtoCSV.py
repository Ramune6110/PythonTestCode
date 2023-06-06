import can
import pandas as pd

# VectorのASCファイルを読み込む
logfile = can.ASCReader("input.asc")

# ログデータをDataFrameに変換
data = []
for msg in logfile:
    data.append({
        'Timestamp': msg.timestamp,
        'ID': msg.arbitration_id,
        'Extended': msg.is_extended_id,
        'Remote': msg.is_remote_frame,
        'Error': msg.is_error_frame,
        'DLC': msg.dlc,
        'Data': msg.data,
    })
df = pd.DataFrame(data)

# DataFrameをCSVファイルとして保存
df.to_csv('output.csv', index=False)