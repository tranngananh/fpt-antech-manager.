# main.py
import os
import sys

# Import bộ xử lý dữ liệu lõi
from data_engine import DataEngine

# Import 5 module chức năng đã xây dựng
import module_hoc_vien
import module_diem_danh
import module_canh_bao
import module_thong_ke
import module_cai_dat

def hien_thi_menu():
    """Hàm hiển thị giao diện Menu chính của chương trình"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================================")
    print("      HỆ THỐNG QUẢN LÝ HỌC VIÊN & ĐIỂM DANH       ")
    print("==================================================")
    print("  1. Quản lý học viên (Thêm, Xóa, Sửa, Tìm kiếm)  ")
    print("  2. Quản lý điểm danh (Thêm/Xóa ngày, Điểm danh) ")
    print("  3. Cảnh báo học vụ (Học tập & Nghỉ học)         ")
    print("  4. Báo cáo thống kê                             ")
    print("  5. Cài đặt (Hồ sơ cá nhân & Admin)              ")
    print("  0. Thoát chương trình                           ")
    print("==================================================")

def main():
    # 1. Luôn kiểm tra và khởi tạo file JSON (Database) nếu chưa có khi vừa mở app
    DataEngine.initialize_db()

    # 2. Vòng lặp chính của chương trình
    while True:
        hien_thi_menu()
        lua_chon = input("👉 Nhập lựa chọn của bạn (0-5): ").strip()

        if lua_chon == '1':
            # Gọi Menu cấp 2 của chức năng Quản lý học viên
            module_hoc_vien.menu_quan_ly_hoc_vien()
            
        elif lua_chon == '2':
            # Gọi Menu cấp 2 của chức năng Quản lý điểm danh
            module_diem_danh.menu_quan_ly_diem_danh()
            
        elif lua_chon == '3':
            # Gọi Menu cấp 2 của chức năng Cảnh báo học vụ
            module_canh_bao.menu_canh_bao()
            
        elif lua_chon == '4':
            # Gọi Menu cấp 2 của chức năng Thống kê
            module_thong_ke.menu_thong_ke()
            
        elif lua_chon == '5':
            # Gọi Menu cấp 2 của chức năng Cài đặt tài khoản
            module_cai_dat.menu_cai_dat()
            
        elif lua_chon == '0':
            print("\n👋 Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            sys.exit()
            
        else:
            print("\n❌ Lựa chọn không hợp lệ! Vui lòng nhập số từ 0 đến 5.")
            input("Nhấn Enter để thao tác lại...")

# Điểm bắt đầu chạy của chương trình Python
if __name__ == "__main__":
    main()