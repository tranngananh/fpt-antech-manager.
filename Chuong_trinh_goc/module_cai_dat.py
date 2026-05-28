# module_cai_dat.py
import os
import json
import hashlib

# Đường dẫn file tài khoản (Nằm trong thư mục data)
USERS_FILE = './data/users.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def _hash(password):
    """Hàm băm mật khẩu để bảo mật"""
    return hashlib.sha256(password.encode()).hexdigest()

def khoi_tao_tai_khoan_mac_dinh():
    """Tự động tạo tài khoản admin nếu file chưa tồn tại"""
    if not os.path.exists('./data'):
        os.makedirs('./data', exist_ok=True)
        
    if not os.path.exists(USERS_FILE) or os.stat(USERS_FILE).st_size == 0:
        default_admin = [{
            "username": "admin",
            "password": _hash("admin123"), # Mật khẩu mặc định
            "role": "admin",
            "ho_ten": "Quản trị viên",
            "email": "admin@fpt.edu.vn",
            "so_dien_thoai": "0987654321"
        }]
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_admin, f, indent=4, ensure_ascii=False)

def doc_users():
    khoi_tao_tai_khoan_mac_dinh()
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def ghi_users(data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def xem_ho_so_ca_nhan(user):
    clear_screen()
    print("=== HỒ SƠ CÁ NHÂN ===")
    print(f"👤 Username : {user['username']}")
    print(f"📝 Họ và tên: {user.get('ho_ten', '-')}")
    print(f"📧 Email    : {user.get('email', '-')}")
    print(f"📞 SĐT      : {user.get('so_dien_thoai', '-')}")
    print(f"🔑 Quyền hạn: {user.get('role', 'nhanvien').upper()}")

def doi_mat_khau(username):
    clear_screen()
    print("=== ĐỔI MẬT KHẨU ===")
    mk_cu = input("👉 Nhập mật khẩu CŨ: ").strip()
    mk_moi = input("👉 Nhập mật khẩu MỚI: ").strip()
    
    users = doc_users()
    for u in users:
        if u['username'] == username:
            if u['password'] != _hash(mk_cu):
                print("\n❌ Mật khẩu cũ không chính xác!")
                return
            if not mk_moi:
                print("\n❌ Mật khẩu mới không được để trống!")
                return
                
            u['password'] = _hash(mk_moi)
            ghi_users(users)
            print("\n✅ Đổi mật khẩu thành công!")
            return

def them_tai_khoan():
    clear_screen()
    print("=== [ADMIN] THÊM TÀI KHOẢN MỚI ===")
    new_user = input("👉 Nhập Username mới: ").strip()
    if not new_user: return
    
    users = doc_users()
    if any(u['username'] == new_user for u in users):
        print("\n❌ Tên đăng nhập này đã tồn tại!")
        return
        
    new_pass = input("👉 Nhập Mật khẩu: ").strip()
    new_role = input("👉 Nhập Quyền (admin/nhanvien): ").strip().lower()
    if new_role not in ['admin', 'nhanvien']:
        new_role = 'nhanvien'
        
    new_hoten = input("👉 Nhập Họ tên: ").strip()
    
    users.append({
        "username": new_user,
        "password": _hash(new_pass),
        "role": new_role,
        "ho_ten": new_hoten,
        "email": "-",
        "so_dien_thoai": "-"
    })
    ghi_users(users)
    print(f"\n✅ Đã tạo tài khoản [{new_user}] thành công!")

def menu_cai_dat():
    """Hàm Menu chính của module Cài đặt"""
    khoi_tao_tai_khoan_mac_dinh()
    
    # Bước xác thực danh tính mô phỏng
    clear_screen()
    print("==========================================")
    print("        BẢO MẬT PHÂN HỆ CÀI ĐẶT           ")
    print("==========================================")
    print("💡 Hệ thống cần xác nhận danh tính của bạn.")
    print("💡 Gợi ý: Tài khoản gốc là -> admin")
    
    nhap_user = input("\n👉 Nhập username của bạn (hoặc 0 để thoát): ").strip()
    if nhap_user == '0' or not nhap_user:
        return
        
    users = doc_users()
    current_user = next((u for u in users if u['username'] == nhap_user), None)
    
    if not current_user:
        print("\n❌ Không tìm thấy tài khoản trong hệ thống!")
        input("Nhấn Enter để quay lại...")
        return

    # Menu hiển thị động dựa trên Quyền (Role)
    while True:
        clear_screen()
        print("==========================================")
        print("            CÀI ĐẶT HỆ THỐNG              ")
        print("==========================================")
        print(f"👤 Đang thao tác: {current_user['ho_ten']} ({current_user['role'].upper()})")
        print("-" * 42)
        print("  1. Xem hồ sơ cá nhân                    ")
        print("  2. Đổi mật khẩu                         ")
        
        # Chỉ Admin mới thấy 2 chức năng này
        if current_user['role'] == 'admin':
            print("  3. 🔑 [Admin] Thêm tài khoản nhân viên  ")
            print("  4. 🔑 [Admin] XEM danh sách tài khoản   ")
            
        print("  0. Trở về Menu chính                    ")
        print("==========================================")
        
        chon = input("👉 Nhập lựa chọn: ").strip()
        
        if chon == '1':
            xem_ho_so_ca_nhan(current_user)
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '2':
            doi_mat_khau(current_user['username'])
            # Đổi pass xong phải lấy lại dữ liệu mới nhất
            users = doc_users() 
            current_user = next(u for u in users if u['username'] == nhap_user)
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '3' and current_user['role'] == 'admin':
            them_tai_khoan()
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '4' and current_user['role'] == 'admin':
            clear_screen()
            print("=== DANH SÁCH TÀI KHOẢN ===")
            for u in doc_users():
                print(f"- {u['username']:<15} | Quyền: {u['role']:<10} | Tên: {u.get('ho_ten')}")
            input("\nNhấn Enter để tiếp tục...")
        elif chon == '0':
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ hoặc bạn không có quyền truy cập!")
            input("Nhấn Enter để thử lại...")