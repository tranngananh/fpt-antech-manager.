# module_hoc_vien.py
import os
import re
from datetime import datetime
from data_engine import DataEngine, NGUOI_HOC_FILE, DIEM_DANH_FILE

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hien_thi_danh_sach(danh_sach=None):
    if danh_sach is None:
        danh_sach = DataEngine.read_file(NGUOI_HOC_FILE)
        
    if not danh_sach:
        print("\nDanh sách học viên đang trống!")
        return

    print("-" * 115)
    print(f"{'ID':<5} | {'Họ và tên':<20} | {'SĐT':<12} | {'Email':<20} | {'Địa chỉ':<15} | {'Vắng':<5} | {'Cảnh báo'}")
    print("-" * 115)
    for hs in danh_sach:
        email_hien_thi = hs.get('email', '-')[:18] + '..' if len(hs.get('email', '-')) > 20 else hs.get('email', '-')
        dia_chi_hien_thi = hs.get('dia_chi', '-')[:13] + '..' if len(hs.get('dia_chi', '-')) > 15 else hs.get('dia_chi', '-')
        
        print(f"{hs.get('id', '-'):<5} | {hs.get('ho_va_ten', '-'):<20} | {hs.get('so_dien_thoai', '-'):<12} | "
              f"{email_hien_thi:<20} | {dia_chi_hien_thi:<15} | {hs.get('so_ngay_vang', 0):<5} | {hs.get('canh_bao', 'Không')}")
    print("-" * 115)

def them_hoc_vien():
    clear_screen()
    print("=== THÊM HỌC VIÊN MỚI ===")
    print("💡 Gợi ý: Gõ '0' và nhấn Enter ở bất kỳ bước nào để HỦY thao tác.\n")
    
    ds_hoc_vien = DataEngine.read_file(NGUOI_HOC_FILE)
    
    # 1. Nhập Họ Tên
    while True:
        ho_ten = input("Nhập Họ và tên (*): ").strip()
        if ho_ten == '0': 
            print("🚫 Đã hủy quá trình thêm học viên!"); return
        if ho_ten: break
        print("❌ Lỗi: Họ tên không được bỏ trống!")

    # 2. Nhập và Validate Số điện thoại
    while True:
        sdt = input("Nhập Số điện thoại (10 chữ số) (*): ").strip()
        if sdt == '0': 
            print("🚫 Đã hủy quá trình thêm học viên!"); return
        if not sdt:
            print("❌ Lỗi: Số điện thoại không được để trống!")
        elif not (sdt.isdigit() and len(sdt) == 10):
            print("❌ Lỗi: Số điện thoại không hợp lệ! Bắt buộc phải là 10 chữ số.")
        elif any(hs.get('so_dien_thoai') == sdt for hs in ds_hoc_vien):
            print("❌ Lỗi: Số điện thoại này đã tồn tại trong hệ thống!")
        else:
            break

    # 3. Nhập Email 
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    while True:
        email = input("Nhập Email (Enter để bỏ qua): ").strip()
        if email == '0': 
            print("🚫 Đã hủy quá trình thêm học viên!"); return
        if not email:
            email = "-"
            break
        if not re.match(email_regex, email):
            print("❌ Lỗi: Email không đúng định dạng (VD: tenban@gmail.com)!")
        elif any(hs.get('email') == email for hs in ds_hoc_vien if hs.get('email') != '-'):
            print("❌ Lỗi: Email này đã được đăng ký cho học viên khác!")
        else:
            break

    # 4. Nhập và Validate Ngày sinh
    while True:
        ngay_sinh = input("Nhập Ngày sinh (dd/mm/yyyy - Enter bỏ qua): ").strip()
        if ngay_sinh == '0': 
            print("🚫 Đã hủy quá trình thêm học viên!"); return
        if not ngay_sinh:
            ngay_sinh = "-"
            break
        try:
            datetime.strptime(ngay_sinh, "%d/%m/%Y")
            break
        except ValueError:
            print("❌ Lỗi: Ngày tháng không hợp lệ! Nhập đúng định dạng dd/mm/yyyy (VD: 25/08/2005).")

    # 5. Các thông tin khác (Gắn lối thoát '0' cho tất cả)
    gioi_tinh = input("Nhập Giới tính (*): ").strip()
    if gioi_tinh == '0': print("🚫 Đã hủy!"); return
    if not gioi_tinh: gioi_tinh = "Chưa rõ"

    khoa_hoc = input("Nhập Khóa học (*): ").strip()
    if khoa_hoc == '0': print("🚫 Đã hủy!"); return
    if not khoa_hoc: khoa_hoc = "Chưa xếp lớp"

    dan_toc = input("Nhập Dân tộc (Enter mặc định Kinh): ").strip()
    if dan_toc == '0': print("🚫 Đã hủy!"); return
    if not dan_toc: dan_toc = "Kinh"

    lop_hoc = input("Nhập Lớp học (Enter để bỏ qua): ").strip()
    if lop_hoc == '0': print("🚫 Đã hủy!"); return
    if not lop_hoc: lop_hoc = "-"

    dia_chi = input("Nhập Địa chỉ (Enter để bỏ qua): ").strip()
    if dia_chi == '0': print("🚫 Đã hủy!"); return
    if not dia_chi: dia_chi = "-"
    
    # Tùy chọn điểm danh
    print("\n🛠️ Tùy chọn điểm danh:")
    print("Đây có phải là học viên nhập bù (đã học từ đầu khóa cùng lớp) không?")
    is_nhap_bu = input("Nhập 'y' cho Có, hoặc phím bất kỳ cho Không (gõ '0' để hủy): ").strip().lower()
    if is_nhap_bu == '0': print("🚫 Đã hủy quá trình thêm học viên!"); return
    trang_thai_init = "Đi học" if is_nhap_bu == 'y' else "Chưa nhập học"

    # Tạo ID tự động
    ids = [int(str(hs.get('id', '0'))) for hs in ds_hoc_vien if str(hs.get('id', '')).isdigit()]
    next_id = str(max(ids) + 1).zfill(3) if ids else "001"

    hoc_vien_moi = {
        "id": next_id, "ho_va_ten": ho_ten, "so_dien_thoai": sdt,
        "dan_toc": dan_toc, "gioi_tinh": gioi_tinh, "ngay_sinh": ngay_sinh,
        "email": email, "dia_chi": dia_chi, "khoa_hoc": khoa_hoc,
        "lop_hoc": lop_hoc, "so_ngay_vang": 0, "canh_bao": "Không"
    }
    
    ds_hoc_vien.append(hoc_vien_moi)
    DataEngine.write_file(NGUOI_HOC_FILE, ds_hoc_vien)

    diem_danh = DataEngine.read_file(DIEM_DANH_FILE)
    for ngay, records in diem_danh.items():
        if not any(str(rec.get('id')) == str(next_id) for rec in records):
            records.append({
                "id": next_id, "ho_va_ten": ho_ten,
                "lop_hoc": lop_hoc, "trang_thai": trang_thai_init
            })
    DataEngine.write_file(DIEM_DANH_FILE, diem_danh)

    print(f"\n✅ Đã thêm học viên thành công! Mã ID được cấp là: {next_id}")

def xoa_hoc_vien():
    clear_screen()
    print("=== XÓA HỌC VIÊN ===")
    hien_thi_danh_sach()
    
    id_xoa = input("\n👉 Nhập ID học viên cần xóa (hoặc Enter/'0' để hủy): ").strip()
    if not id_xoa or id_xoa == '0': 
        print("🚫 Đã hủy thao tác xóa!")
        return
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    ds_moi = [hs for hs in ds if str(hs.get('id')) != id_xoa]
    
    if len(ds) == len(ds_moi):
        print("\n❌ Không tìm thấy học viên mang ID này!")
    else:
        DataEngine.write_file(NGUOI_HOC_FILE, ds_moi)
        print("\n✅ Đã xóa học viên thành công!")

def cap_nhat_hoc_vien():
    clear_screen()
    print("=== CẬP NHẬT THÔNG TIN HỌC VIÊN ===")
    print("💡 Gợi ý: Gõ '0' ở bất kỳ ô nhập nào để HỦY cập nhật.\n")
    
    id_sua = input("👉 Nhập ID học viên cần cập nhật (hoặc Enter/'0' để hủy): ").strip()
    if not id_sua or id_sua == '0': 
        print("🚫 Đã hủy thao tác cập nhật!")
        return
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    hoc_vien = next((hs for hs in ds if str(hs.get('id')) == id_sua), None)
    
    if not hoc_vien:
        print("\n❌ Không tìm thấy học viên mang ID này!")
        return
        
    print("\nNhập thông tin mới (nhấn Enter nếu không muốn thay đổi):")
    
    ho_ten_moi = input(f"Họ và tên [{hoc_vien.get('ho_va_ten')}]: ").strip()
    if ho_ten_moi == '0': print("🚫 Đã hủy thao tác cập nhật!"); return
    if ho_ten_moi: hoc_vien['ho_va_ten'] = ho_ten_moi
    
    while True:
        sdt_moi = input(f"SĐT (10 số) [{hoc_vien.get('so_dien_thoai')}]: ").strip()
        if sdt_moi == '0': print("🚫 Đã hủy thao tác cập nhật!"); return
        if not sdt_moi: 
            break
        if not (sdt_moi.isdigit() and len(sdt_moi) == 10):
            print("❌ Lỗi: Số điện thoại phải gồm đúng 10 chữ số!")
        elif any(hs.get('so_dien_thoai') == sdt_moi and str(hs.get('id')) != id_sua for hs in ds):
            print("❌ Lỗi: Số điện thoại này đã được sử dụng bởi học viên khác!")
        else:
            hoc_vien['so_dien_thoai'] = sdt_moi
            break
            
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    while True:
        email_moi = input(f"Email [{hoc_vien.get('email')}]: ").strip()
        if email_moi == '0': print("🚫 Đã hủy thao tác cập nhật!"); return
        if not email_moi:
            break
        if not re.match(email_regex, email_moi):
            print("❌ Lỗi: Email không đúng định dạng!")
        elif any(hs.get('email') == email_moi and str(hs.get('id')) != id_sua for hs in ds if hs.get('email') != '-'):
            print("❌ Lỗi: Email này đã được đăng ký bởi học viên khác!")
        else:
            hoc_vien['email'] = email_moi
            break

    while True:
        ngay_sinh_moi = input(f"Ngày sinh [{hoc_vien.get('ngay_sinh')}]: ").strip()
        if ngay_sinh_moi == '0': print("🚫 Đã hủy thao tác cập nhật!"); return
        if not ngay_sinh_moi:
            break
        try:
            datetime.strptime(ngay_sinh_moi, "%d/%m/%Y")
            hoc_vien['ngay_sinh'] = ngay_sinh_moi
            break
        except ValueError:
            print("❌ Lỗi: Nhập đúng định dạng dd/mm/yyyy!")

    khoa_hoc_moi = input(f"Khóa học [{hoc_vien.get('khoa_hoc')}]: ").strip()
    if khoa_hoc_moi == '0': print("🚫 Đã hủy thao tác cập nhật!"); return
    if khoa_hoc_moi: hoc_vien['khoa_hoc'] = khoa_hoc_moi
    
    dia_chi_moi = input(f"Địa chỉ [{hoc_vien.get('dia_chi')}]: ").strip()
    if dia_chi_moi == '0': print("🚫 Đã hủy thao tác cập nhật!"); return
    if dia_chi_moi: hoc_vien['dia_chi'] = dia_chi_moi
    
    DataEngine.write_file(NGUOI_HOC_FILE, ds)
    print("\n✅ Cập nhật thông tin thành công!")

def tim_kiem_hoc_vien():
    clear_screen()
    print("=== TÌM KIẾM HỌC VIÊN ===")
    tu_khoa = input("👉 Nhập từ khóa (hoặc Enter/'0' để hủy): ").strip().lower()
    
    if not tu_khoa or tu_khoa == '0': 
        return
    
    ds = DataEngine.read_file(NGUOI_HOC_FILE)
    ket_qua = []
    
    for hs in ds:
        chuoi_thong_tin = f"{hs.get('id')} {hs.get('ho_va_ten')} {hs.get('so_dien_thoai')} {hs.get('email')} {hs.get('dia_chi')} {hs.get('khoa_hoc')}".lower()
        if tu_khoa in chuoi_thong_tin:
            ket_qua.append(hs)
            
    print(f"\n🔍 Tìm thấy {len(ket_qua)} kết quả phù hợp:")
    hien_thi_danh_sach(ket_qua)

def menu_quan_ly_hoc_vien():
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