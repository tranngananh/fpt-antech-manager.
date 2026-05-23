# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from config import Config
from models import DataEngine, NguoiHocModel, DiemDanhModel, UserModel

app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo DB và tài khoản mặc định khi chạy lần đầu
DataEngine.initialize_db()
UserModel.initialize()


# ============================================================
# DECORATOR PHÂN QUYỀN
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash("⚠️ Vui lòng đăng nhập để tiếp tục!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash("⚠️ Vui lòng đăng nhập!", "warning")
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash("🚫 Chỉ Admin mới có quyền truy cập trang này!", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated


# Biến context mặc định truyền vào tất cả template
@app.context_processor
def inject_user():
    return {
        'current_user': session.get('user'),
        'current_role': session.get('role'),
        'current_hoten': session.get('ho_ten'),
    }


# ============================================================
# AUTH — Đăng nhập / Đăng xuất
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user     = UserModel.authenticate(username, password)

        if user:
            session['user']   = user['username']
            session['role']   = user['role']
            session['ho_ten'] = user.get('ho_ten', user['username'])
            flash(f"👋 Xin chào, {session['ho_ten']}!", "success")
            return redirect(url_for('dashboard'))

        flash("❌ Sai tên đăng nhập hoặc mật khẩu!", "danger")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("👋 Đã đăng xuất thành công!", "info")
    return redirect(url_for('login'))

# DASHBOARD
@app.route('/')
@login_required
def dashboard():
    data     = NguoiHocModel.get_all()
    total    = len(data)
    warnings = len([s for s in data if s.get('canh_bao') == 'Cảnh báo học tập'])
    expelled = len([s for s in data if s.get('canh_bao') == 'Cảnh báo nghỉ học'])
    ok       = total - warnings - expelled

    return render_template('dashboard.html',
                           total=total,
                           warnings=warnings,
                           expelled=expelled,
                           ok=ok)
# ============================================================
# XỬ LÝ ĐĂNG KÝ TÀI KHOẢN TỪ TRANG LOGIN
# ============================================================
@app.route('/register', methods=['POST'])
def register():
    username         = request.form.get('username', '').strip()
    password         = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    role             = request.form.get('role', 'nhanvien')
    ho_ten           = request.form.get('ho_ten', '').strip()
    email            = request.form.get('email', '').strip()        # ← thêm
    so_dien_thoai    = request.form.get('sdt', '').strip()          # ← thêm

    if password != confirm_password:
        flash("❌ Mật khẩu xác nhận không khớp!", "danger")
        return redirect(url_for('login'))

    success, msg = UserModel.create(
        username=username,
        password=password,
        role=role,
        ho_ten=ho_ten,
        email=email,                 # ← thêm
        so_dien_thoai=so_dien_thoai, # ← thêm
    )

    if success:
        flash("✅ Đăng ký thành công! Vui lòng đăng nhập.", "success")
    else:
        flash(msg, "danger")

    return redirect(url_for('login'))
# ============================================================
# STUDENTS — Danh sách, thêm, sửa
# Xóa chỉ dành cho Admin
# ============================================================
@app.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':
            form_data = {
                'ho_va_ten':     request.form.get('ho_va_ten', '').strip(),
                'so_dien_thoai': request.form.get('so_dien_thoai', '').strip(),
                'gioi_tinh':     request.form.get('gioi_tinh', '').strip(),
                'dan_toc':       request.form.get('dan_toc', 'Kinh').strip(),
                'ngay_sinh':     request.form.get('ngay_sinh', '').strip(),
                'email':         request.form.get('email', '').strip(),
                'khoa_hoc':      request.form.get('khoa_hoc', '').strip(),
                'lop_hoc':       request.form.get('lop_hoc', '').strip(),
                'dia_chi':       request.form.get('dia_chi', '').strip(),
            }
            success, msg = NguoiHocModel.create(form_data)
            flash(msg, 'success' if success else 'danger')

        elif action == 'update':
            student_id = request.form.get('id')
            form_data  = {
                'ho_va_ten':     request.form.get('ho_va_ten', '').strip(),
                'so_dien_thoai': request.form.get('so_dien_thoai', '').strip(),
                'gioi_tinh':     request.form.get('gioi_tinh', '').strip(),
                'dan_toc':       request.form.get('dan_toc', '').strip(),
                'ngay_sinh':     request.form.get('ngay_sinh', '').strip(),
                'email':         request.form.get('email', '').strip(),
                'khoa_hoc':      request.form.get('khoa_hoc', '').strip(),
                'lop_hoc':       request.form.get('lop_hoc', '').strip(),
                'dia_chi':       request.form.get('dia_chi', '').strip(),
            }
            success, msg = NguoiHocModel.update(student_id, form_data)
            flash(msg, 'success' if success else 'danger')

        return redirect(url_for('students'))

    # TÌM KIẾM HỌC VIÊN  (Tìm theo ID, Tên, SĐT, Email, Lớp, Khóa)
    data = NguoiHocModel.get_all()
    tu_khoa = request.args.get('tu_khoa', '').strip().lower()
    
    if tu_khoa:
        data_loc = []
        for s in data:
            # Chuẩn hóa toàn bộ dữ liệu của học viên về chữ thường và xóa khoảng trắng thừa
            s_id = str(s.get('id', '')).strip().lower()
            s_ten = str(s.get('ho_va_ten', '')).strip().lower()
            s_sdt = str(s.get('so_dien_thoai', '')).strip().lower()
            s_email = str(s.get('email', '')).strip().lower()
            s_khoa = str(s.get('khoa_hoc', '')).strip().lower()
            s_lop = str(s.get('lop_hoc', '')).strip().lower()
            
            # Kiểm tra xem từ khóa có nằm trong bất kỳ trường thông tin nào không
            if (tu_khoa in s_id or 
                tu_khoa in s_ten or 
                tu_khoa in s_sdt or 
                tu_khoa in s_email or 
                tu_khoa in s_khoa or 
                tu_khoa in s_lop):
                data_loc.append(s)
                
        data = data_loc # Gán lại danh sách đã lọc chính xác

    return render_template('students.html', students=data, tu_khoa=request.args.get('tu_khoa', ''))



@app.route('/delete-student/<string:student_id>')
@admin_required
def delete_student(student_id):
    _, msg = NguoiHocModel.delete(student_id)
    flash(msg, "warning")
    return redirect(url_for('students'))


# ============================================================
# ATTENDANCE — Bảng điểm danh
# Hàng = học viên, cột = ngày
# Tick = Có mặt, bỏ tick = Vắng
# Thêm / xóa cột ngày
# ============================================================
@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    ds_nguoi_hoc   = NguoiHocModel.get_all()
    diem_danh      = DiemDanhModel.get_all()
    danh_sach_ngay = DiemDanhModel.get_ngay_list()

    if request.method == 'POST':
        action = request.form.get('action')

        # --- Thêm cột ngày mới ---
        if action == 'add_day':
            ngay_moi = request.form.get('ngay_moi', '').strip()
            if not ngay_moi:
                flash("⚠️ Vui lòng nhập ngày!", "warning")
            else:
                success, msg = DiemDanhModel.add_day(ngay_moi, ds_nguoi_hoc)
                flash(msg, 'success' if success else 'warning')
            return redirect(url_for('attendance'))

        # --- Xóa cột ngày (chỉ admin) ---
        if action == 'delete_day':
            if session.get('role') != 'admin':
                flash("🚫 Chỉ Admin mới được xóa ngày!", "danger")
            else:
                ngay_xoa     = request.form.get('ngay_xoa', '').strip()
                success, msg = DiemDanhModel.delete_day(ngay_xoa)
                flash(msg, 'success' if success else 'danger')
            return redirect(url_for('attendance'))

        # --- Lưu điểm danh ---
        if action == 'save_attendance':
            # Cập nhật trạng thái từng ô trong bảng
            for ngay in danh_sach_ngay:
                records = diem_danh.get(ngay, [])
                for rec in records:
                    s_id = rec['id']
                    # Checkbox được tick → Có mặt, không tick → Vắng
                    checked      = request.form.get(f'dd_{ngay}_{s_id}')
                    rec['trang_thai'] = "Có mặt" if checked else "Vắng"

            DiemDanhModel.save_all(diem_danh)

            # Đồng bộ lại so_ngay_vang + canh_bao về nguoi_hoc.json
            DiemDanhModel.sync_to_nguoi_hoc()

            flash("✅ Đã lưu điểm danh và cập nhật cảnh báo học vụ!", "success")
            return redirect(url_for('attendance'))

    return render_template('attendance.html',
                           students=ds_nguoi_hoc,
                           diem_danh=diem_danh,
                           danh_sach_ngay=danh_sach_ngay)


# ============================================================
# WARNINGS — Danh sách cảnh báo
# ============================================================
@app.route('/warnings')
@login_required
def warnings():
    data         = NguoiHocModel.get_all()
    warning_list = [s for s in data if s.get('canh_bao') != 'Không']
    hoc_tap      = [s for s in warning_list if s.get('canh_bao') == 'Cảnh báo học tập']
    nghi_hoc     = [s for s in warning_list if s.get('canh_bao') == 'Cảnh báo nghỉ học']

    return render_template('warnings.html',
                           warning_list=warning_list,
                           hoc_tap=hoc_tap,
                           nghi_hoc=nghi_hoc)


# ============================================================
# REPORTS — Thống kê biểu đồ
# ============================================================
@app.route('/reports')
@login_required
def reports():
    data = NguoiHocModel.get_all()

    thong_ke_canh_bao  = {"Không": 0, "Cảnh báo học tập": 0, "Cảnh báo nghỉ học": 0}
    thong_ke_khoa_hoc  = {}
    thong_ke_gioi_tinh = {"Nam": 0, "Nữ": 0, "Khác": 0}

    for s in data:
        cb = s.get('canh_bao', 'Không')
        if cb in thong_ke_canh_bao:
            thong_ke_canh_bao[cb] += 1

        kh = s.get('khoa_hoc', 'Chưa xếp lớp')
        thong_ke_khoa_hoc[kh] = thong_ke_khoa_hoc.get(kh, 0) + 1

        gt = s.get('gioi_tinh', 'Khác')
        if gt in thong_ke_gioi_tinh:
            thong_ke_gioi_tinh[gt] += 1
        else:
            thong_ke_gioi_tinh['Khác'] += 1

    return render_template('reports.html',
                           students=data,
                           tk_canh_bao=thong_ke_canh_bao,
                           tk_khoa_hoc=thong_ke_khoa_hoc,
                           tk_gioi_tinh=thong_ke_gioi_tinh)


# ============================================================
# SETTINGS — Chỉ Admin
# ============================================================
# SETTINGS — Chỉ Admin
# Quản lý tài khoản + đổi mật khẩu
# ============================================================
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        return redirect(url_for('login'))

    current_username = session['user']
    users = UserModel._read()
    user_info = next((u for u in users if u['username'] == current_username), {})

    if request.method == 'POST':
        action = request.form.get('action', 'update_profile')

        # 1. CẬP NHẬT THÔNG TIN CÁ NHÂN
        if action == 'update_profile':
            ho_ten_moi  = request.form.get('ho_ten', '').strip()
            email_moi   = request.form.get('email', '').strip()
            sdt_moi     = request.form.get('so_dien_thoai', '').strip()
            dia_chi_moi = request.form.get('dia_chi', '').strip()
            mk_moi      = request.form.get('new_password', '').strip()

            for u in users:
                if u['username'] == current_username:
                    u['ho_ten']        = ho_ten_moi
                    u['email']         = email_moi
                    u['so_dien_thoai'] = sdt_moi
                    u['dia_chi']       = dia_chi_moi
                    if mk_moi:
                        u['password'] = UserModel._hash(mk_moi)
                    session['ho_ten'] = ho_ten_moi
                    break
            UserModel._save(users)
            flash("✅ Cập nhật thông tin cá nhân thành công!", "success")

        # 2. TỰ XÓA TÀI KHOẢN
        elif action == 'delete_self':
            if current_username == 'admin':
                flash("❌ Tài khoản Admin gốc không thể tự xóa!", "danger")
            else:
                filtered = [u for u in users if u['username'] != current_username]  # ← filtered
                UserModel._save(filtered)
                session.clear()
                flash("✅ Tài khoản của bạn đã được xóa!", "success")
                return redirect(url_for('login'))

        # 3. ADMIN THÊM TÀI KHOẢN MỚI
        elif action == 'add_user':
            if session.get('role') != 'admin':
                flash("❌ Bạn không có quyền!", "danger")
            else:
                new_username = request.form.get('username', '').strip()
                new_password = request.form.get('password', '').strip()
                new_role     = request.form.get('role', 'nhanvien')
                new_hoten    = request.form.get('ho_ten', '').strip()
                new_email    = request.form.get('email', '').strip()
                new_sdt      = request.form.get('so_dien_thoai', '').strip()
                new_diachi   = request.form.get('dia_chi', '').strip()

                if any(u['username'] == new_username for u in users):
                    flash("❌ Tên đăng nhập đã tồn tại!", "danger")
                else:
                    users.append({
                        "username":      new_username,
                        "password":      UserModel._hash(new_password),
                        "role":          new_role,
                        "ho_ten":        new_hoten,
                        "email":         new_email,
                        "so_dien_thoai": new_sdt,
                        "dia_chi":       new_diachi,
                    })
                    UserModel._save(users)
                    flash(f"✅ Đã thêm tài khoản [{new_username}]!", "success")

        # 4. ADMIN XÓA TÀI KHOẢN KHÁC
        elif action == 'delete_user':
            if session.get('role') != 'admin':
                flash("❌ Bạn không có quyền!", "danger")
            else:
                del_username = request.form.get('del_username')
                if del_username == 'admin':
                    flash("❌ Không thể xóa tài khoản Admin gốc!", "danger")
                elif del_username == current_username:
                    flash("❌ Dùng nút Xóa tài khoản của tôi!", "danger")
                else:
                    filtered = [u for u in users if u['username'] != del_username]  # ← filtered
                    UserModel._save(filtered)
                    flash(f"✅ Đã xóa tài khoản [{del_username}]!", "success")

        # 5. ADMIN RESET MẬT KHẨU
        elif action == 'reset_password':
            if session.get('role') != 'admin':
                flash("❌ Bạn không có quyền!", "danger")
            else:
                target_username = request.form.get('target_username', '').strip()
                new_pass        = request.form.get('new_pass', '').strip()
                if not new_pass:
                    flash("⚠️ Mật khẩu mới không được để trống!", "danger")
                else:
                    for u in users:
                        if u['username'] == target_username:
                            u['password'] = UserModel._hash(new_pass)
                            break
                    UserModel._save(users)
                    flash(f"✅ Đã reset mật khẩu cho [{target_username}]!", "success")

        return redirect(url_for('settings'))

    return render_template('settings.html', all_users=users, user_info=user_info)
    return render_template('settings.html', all_users=users, user_info=user_info)
if __name__ == '__main__':
    app.run(debug=True)