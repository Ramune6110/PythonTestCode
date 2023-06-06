import can
from asammdf import MDF, Signal
import numpy as np

# ASCファイルを開きます
"""
ex)input.asc

date Tue Dec 17 08:30:07.364 2019
base hex  timestamps absolute
internal events logged
Begin Triggerblock Tue Dec 17 08:30:07.364 2019
   0.000000 1  Receiver    d 8  8D 0B 8F A1 9C FE AA 38   Length     1 BitCount     1
   0.000562 1  Transmitter  d 8  AD 1B 7F 31 AC EE BA 28   Length     1 BitCount     1
   0.000938 2  Receiver    d 8  3D 2B 6F C1 BC DE CA 18   Length     1 BitCount     1
   0.001875 1  Transmitter  d 8  CD 3B 5F 51 CC CE DA 08   Length     1 BitCount     1
   0.002812 2  Receiver    d 8  4D 4B 4F E1 DC BE EA F8   Length     1 BitCount     1
End TriggerBlock
"""
asc_reader = can.ASCReader("input.asc")

# データを格納するためのリストを用意します
timestamps = []
channels = []
data = []

# 各メッセージからデータを抽出します
for msg in asc_reader:
    timestamps.append(msg.timestamp)
    channels.append(msg.channel)
    data.append(msg.data)

# numpy配列に変換します
timestamps = np.array(timestamps)
channels = np.array(channels, dtype=np.uint8)
data = np.array(data, dtype=np.uint8)

# 各データに対応するSignalを作成します
timestamp_signal = Signal(timestamps, timestamps, name="timestamp")
channel_signal = Signal(channels, timestamps, name="channel")
data_signal = Signal(data, timestamps, name="data")

# MDFファイルを作成し、Signalを追加します
mdf = MDF(version="4.10")
mdf.append([timestamp_signal, channel_signal, data_signal])

# MDFファイルを保存します
mdf.save("output.mf4", overwrite=True)

"""
ex)output.mf4

1."timestamp"信号: 各CANメッセージのタイムスタンプを保持しています。
  この例では、その値は [0.000000, 0.000562, 0.000938, 0.001875, 0.002812]となります。
2."channel"信号: どのチャンネルがメッセージを送信したかを示します。
  この例では、その値は [1, 1, 2, 1, 2]となります。
3."data"信号: 各メッセージのデータ部分を保持しています。
  このデータは8バイトのバイナリデータとして格納されます。
  したがって、各メッセージのデータをバイトの配列として解釈します。
  この例では、それぞれのメッセージのデータは
  [0x8D, 0x0B, 0x8F, 0xA1, 0x9C, 0xFE, 0xAA, 0x38], 
  [0xAD, 0x1B, 0x7F, 0x31, 0xAC, 0xEE, 0xBA, 0x28], 
  [0x3D, 0x2B, 0x6F, 0xC1, 0xBC, 0xDE, 0xCA, 0x18], 
  [0xCD, 0x3B, 0x5F, 0x51, 0xCC, 0xCE, 0xDA, 0x08], 
  [0x4D, 0x4B, 0x4F, 0xE1, 0xDC, 0xBE, 0xEA, 0xF8]
  
  例えば，1行目に関して，それぞれの16進数のバイトを10進数に変換すると次のようになります：
    0x8D = 141
    0x0B = 11
    0x8F = 143
    0xA1 = 161
    0x9C = 156
    0xFE = 254
    0xAA = 170
    0x38 = 56
  ただし、8バイト全体を1つの大きな数値として解釈する場合、これらのバイトを一緒に連結し、
  それを一つの16進数として解釈し、それを10進数に変換します。それは大きな数値になるため、通常は各バイトを個別に解釈します。

ただし、この情報は生の数値データとして.mf4ファイルに格納されます。
したがって、.mf4ファイル自体をテキストエディタで開いても、上記の情報は直接的には見えません。
代わりに、.mf4ファイルはASAM MDFツール（例えば、MDF4 ViewerやMDF Validator）やasammdfを使用して解析・閲覧することができます。
"""