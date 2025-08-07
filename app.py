# app.py

# Thêm 'request' và 'jsonify' vào danh sách công cụ
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Một biến tạm để lưu dữ liệu mới nhất (giống như một cái bảng tin)
du_lieu_hien_tai = {
    "voltage": 0.0,
    "temp": 0.0,
    "battery_curr": 0.0
}

# --- Cửa cho NGƯỜI DÙNG (dùng GET) ---
@app.route('/')
def home_page():
    # Lấy dữ liệu từ "bảng tin" và hiển thị ra
    return render_template('home.html', data=du_lieu_hien_tai)

# --- Cửa cho MÁY MÓC (dùng POST) ---
@app.route('/data', methods=['POST'])
def receive_data_endpoint():
    # Lấy dữ liệu JSON mà máy gửi lên
    incoming_data = request.get_json()
    
    # In ra terminal để xem ta nhận được gì
    print("Đã nhận được dữ liệu:", incoming_data)
    # Cách đơn giản nhất là cập nhật từng key cho rõ ràng:
    global du_lieu_hien_tai # Đừng quên dòng này
    du_lieu_hien_tai['voltage'] = incoming_data['voltage']
    du_lieu_hien_tai['temp'] = incoming_data['temp']
    du_lieu_hien_tai['battery_curr'] = incoming_data['battery_curr']
    
    # Trả lời lại cho máy gửi rằng "OK đã nhận"
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(debug=True)