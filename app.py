# app.py (phiên bản cập nhật)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

du_lieu_hien_tai = {
    "voltage": 0.0,
    "temp": 0.0,
    "battery_curr": 0.0
}

# --- Route cũ: Trả về trang web LẦN ĐẦU TIÊN ---
# Nó sẽ hiển thị các giá trị ban đầu (0.0)
@app.route('/')
def home_page():
    return render_template('home.html')

# --- Route CŨ: Nhận dữ liệu từ simulator (KHÔNG THAY ĐỔI) ---
@app.route('/data', methods=['POST'])
def receive_data_endpoint():
    incoming_data = request.get_json()
    global du_lieu_hien_tai
    du_lieu_hien_tai = incoming_data # Gán lại cả dict cho đơn giản
    return jsonify({"status": "OK"})

# --- Route MỚI: Cung cấp dữ liệu mới nhất cho JavaScript ---
@app.route('/api/latest-data')
def get_latest_data():
    # Hàm này chỉ có một nhiệm vụ: trả về dữ liệu dưới dạng JSON
    return jsonify(du_lieu_hien_tai)

if __name__ == '__main__':
    app.run(debug=True)