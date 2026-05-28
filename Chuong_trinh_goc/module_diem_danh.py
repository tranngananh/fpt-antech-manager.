# module_diem_danh.py
import os
from data_engine import DataEngine, NGUOI_HOC_FILE, DIEM_DANH_FILE

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def sync_to_nguoi_hoc():
    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    ds_hoc_vien = DataEngine.read_file(NGUOI_HOC_FILE) 
    
    vong_dem = {}
    for ngay, records in diem_danh.items():
        for rec in records:
            if str(rec.get('trang_thai', '')).strip() == 'Vắng':
                raw_id = str(rec.get('id', '')).strip()
                norm_id = raw_id.lstrip('0') if raw_id.lstrip('0') != '' else raw_id
                vong_dem[norm_id] = vong_dem.get(norm_id, 0) + 1

    for hs in ds_hoc_vien:
        raw_id = str(hs.get('id', '')).strip()
        norm_id = raw_id.lstrip('0') if raw_id.lstrip('0') != '' else raw_id
        
        so_vang = vong_dem.get(norm_id, 0)
        hs['so_ngay_vang'] = so_vang
        
        if so_vang >= 5:
            hs['canh_bao'] = "Cảnh báo nghỉ học"
        elif 5 > so_vang >= 3:
            hs['canh_bao'] = "Cảnh báo học tập"
        else:
            hs['canh_bao'] = "Không"

    DataEngine.write_file(NGUOI_HOC_FILE, ds_hoc_vien)

def xem_danh_sach_ngay():
    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    if not diem_danh:
        print("\nChưa có ngày điểm danh nào trong hệ thống!")
        return []
    
    print("\n--- CÁC NGÀY ĐÃ TẠO ĐIỂM DANH ---")
    danh_sach_ngay = sorted(diem_danh.keys())
    for i, ngay in enumerate(danh_sach_ngay, 1):
        print(f" {i}. Ngày: {ngay} (Có {len(diem_danh[ngay])} bản ghi)")
    return danh_sach_ngay

# THÊM MỚI: Hàm xem chi tiết điểm danh theo ngày
def xem_thong_tin_diem_danh():
    clear_screen()
    print("=== XEM CHI TIẾT ĐIỂM DANH ===")
    danh_sach_ngay = xem_danh_sach_ngay()
    if not danh_sach_ngay: return

    ngay_chon = input("\n👉 Nhập chính xác tên ngày muốn xem (hoặc '0' để HỦY): ").strip()
    
    if not ngay_chon or ngay_chon == '0':
        return
        
    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    if ngay_chon not in diem_danh:
        print("\n❌ Ngày này không tồn tại!")
        return

    records = diem_danh[ngay_chon]
    
    clear_screen()
    print(f"=== CHI TIẾT ĐIỂM DANH NGÀY: {ngay_chon} ===")
    print("-" * 65)
    print(f"{'ID':<5} | {'Họ và tên':<25} | {'Lớp học':<10} | {'Trạng thái'}")
    print("-" * 65)
    
    tong_co_mat = 0
    tong_vang = 0
    
    for rec in records:
        tt = rec.get('trang_thai', 'Vắng')
        if tt == 'Có mặt':
            tong_co_mat += 1
        else:
            tong_vang += 1
            
        print(f"{rec.get('id', '-'):<5} | {rec.get('ho_va_ten', '-'):<25} | {rec.get('lop_hoc', '-'):<10} | {tt}")
        
    print("-" * 65)
    print(f"📊 TỔNG KẾT: Sĩ số {len(records)} | Có mặt: {tong_co_mat} | Vắng: {tong_vang}")

def them_ngay_diem_danh():
    clear_screen()
    print("=== THÊM NGÀY ĐIỂM DANH MỚI ===")
    ngay_moi = input("👉 Nhập ngày học mới (VD: 28/05/2026) hoặc '0' để HỦY: ").strip()
    
    if not ngay_moi or ngay_moi == '0': 
        print("🚫 Đã hủy thao tác!")
        return

    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    if ngay_moi in diem_danh:
        print("\n⚠️ Ngày này đã tồn tại trong hệ thống!")
        return

    ds_hoc_vien = DataEngine.read_file(NGUOI_HOC_FILE)
    if not ds_hoc_vien:
        print("\n⚠️ Danh sách học viên đang trống, hãy thêm học viên trước!")
        return

    diem_danh[ngay_moi] = [
        {
            "id": hs.get('id'),
            "ho_va_ten": hs.get('ho_va_ten'),
            "lop_hoc": hs.get('lop_hoc', '-'),
            "trang_thai": "Vắng"
        }
        for hs in ds_hoc_vien
    ]
    
    DataEngine.write_file(DIEM_DANH_FILE, diem_danh)
    sync_to_nguoi_hoc()
    print(f"\n✅ Đã tạo cột điểm danh cho ngày {ngay_moi} thành công!")

def xoa_ngay_diem_danh():
    clear_screen()
    print("=== XÓA NGÀY ĐIỂM DANH ===")
    danh_sach_ngay = xem_danh_sach_ngay()
    if not danh_sach_ngay: return

    ngay_xoa = input("\n👉 Nhập chính xác tên ngày muốn xóa (hoặc '0' để HỦY): ").strip()
    if not ngay_xoa or ngay_xoa == '0': 
        print("🚫 Đã hủy thao tác!")
        return

    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    if ngay_xoa in diem_danh:
        del diem_danh[ngay_xoa]
        DataEngine.write_file(DIEM_DANH_FILE, diem_danh)
        sync_to_nguoi_hoc()
        print(f"\n✅ Đã xóa ngày {ngay_xoa} khỏi hệ thống!")
    else:
        print("\n❌ Không tìm thấy ngày này!")

def thuc_hien_diem_danh():
    clear_screen()
    print("=== THỰC HIỆN ĐIỂM DANH ===")
    danh_sach_ngay = xem_danh_sach_ngay()
    if not danh_sach_ngay: return

    ngay_chon = input("\n👉 Nhập chính xác tên ngày muốn điểm danh (hoặc '0' để HỦY): ").strip()
    
    if not ngay_chon or ngay_chon == '0':
        print("🚫 Đã hủy thao tác!")
        return
        
    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    if ngay_chon not in diem_danh:
        print("\n❌ Ngày này không tồn tại!")
        return

    records = diem_danh[ngay_chon]
    print(f"\n--- Đang điểm danh cho ngày: {ngay_chon} ---")
    print("💡 Hướng dẫn: BẮT BUỘC nhập 'c' (Có mặt) hoặc 'v' (Vắng). Gõ '0' để DỪNG ĐIỂM DANH giữa chừng.")
    
    for rec in records:
        trang_thai_cu = rec.get('trang_thai', 'Vắng')
        luu_y = "(Đang Có mặt)" if trang_thai_cu == "Có mặt" else "(Đang Vắng)"
        
        while True:
            nhap = input(f"Học viên: {rec.get('id')} - {rec.get('ho_va_ten')} {luu_y} -> ").strip().lower()
            
            if nhap == '0':
                break
                
            if nhap == 'c':
                rec['trang_thai'] = "Có mặt"
                break
                
            elif nhap == 'v':
                rec['trang_thai'] = "Vắng"
                break
                
            else:
                print("   ❌ Lỗi: Lựa chọn không hợp lệ! Vui lòng chỉ nhập 'c' hoặc 'v'.")
                
        if nhap == '0':
            print("\n⏸️ Đã tạm dừng điểm danh. Kết quả từ đầu đến giờ đã được lưu lại an toàn!")
            break
            
    DataEngine.write_file(DIEM_DANH_FILE, diem_danh)
    sync_to_nguoi_hoc()
    print("\n✅ Đã cập nhật xong dữ liệu điểm danh!")

def menu_quan_ly_diem_danh():
    while True:
        clear_screen()
        print("==========================================")
        print("           QUẢN LÝ ĐIỂM DANH              ")
        print("==========================================")
        print("  1. Xem chi tiết điểm danh theo ngày     ")
        print("  2. Thêm ngày điểm danh mới              ")
        print("  3. Thực hiện điểm danh (Tích Có/Vắng)   ")
        print("  4. Xóa ngày điểm danh                   ")
        print("  0. Trở về Menu chính                    ")
        print("==========================================")
        
        chon = input("👉 Nhập lựa chọn (0-4): ").strip()
        
        if chon == '1':
            xem_thong_tin_diem_danh()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '2':
            them_ngay_diem_danh()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '3':
            thuc_hien_diem_danh()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '4':
            xoa_ngay_diem_danh()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '0':
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để thử lại...")