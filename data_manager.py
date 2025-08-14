# data_manager.py

import json
from pathlib import Path

class DataManager:
    """
    Một class chuyên để quản lý việc đọc, ghi và lưu trữ trạng thái dữ liệu.
    """
    # Phương thức 1: Khởi tạo
    def __init__(self, log_file_path):
        self.log_file = Path(log_file_path)
        # Tạo ra "ngăn chứa" bên trong
        self.current_state = {} 
        # Tự động khôi phục trạng thái
        self._load_initial_state()

    # Phương thức 2 (nội bộ): Đọc file log để khôi phục
    def _load_initial_state(self):
        default_state = {"voltage": 0.0, "temp": 0.0, "battery_curr": 0.0}
        
        if not self.log_file.is_file():
            self.current_state = default_state
            print(f"INFO (DataManager): File log không tìm thấy. Dùng trạng thái mặc định: {self.current_state}")
            return

        try:
            with open(self.log_file, 'r') as f:
                last_line = None
                for line in f:
                    if line.strip():
                        last_line = line
                
                if last_line:
                    self.current_state = json.loads(last_line)
                    print(f"INFO (DataManager): Khôi phục trạng thái thành công: {self.current_state}")
                else:
                    self.current_state = default_state
                    print(f"INFO (DataManager): File log trống. Dùng trạng thái mặc định: {self.current_state}")
        except Exception as e:
            self.current_state = default_state
            print(f"ERROR (DataManager): Lỗi đọc file log, dùng trạng thái mặc định. Chi tiết: {e}")

    # Phương thức 3 (nội bộ): Ghi vào file log
    def _write_to_log(self, data):
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            print(f"ERROR (DataManager): Lỗi ghi file log: {e}")

    # --- CÁC PHƯƠNG THỨC CÔNG KHAI ---

    # Phương thức 4: Cập nhật trạng thái và ghi log
    def update_state_and_log(self, new_data):
        self.current_state = new_data
        self._write_to_log(new_data)
        print(f"INFO (DataManager): Trạng thái đã được cập nhật -> {self.current_state}")

    # Phương thức 5: Trả về trạng thái hiện tại
    def get_current_state(self):
        return self.current_state