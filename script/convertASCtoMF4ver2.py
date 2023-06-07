import can
from asammdf import MDF, Signal
import numpy as np

# ASCファイルを開きます
asc_reader = can.ASCReader("input.asc")

# データを格納するためのリストを用意します
timestamps = []
channels = []
data = []

# 各メッセージからデータを抽出します
for msg in asc_reader:
    timestamps.append(msg.timestamp)
    channels.append(msg.channel)
    # バイトデータを個別に10進数に変換し、リストとして保存します
    data.append([byte for byte in msg.data])

# numpy配列に変換します
timestamps = np.array(timestamps)
channels = np.array(channels, dtype=np.uint8)
# データのサイズに応じてdtypeを調整します
# データサイズが最大64byteであることを考慮して、dtypeをnp.objectにします
data = np.array(data, dtype=np.object)

# 各データに対応するSignalを作成します
timestamp_signal = Signal(timestamps, timestamps, name="timestamp")
channel_signal = Signal(channels, timestamps, name="channel")
data_signal = Signal(data, timestamps, name="data")

# MDFファイルを作成し、Signalを追加します
mdf = MDF(version="4.10")
mdf.append({"timestamp": timestamp_signal, "channel": channel_signal, "data": data_signal})

# MDFファイルを保存します
mdf.save("output.mf4", overwrite=True)

#######################################################
#######################################################
#######################################################

import can
from asammdf import MDF, Signal
import numpy as np

# ASCファイルを開きます
asc_reader = can.ASCReader("input.asc")

# データを格納するためのリストを用意します
timestamps = []
channels = []
data = []

# 各メッセージからデータを抽出します
for msg in asc_reader:
    timestamps.append(msg.timestamp)
    channels.append(msg.channel)
    # バイトデータを整数に変換します
    data.append(int.from_bytes(msg.data, byteorder='big'))

# numpy配列に変換します
timestamps = np.array(timestamps)
channels = np.array(channels, dtype=np.uint8)
data = np.array(data, dtype=np.uint32)  # Changed to uint32 to hold large numbers

# 各データに対応するSignalを作成します
timestamp_signal = Signal(timestamps, timestamps, name="timestamp")
channel_signal = Signal(channels, timestamps, name="channel")
data_signal = Signal(data, timestamps, name="data")

# MDFファイルを作成し、Signalを追加します
mdf = MDF(version="4.10")
mdf.append({"timestamp": timestamp_signal, "channel": channel_signal, "data": data_signal})  # Changed to dict

# MDFファイルを保存します
mdf.save("output.mf4", overwrite=True)