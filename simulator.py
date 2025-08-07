
# simulator.py

# Cần thư viện 'requests' để gửi yêu cầu HTTP
import requests
import time
import random

# Địa chỉ "cánh cửa" POST của server chúng ta
API_ENDPOINT = "http://127.0.0.1:5000/data"

# Vòng lặp gửi dữ liệu mỗi 3 giây
while True:
    try:
        # Dữ liệu cần gửi, dưới dạng Dictionary
        data_to_send = {"voltage": round(random.uniform(12, 35), 1),
                        "temp": round(random.uniform(20,50),1),
                        "battery_curr":round(random.uniform(0,5),1)}
        
        print("Đang gửi:", data_to_send)
        
        # Gửi dữ liệu bằng phương thức POST
        response = requests.post(url=API_ENDPOINT, json=data_to_send)
        
        # In ra phản hồi từ server
        print("Phản hồi từ server:", response.text)
        
    except Exception as e:
        print("Lỗi:", e)
        
    time.sleep(3)