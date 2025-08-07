# app.py (phiên bản chống đạn)

from flask import Flask, render_template, request, jsonify
from pathlib import Path
import json

# --- Cấu hình ---
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE_PATH = BASE_DIR / "mppt_data.log"

app = Flask(__name__)

# --- Các hàm trợ giúp (Helpers) ---

def write_to_log_file(data_dict):
    """Ghi một dictionary vào file log dưới dạng một dòng JSON."""
    try:
        json_string = json.dumps(data_dict)
        with open(LOG_FILE_PATH, 'a') as f:
            f.write(json_string + '\n')
    except Exception as e:
        print(f"ERROR writing to log file: {e}")

def load_last_known_state():
    """
    Đọc dòng cuối cùng của file log để khôi phục trạng thái.
    Trả về một dictionary hoặc None nếu có lỗi/không có file.
    """
    if not LOG_FILE_PATH.is_file():
        print("INFO: Log file not found. Starting with default state.")
        return None
        
    try:
        with open(LOG_FILE_PATH, 'r') as f:
            last_line = None
            for line in f:
                if line.strip(): # Bỏ qua các dòng trống
                    last_line = line
            
            if last_line:
                return json.loads(last_line)
            else:
                print("INFO: Log file is empty. Starting with default state.")
                return None
    except Exception as e:
        print(f"ERROR reading or parsing log file: {e}")
        return None

# --- Khởi tạo và Khôi phục Trạng thái ---

print("--- Initializing Server ---")
# 1. Thử khôi phục trạng thái
initial_data = load_last_known_state()

# 2. Nếu không khôi phục được, dùng trạng thái mặc định. Ngược lại, dùng trạng thái đã khôi phục.
if not initial_data:
    du_lieu_hien_tai = {"voltage": 0.0, "temp": 0.0, "battery_curr": 0.0}
else:
    du_lieu_hien_tai = initial_data

print(f"Initial state loaded: {du_lieu_hien_tai}")
print("---------------------------")


# --- Các Route (API Endpoints) ---

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/api/latest-data')
def get_latest_data():
    return jsonify(du_lieu_hien_tai)

@app.route('/data', methods=['POST'])
def receive_data_endpoint():
    global du_lieu_hien_tai
    incoming_data = request.get_json()
    du_lieu_hien_tai = incoming_data
    write_to_log_file(incoming_data)
    return jsonify({"status": "OK"})

# --- Chạy ứng dụng ---
if __name__ == '__main__':
    app.run(debug=True)