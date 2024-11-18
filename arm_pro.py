import serial
import time

# チャンネル3は手首で500側が内側に閉じる、2500側が上に上がる
# チャンネル2は関節で500側が上向きに上げる
# チャンネル1
# チャンネル0はベースの旋回2500側で右に回り、500側で左に回る
# 500から2500
BASE_ANGLE = 1500
MAX_ANGLE = 2500
MIN_ANGLE = 500
TOTAL_CHANNELS = 5  # チャンネル数
BASE_SPEED = 300


class AL5D:
    def __init__(self, port="/dev/tty.usbserial-AB0K6DQX", baudrate=9600):
        self.base_angle = BASE_ANGLE
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connect()
        self.initialize_position()

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print("シリアルポートが開かれました。")
        except serial.serialutil.SerialException as e:
            print(f"シリアルポートエラー: {e}")

    def initialize_position(self):
        if self.ser and self.ser.is_open:
            for channel in range(TOTAL_CHANNELS):
                command = f"#{channel} P{self.base_angle} S{BASE_SPEED}\r"
                print(f"送信コマンド: {command}")
                self.ser.write(command.encode("ascii"))
                time.sleep(0.1)  # 各コマンドの間に少し待つ
            print("すべてのサーボモーターを初期位置にセットしました。")
            time.sleep(1)  # 応答を待つ
            response = self.ser.read_all().decode("ascii")
            print(f"受信応答: {response}")

    def move_servo(self, channel, position, speed):
        if self.ser and self.ser.is_open:
            command = f"#{channel} P{position} S{speed}\r"
            print(f"送信コマンド: {command}")
            self.ser.write(command.encode("ascii"))
            time.sleep(1)  # 応答を待つ
            response = self.ser.read_all().decode("ascii")
            print(f"受信応答: {response}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("シリアルポートが閉じられました。")


if __name__ == "__main__":
    robot_arm = AL5D()
    # robot_arm.move_servo(0, 1700, 750)
    robot_arm.move_servo(5, 500, 300)
    robot_arm.move_servo(4, 500, 300)
    robot_arm.move_servo(2, 1700, 300)
    robot_arm.move_servo(1, 2000, 300)
    robot_arm.move_servo(0, 500, 300)
    robot_arm.close()
