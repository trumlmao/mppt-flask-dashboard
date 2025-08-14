# simulator.py

import paho.mqtt.client as mqtt
import time
import random
import json # <-- Cần import json

# --- Cấu hình ---
BROKER_ADDRESS = "localhost"
PORT = 1883
TOPIC = "mppt/data"
CLIENT_ID = "mppt_simulator_01" 

# --- Khởi tạo MQTT Client ---
# Truyền Client ID vào khi tạo client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)

print(f"Đang kết nối đến Broker tại {BROKER_ADDRESS}...")
client.connect(BROKER_ADDRESS, PORT)

# Bắt đầu vòng lặp của client trên một luồng riêng
client.loop_start() 
print("Kết nối thành công! Bắt đầu gửi dữ liệu...")

try:
    while True:
        # 1. Tạo dữ liệu ngẫu nhiên
        data_to_send = {
            "voltage": round(random.uniform(12, 35), 1),
            "temp": round(random.uniform(20, 50), 1),
            "battery_curr": round(random.uniform(0, 5), 1)
        }
        
        # 2. Chuyển đổi dictionary thành chuỗi JSON
        payload = json.dumps(data_to_send)
        
        # 3. Publish chuỗi JSON lên topic
        result = client.publish(TOPIC, payload)
        
        # Kiểm tra xem publish có thành công không
        if result[0] == 0:
            print(f"Đã gửi: {payload}")
        else:
            print(f"Gửi thất bại, mã lỗi: {result[0]}")
            
        # 4. Đợi
        time.sleep(3)

except KeyboardInterrupt:
    print("Dừng chương trình.")
finally:
    # Dừng vòng lặp của client và ngắt kết nối
    client.loop_stop()
    client.disconnect()
    print("Đã ngắt kết nối.")