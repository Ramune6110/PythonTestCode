import tkinter as tk
from tkinter import filedialog, messagebox

def extract_channel_data(input_asc_file, output_asc_file, channel_number):
    """
    ASCファイルから指定したチャンネルのデータのみを抽出し、チャンネルに属さないデータは保持して新しいASCファイルに保存する関数
    
    :param input_asc_file: 入力ASCファイルのパス
    :param output_asc_file: 出力ASCファイルのパス
    :param channel_number: 抽出するチャンネル番号（例: 1）
    """
    try:
        with open(input_asc_file, 'r') as f_in, open(output_asc_file, 'w') as f_out:
            is_triggerblock = False
            for line in f_in:
                # トリガーブロックの開始を確認
                if 'Begin Triggerblock' in line:
                    is_triggerblock = True
                
                # トリガーブロック終了までのデータをそのまま書き込む（チャンネルに属さないデータも含む）
                if not is_triggerblock or ('CANFD' not in line and 'CAN ' not in line):
                    # チャンネルに関連する行かどうかを確認する
                    parts = line.split()
                    if len(parts) > 2:
                        try:
                            # 2番目の要素がチャンネル番号に該当するか確認
                            if parts[1] == str(channel_number):
                                f_out.write(line)
                            elif 'CANFD' not in line and 'CAN ' not in line:
                                f_out.write(line)  # チャンネルに関係のない行はそのまま出力
                        except ValueError:
                            f_out.write(line)  # エラーが出た場合はそのまま出力（チャンネル番号が無い行など）
                    else:
                        f_out.write(line)  # チャンネルに関係のない行はそのまま出力
                    continue
                
                # CANFDやCANに関連するチャンネル番号の行を抽出
                if 'CANFD' in line or 'CAN ' in line:
                    parts = line.split()
                    if parts[2] == str(channel_number):  # parts[2]がチャンネル番号
                        f_out.write(line)
                
                # トリガーブロックの終了を確認
                if 'End TriggerBlock' in line:
                    f_out.write(line)
                    is_triggerblock = False

        print(f"channel{channel_number}のデータのみを含む新しいASCファイルが作成されました: {output_asc_file}")
        messagebox.showinfo("完了", f"channel{channel_number}のデータが抽出されました")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        messagebox.showerror("エラー", f"エラーが発生しました: {e}")

def open_file_dialog():
    """ファイル選択ダイアログを開く"""
    return filedialog.askopenfilename(filetypes=[("ASCファイル", "*.asc")])

def save_file_dialog():
    """保存先のファイル選択ダイアログを開く"""
    return filedialog.asksaveasfilename(defaultextension=".asc", filetypes=[("ASCファイル", "*.asc")])

def on_submit():
    """ユーザーが指定したチャンネル番号で抽出を開始"""
    input_file = open_file_dialog()
    if not input_file:
        return
    output_file = save_file_dialog()
    if not output_file:
        return
    try:
        channel_number = int(channel_entry.get())
        extract_channel_data(input_file, output_file, channel_number)
    except ValueError:
        messagebox.showerror("入力エラー", "チャンネル番号は整数で入力してください。")

# GUIの作成
root = tk.Tk()
root.title("ASCファイルからチャンネルデータ抽出")

# チャンネル番号入力用のラベルとテキストボックス
label = tk.Label(root, text="抽出するチャンネル番号を入力:")
label.pack(pady=10)

channel_entry = tk.Entry(root)
channel_entry.pack(pady=5)

# 抽出ボタン
submit_button = tk.Button(root, text="抽出開始", command=on_submit)
submit_button.pack(pady=20)

# GUIを起動
root.mainloop()

```
date Sam Sep 30 15:06:13.191 2017
base hex  timestamps absolute
internal events logged
// version 9.0.0
Begin Triggerblock Sam Sep 30 15:06:13.191 2017
  0.000000 Start of measurement
  0.015991 CAN 1 Status:chip status error passive - TxErr: 132 RxErr: 0
  0.015991 CAN 2 Status:chip status error active
  2.510001 2 100 Rx r
  2.520002 2 200 Tx r Length = 1704000 BitCount = 145 ID = 88888888x
  2.584921 2 300 Rx r 8 Length = 1704000 BitCount = 145 ID = 88888888x 
  4.501000 2 ErrorFrame Flags = 0xe CodeExt = 0x20a2 Code = 0x82 ID = 0 DLC = 0 Position = 5 Length = 11300
  30.005021 CANFD   1 Rx        300                                   1 0 8  8 11 c2 03 04 05 06 07 08   102203  133   303000 e0006659 46500250 4b140250 20011736 2001040d
  30.005041 CANFD   2 Tx        1C4D80A7x                                   0 1 8  8 12 c2 03 04 05 06 07 08   102203  133   303000 e0006659 46500250 4b140250 20011736 2001040d
  30.005071 CANFD   3 Rx        30a  Generic_Name_12                  1 1 8  8 01 02 03 04 05 06 07 08   102203  133   303000 e0006659 46500250 4b140250 20011736 2001040d
End TriggerBlock
```

import can
import tkinter as tk
from tkinter import filedialog, messagebox

# BLFをASCに変換する関数
def convert_blf_to_asc(input_blf_file, output_asc_file):
    try:
        with open(input_blf_file, 'rb') as f_in:
            log_in = can.io.BLFReader(f_in)

            with open(output_asc_file, 'w') as f_out:
                log_out = can.io.ASCWriter(f_out)
                for msg in log_in:
                    log_out.on_message_received(msg)
                log_out.stop()

        print(f"BLFファイルがASCファイルに変換されました: {output_asc_file}")
        return output_asc_file
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        messagebox.showerror("エラー", f"エラーが発生しました: {e}")
        return None

# チャンネルデータを抽出する関数
def extract_channel_data(input_asc_file, output_asc_file, channel_number):
    try:
        with open(input_asc_file, 'r') as f_in, open(output_asc_file, 'w') as f_out:
            is_triggerblock = False
            for line in f_in:
                # トリガーブロックの開始を確認
                if 'Begin Triggerblock' in line:
                    is_triggerblock = True

                # トリガーブロック終了までのデータをそのまま書き込む（チャンネルに属さないデータも含む）
                if not is_triggerblock or ('CANFD' not in line and 'CAN ' not in line):
                    # チャンネルに関連する行かどうかを確認する
                    parts = line.split()
                    if len(parts) > 2:
                        try:
                            # 2番目の要素がチャンネル番号に該当するか確認
                            if parts[1] == str(channel_number):
                                f_out.write(line)
                            elif 'CANFD' not in line and 'CAN ' not in line:
                                f_out.write(line)  # チャンネルに関係のない行はそのまま出力
                        except ValueError:
                            f_out.write(line)  # エラーが出た場合はそのまま出力（チャンネル番号が無い行など）
                    else:
                        f_out.write(line)  # チャンネルに関係のない行はそのまま出力
                    continue

                # CANFDやCANに関連するチャンネル番号の行を抽出
                if 'CANFD' in line or 'CAN ' in line:
                    parts = line.split()
                    if parts[2] == str(channel_number):  # parts[2]がチャンネル番号
                        f_out.write(line)

                # トリガーブロックの終了を確認
                if 'End TriggerBlock' in line:
                    f_out.write(line)
                    is_triggerblock = False

        print(f"channel{channel_number}のデータのみを含む新しいASCファイルが作成されました: {output_asc_file}")
        messagebox.showinfo("完了", f"channel{channel_number}のデータが抽出されました")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        messagebox.showerror("エラー", f"エラーが発生しました: {e}")

def open_blf_file_dialog():
    """BLFファイル選択ダイアログを開く"""
    return filedialog.askopenfilename(filetypes=[("BLFファイル", "*.blf")])

def save_file_dialog():
    """保存先のファイル選択ダイアログを開く"""
    return filedialog.asksaveasfilename(defaultextension=".asc", filetypes=[("ASCファイル", "*.asc")])

def on_convert_and_extract():
    """BLFファイルを指定して、指定チャンネルのデータを抽出"""
    input_blf_file = open_blf_file_dialog()  # BLFファイルを選択
    if not input_blf_file:
        return
    try:
        channel_number = int(channel_entry.get())  # チャンネル番号を取得
    except ValueError:
        messagebox.showerror("入力エラー", "チャンネル番号は整数で入力してください。")
        return

    # 一時的なASCファイルのパスを生成（変換用）
    temp_asc_file = "temp_output.asc"
    
    # BLFをASCに変換
    converted_asc_file = convert_blf_to_asc(input_blf_file, temp_asc_file)
    if not converted_asc_file:
        return

    # チャンネルデータを抽出する保存先ファイルを選択
    output_file = save_file_dialog()
    if not output_file:
        return

    # 指定チャンネルのデータを抽出して新規ASCファイルを生成
    extract_channel_data(converted_asc_file, output_file, channel_number)

# GUIの作成
root = tk.Tk()
root.title("BLFからASC変換 & チャンネル抽出")

# チャンネル番号入力用のラベルとテキストボックス
label = tk.Label(root, text="抽出するチャンネル番号を入力:")
label.pack(pady=10)

channel_entry = tk.Entry(root)
channel_entry.pack(pady=5)

# BLF -> ASC変換とチャンネル抽出ボタン
convert_button = tk.Button(root, text="BLFファイルを指定して変換 & 抽出", command=on_convert_and_extract)
convert_button.pack(pady=20)

# GUIを起動
root.mainloop()
