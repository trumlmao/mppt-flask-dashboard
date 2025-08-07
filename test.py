# app.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    # ---- PHẦN MỚI ----
    # Giả sử đây là dữ liệu bạn đọc được từ cảm biến
    ten_thiet_bi = "MPPT Solar Charger 01"
    nhiet_do_hien_tai = 38.5
    # ------------------

    # Khi gọi render_template, ta truyền thêm dữ liệu vào
    # device_name và temp là "biến" mà HTML có thể sử dụng
    return render_template(
        'home.html', 
        device_name=ten_thiet_bi, 
        temp=nhiet_do_hien_tai
    )

if __name__ == '__main__':
    app.run(debug=True)