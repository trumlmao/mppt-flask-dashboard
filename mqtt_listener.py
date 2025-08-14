# mqtt_listener.py

import paho.mqtt.client as mqtt
import json
from data_manager import DataManager # <-- Import "hộp đen" của chúng ta
from pathlib import Path

# --- Cấu hình ---
BROKER_ADDRESS = "localhost"
PORT = 1883
TOPIC = "mppt/data"
CLIENT_ID = "mppt_backend_listener_01"

# Đường dẫn đến file log
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "mppt_data.log"

# --- Khởi tạo DataManager ---
# Tạo ra một "người xử lý" chuyên dụng
datamanager = DataManager(log_file_path=LOG_FILE)
print("INFO: DataManager đã sẵn sàng.")

# --- Các hàm Callback cho MQTT ---

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback được gọi khi kết nối thành công."""
    if rc == 0:
        print("INFO: Đã kết nối thành công đến MQTT Broker!")
        # Đăng ký nghe trên topic chỉ định
        client.subscribe(TOPIC)
        print(f"INFO: Đang lắng nghe trên topic '{TOPIC}'...")
    else:
        print(f"ERROR: Kết nối thất bại, mã lỗi: {rc}")

def on_message(client, userdata, msg):
    """Callback được gọi mỗi khi có tin nhắn mới."""
    print(f"-> Nhận được tin nhắn từ topic '{msg.topic}'")
    
    try:
        # Lấy nội dung tin nhắn và chuyển từ bytes thành string
        payload_str = msg.payload.decode('utf-8')
        # Chuyển chuỗi JSON thành dictionary
        data_dict = json.loads(payload_str)
        
        # Gọi "hộp đen" để xử lý và ghi dữ liệu
        data_manager.update_state_and_log(data_dict)
        
    except json.JSONDecodeError:
        print("ERROR: Tin nhắn nhận được không phải là JSON hợp lệ.")
    except Exception as e:
        print(f"ERROR: Đã có lỗi xảy ra khi xử lý tin nhắn: {e}")

# --- Khởi tạo và Chạy MQTT Client ---

# Tạo client mới với API v2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)

# Gắn các hàm callback vào client
client.on_connect = on_connect
client.on_message = on_message

# Thực hiện kết nối
print(f"INFO: Đang kết nối đến Broker tại {BROKER_ADDRESS}...")
client.connect(BROKER_ADDRESS, PORT)
print(f"INFO: Đang kết nối đến Broker tại {BROKER_ADDRESS}...")
# Bắt đầu vòng lặp vô tận để lắng nghe.
# Đây là một lệnh blocking, chương trình sẽ dừng ở đây.
client.loop_forever()