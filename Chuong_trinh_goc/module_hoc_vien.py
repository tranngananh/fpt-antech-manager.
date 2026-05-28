# module_hoc_vien.py
import os
from data_engine import DataEngine, NGUOI_HOC_FILE, DIEM_DANH_FILE

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hien_thi_danh_sach(danh_sach=None):
    """Hàm hỗ trợ in danh sách học viên ra màn hình dưới dạng bảng"""
    if danh_sach is None:
        danh_sach = DataEngine.read_file(NGUOI_HOC_FILE)
        
    if not danh_sach:
        print("\nDanh sách học viên đang trống!")
        return

    print("-" * 85)
    print(f"{'ID':<5} | {'Họ và tên':<20} | {'SĐT':<12} | {'Khóa học':<15} | {'Vắng':<5} | {'Cảnh báo'}")
    print("-" * 85)
    for hs in danh_sach:
        print(f"{hs.get('id', '-'):<5} | {hs.get('ho_va_ten', '-'):<20} | {hs.get('so_dien_thoai', '-'):<12} | "
              f"{hs.get('khoa_hoc', '-'):<15} | {hs.get('so_ngay_vang', 0):<5} | {hs.get('canh_bao', 'Không')}")
    print("-" * 85)

def them_hoc_vien():
    clear_screen()
    print("=== THÊM HỌC VIÊN MỚI ===")
    
    # Nhập thông tin cơ bản
    ho_ten = input("Nhập Họ và tên (*): ").strip()
    sdt = input("Nhập Số điện thoại (*): ").strip()
    gioi_tinh = input("Nhập Giới tính (*): ").strip()
    khoa_hoc = input("Nhập Khóa học (*): ").strip()
    
    if not ho_ten or not sdt or not gioi_tinh or not khoa_hoc:
        print("\n❌ Lỗi: Không được bỏ trống Họ tên, SĐT, Giới tính và Khóa học!")
        return

    ds_hoc_vien = DataEngine.read_file(NGUOI_HOC_FILE)
    
    # Kiểm tra trùng SĐT
    if any(hs.get('so_dien_thoai') == sdt for hs in ds_hoc_vien):
        print("\n❌ Lỗi: Số điện thoại này đã tồn tại trong hệ thống!")
        return

    # Các thông tin không bắt buộc
    dan_toc = input("Nhập Dân tộc (Enter để bỏ qua - mặc định Kinh): ").strip() or "Kinh"
    ngay_sinh = input("Nhập Ngày sinh (Enter để bỏ qua): ").strip() or "-"
    email = input("Nhập Email (Enter để bỏ qua): ").strip() or "-"
    lop_hoc = input("Nhập Lớp học (Enter để bỏ qua): ").strip() or "-"
    
    # Xử lý nhập bù điểm danh
    print("\n🛠️ Tùy chọn điểm danh:")
    print("Đây có phải là học viên nhập bù (đã học từ đầu khóa cùng lớp) không?")
    is_nhap_bu = input("Nhập 'y' cho Có, hoặc phím bất kỳ cho Không: ").strip().lower()
    trang_thai_init = "Đi học" if is_nhap_bu == 'y' else "Chưa nhập học"

    # Tạo ID tự động
    ids = [int(str(hs.get('id', '0'))) for hs in ds_hoc_vien if str(hs.get('id', '')).isdigit()]
    next_id = str(max(ids) + 1).zfill(3) if ids else "001"

    hoc_vien_moi = {
        "id": next_id,
        "ho_va_ten": ho_ten,
        "so_dien_thoai": sdt,
        "dan_toc": dan_toc,
        "gioi_tinh": gioi_tinh,
        "ngay_sinh": ngay_sinh,
        "email": email,
        "dia_chi": "-",
        "khoa_hoc": khoa_hoc,
        "lop_hoc": lop_hoc,
        "so_ngay_vang": 0,
        "canh_bao": "Không"
    }
    
    ds_hoc_vien.append(hoc_vien_moi)
    DataEngine.write_file(NGUOI_HOC_FILE, ds_hoc_vien)

    # Đồng bộ vào file điểm danh
    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    for ngay, records in diem_danh.items():
        if not any(str(rec.get('id')) == str(next_id) for rec in records):
            records.append({
                "id": next_id,
                "ho_va_ten": ho_ten,
                "lop_hoc": lop_hoc,
                "trang_thai": trang_thai_init
            })
    DataEngine.write_file(DIEM_DANH_FILE, diem_danh)

    print(f"\n✅ Đã thêm học viên thành công! Mã ID được cấp là: {next_id}")

def xoa_hoc_vien():
    clear_screen()
    print("=== XÓA HỌC VIÊN ===")
    hien_thi_danh_sach()
    
    id_xoa = input("\n👉 Nhập ID học viên cần xóa (hoặc Enter để hủy): ").strip()
    if not id_xoa: return
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    ds_moi = [hs for hs in ds if str(hs.get('id')) != id_xoa]
    
    if len(ds) == len(ds_moi):
        print("\n❌ Không tìm thấy học viên mang ID này!")
    else:
        # Lưu ý: Ở một hệ thống thực tế có thể không xóa dữ liệu bên điểm danh để giữ lịch sử, 
        # nhưng để code gọn nhẹ ta chỉ xóa bên danh sách học viên chính.
        DataEngine.write_file(NGUOI_HOC_FILE, ds_moi)
        print("\n✅ Đã xóa học viên thành công!")

def cap_nhat_hoc_vien():
    clear_screen()
    print("=== CẬP NHẬT THÔNG TIN HỌC VIÊN ===")
    id_sua = input("👉 Nhập ID học viên cần cập nhật (hoặc Enter để hủy): ").strip()
    if not id_sua: return
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    hoc_vien = next((hs for hs in ds if str(hs.get('id')) == id_sua), None)
    
    if not hoc_vien:
        print("\n❌ Không tìm thấy học viên mang ID này!")
        return
        
    print("\nNhập thông tin mới (nhấn Enter nếu không muốn thay đổi):")
    ho_ten_moi = input(f"Họ và tên [{hoc_vien.get('ho_va_ten')}]: ").strip()
    sdt_moi = input(f"SĐT [{hoc_vien.get('so_dien_thoai')}]: ").strip()
    khoa_hoc_moi = input(f"Khóa học [{hoc_vien.get('khoa_hoc')}]: ").strip()
    
    if ho_ten_moi: hoc_vien['ho_va_ten'] = ho_ten_moi
    if sdt_moi: hoc_vien['so_dien_thoai'] = sdt_moi
    if khoa_hoc_moi: hoc_vien['khoa_hoc'] = khoa_hoc_moi
    
    DataEngine.write_file(NGUOI_HOC_FILE, ds)
    print("\n✅ Cập nhật thông tin thành công!")

def tim_kiem_hoc_vien():
    clear_screen()
    print("=== TÌM KIẾM HỌC VIÊN ===")
    tu_khoa = input("👉 Nhập từ khóa (Tên, SĐT, Khóa học...): ").strip().lower()
    
    if not tu_khoa: return
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    ket_qua = []
    
    for hs in ds:
        chuoi_thong_tin = f"{hs.get('id')} {hs.get('ho_va_ten')} {hs.get('so_dien_thoai')} {hs.get('khoa_hoc')}".lower()
        if tu_khoa in chuoi_thong_tin:
            ket_qua.append(hs)
            
    print(f"\n🔍 Tìm thấy {len(ket_qua)} kết quả phù hợp:")
    hien_thi_danh_sach(ket_qua)

def menu_quan_ly_hoc_vien():
    """Hàm Menu chính của module này, được gọi từ main.py"""
    while True:
        clear_screen()
        print("==========================================")
        print("         QUẢN LÝ HỒ SƠ HỌC VIÊN           ")
        print("==========================================")
        print("  1. Xem danh sách học viên               ")
        print("  2. Thêm học viên mới                    ")
        print("  3. Cập nhật thông tin học viên          ")
        print("  4. Xóa học viên                         ")
        print("  5. Tìm kiếm học viên                    ")
        print("  0. Trở về Menu chính                    ")
        print("==========================================")
        
        chon = input("👉 Nhập lựa chọn (0-5): ").strip()
        
        if chon == '1':
            clear_screen()
            print("=== DANH SÁCH HỌC VIÊN ===")
            hien_thi_danh_sach()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '2':
            them_hoc_vien()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '3':
            cap_nhat_hoc_vien()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '4':
            xoa_hoc_vien()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '5':
            tim_kiem_hoc_vien()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '0':
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để thử lại...")