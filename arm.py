import serial
import time

try:
    # シリアルポートの設定
    ser = serial.Serial("/dev/tty.usbserial-AB0K6DQX", 9600, timeout=1)
    print("シリアルポートが開かれました。")

    # コマンドの送信
    command = "#0 P1700 S750\r"
    print(f"送信コマンド: {command}")
    ser.write(command.encode("ascii"))  # ASCIIエンコードで送信
    print("コマンドが送信されました。")

    # 応答の確認
    time.sleep(1)  # 少し待ってから応答を確認
    response = ser.read_all().decode("ascii")
    print(f"受信応答: {response}")

except serial.serialutil.SerialException as e:
    print(f"シリアルポートエラー: {e}")

finally:
    # シリアルポートが開かれている場合のみ閉じる
    if "ser" in locals() and ser.is_open:
        ser.close()
        print("シリアルポートが閉じられました。")
