# module_canh_bao.py
import os
from data_engine import DataEngine, NGUOI_HOC_FILE

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def in_danh_sach_canh_bao(danh_sach, tieu_de):
    """Hàm hỗ trợ in bảng danh sách dựa trên dữ liệu đã lọc"""
    clear_screen()
    print(f"=== {tieu_de.upper()} ===")
    
    if not danh_sach:
        print("\n🎉 Tuyệt vời! Không có học viên nào nằm trong danh sách này.")
        return

    print("-" * 85)
    print(f"{'ID':<5} | {'Họ và tên':<20} | {'SĐT':<12} | {'Khóa học':<15} | {'Vắng':<5} | {'Cảnh báo'}")
    print("-" * 85)
    for hs in danh_sach:
        print(f"{hs.get('id', '-'):<5} | {hs.get('ho_va_ten', '-'):<20} | {hs.get('so_dien_thoai', '-'):<12} | "
              f"{hs.get('khoa_hoc', '-'):<15} | {hs.get('so_ngay_vang', 0):<5} | {hs.get('canh_bao', 'Không')}")
    print("-" * 85)
    print(f"Tổng cộng: {len(danh_sach)} học viên.")

def xem_canh_bao_hoc_tap():
    """Lọc những người vắng từ 3 đến dưới 5 buổi"""
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    ds_loc = [hs for hs in ds if hs.get('canh_bao') == 'Cảnh báo học tập']
    in_danh_sach_canh_bao(ds_loc, "Danh sách Cảnh báo học tập (Vắng 3 - 4 buổi)")

def xem_canh_bao_nghi_hoc():
    """Lọc những người vắng từ 5 buổi trở lên"""
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    ds_loc = [hs for hs in ds if hs.get('canh_bao') == 'Cảnh báo nghỉ học']
    in_danh_sach_canh_bao(ds_loc, "Danh sách Cảnh báo nghỉ học (Vắng >= 5 buổi)")

def xem_tat_ca_canh_bao():
    """Lọc tất cả những người đang bị cảnh báo và sắp xếp theo số ngày vắng giảm dần"""
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    ds_loc = [hs for hs in ds if hs.get('canh_bao') in ['Cảnh báo học tập', 'Cảnh báo nghỉ học']]
    
    # Sắp xếp danh sách: Ai vắng nhiều nhất xếp lên đầu
    ds_loc.sort(key=lambda x: x.get('so_ngay_vang', 0), reverse=True)
    in_danh_sach_canh_bao(ds_loc, "Tất cả học viên bị cảnh báo (Xếp theo số ngày vắng)")

def menu_canh_bao():
    """Hàm Menu chính của module cảnh báo"""
    while True:
        clear_screen()
        print("==========================================")
        print("         DANH SÁCH CẢNH BÁO HỌC VỤ        ")
        print("==========================================")
        print("  1. Xem danh sách Cảnh báo học tập (3-4 buổi)")
        print("  2. Xem danh sách Cảnh báo nghỉ học (>=5 buổi)")
        print("  3. Xem toàn bộ học viên vi phạm kỷ luật     ")
        print("  0. Trở về Menu chính                        ")
        print("==========================================")
        
        chon = input("👉 Nhập lựa chọn (0-3): ").strip()
        
        if chon == '1':
            xem_canh_bao_hoc_tap()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '2':
            xem_canh_bao_nghi_hoc()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '3':
            xem_tat_ca_canh_bao()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '0':
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để thử lại...")