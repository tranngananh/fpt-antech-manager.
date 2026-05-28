# module_thong_ke.py
import os
from data_engine import DataEngine, NGUOI_HOC_FILE

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hien_thi_bieu_do_phan_tram(gia_tri, tong_so, chieu_dai_thanh=30):
    """Hàm hỗ trợ vẽ thanh biểu đồ (bar chart) bằng các ký tự khối đặc"""
    if tong_so == 0:
        return "[ Chưa có dữ liệu ]"
    
    phan_tram = (gia_tri / tong_so) * 100
    so_block = int((phan_tram / 100) * chieu_dai_thanh)
    # Dùng ký tự khối đặc '█' để làm thanh biểu đồ, dấu '-' để làm nền
    thanh_bieu_do = '█' * so_block + '-' * (chieu_dai_thanh - so_block)
    
    return f"[{thanh_bieu_do}] {phan_tram:5.1f}% ({gia_tri:2} học viên)"

def thong_ke_suc_khoe_hoc_vu():
    """Thống kê tỉ lệ cảnh báo học vụ - tương đương biểu đồ tròn trên Web"""
    clear_screen()
    print("=== THỐNG KÊ SỨC KHỎE HỌC VỤ ===")
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    tong_so = len(ds)
    
    if tong_so == 0:
        print("\n❌ Chưa có dữ liệu học viên trong hệ thống!")
        return

    # Đếm số lượng theo từng nhóm cảnh báo
    hoc_tap = sum(1 for hs in ds if hs.get('canh_bao') == 'Cảnh báo học tập')
    nghi_hoc = sum(1 for hs in ds if hs.get('canh_bao') == 'Cảnh báo nghỉ học')
    binh_thuong = tong_so - hoc_tap - nghi_hoc

    print(f"\n📊 TỔNG SỐ HỌC VIÊN HIỆN TẠI: {tong_so}\n")
    print(f" 🟢 Bình thường              : {hien_thi_bieu_do_phan_tram(binh_thuong, tong_so)}")
    print(f" 🟡 Cảnh báo học tập (3-4)   : {hien_thi_bieu_do_phan_tram(hoc_tap, tong_so)}")
    print(f" 🔴 Cảnh báo nghỉ học (>=5)  : {hien_thi_bieu_do_phan_tram(nghi_hoc, tong_so)}")

def thong_ke_khoa_hoc():
    """Thống kê lượng học viên phân bổ theo từng khóa học"""
    clear_screen()
    print("=== THỐNG KÊ THEO KHÓA HỌC ===")
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    tong_so = len(ds)
    
    if tong_so == 0:
        print("\n❌ Chưa có dữ liệu học viên trong hệ thống!")
        return
        
    tk_khoa_hoc = {}
    for hs in ds:
        kh = hs.get('khoa_hoc', 'Chưa xếp lớp').strip()
        if not kh: kh = "Chưa xếp lớp"
        tk_khoa_hoc[kh] = tk_khoa_hoc.get(kh, 0) + 1
        
    print(f"\n📊 TỔNG SỐ HỌC VIÊN HIỆN TẠI: {tong_so}\n")
    
    # Sắp xếp khóa học theo số lượng học viên giảm dần
    for kh, so_luong in sorted(tk_khoa_hoc.items(), key=lambda x: x[1], reverse=True):
        print(f" 📖 Khóa {kh:<17}: {hien_thi_bieu_do_phan_tram(so_luong, tong_so)}")

def menu_thong_ke():
    """Hàm Menu chính của module Thống kê"""
    while True:
        clear_screen()
        print("==========================================")
        print("            BÁO CÁO THỐNG KÊ              ")
        print("==========================================")
        print("  1. Tỉ lệ sức khỏe học vụ (Theo cảnh báo)")
        print("  2. Phân bổ học viên theo Khóa học       ")
        print("  0. Trở về Menu chính                    ")
        print("==========================================")
        
        chon = input("👉 Nhập lựa chọn (0-2): ").strip()
        
        if chon == '1':
            thong_ke_suc_khoe_hoc_vu()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '2':
            thong_ke_khoa_hoc()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '0':
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để thử lại...")