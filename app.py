# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import DataEngine, NguoiHocModel

app = Flask(__name__)
app.config.from_object(Config)

DataEngine.initialize_db()

@app.route('/')
def dashboard():
    data = NguoiHocModel.get_all()
    total = len(data)
    warnings = len([s for s in data if s.get('canh_bao') in ['Cảnh báo học tập', 'Cảnh báo']])
    expelled = len([s for s in data if s.get('canh_bao') in ['Cảnh báo nghỉ học', 'Đuổi học']])
    return render_template('dashboard.html', total=total, warnings=warnings, expelled=expelled)

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            form_data = {
                'ho_va_ten': request.form.get('ho_va_ten'),
                'so_dien_thoai': request.form.get('so_dien_thoai'),
                'gioi_tinh': request.form.get('gioi_tinh'),
                'dan_toc': request.form.get('dan_toc'),
                'ngay_sinh': request.form.get('ngay_sinh'),
                'email': request.form.get('email'),
                'khoa_hoc': request.form.get('khoa_hoc'),
                'dia_chi': request.form.get('dia_chi')
            }
            success, msg = NguoiHocModel.create(form_data)
            flash(msg, 'success' if success else 'danger')
            
        elif action == 'update':
            student_id = request.form.get('id')
            form_data = {
                'ho_va_ten': request.form.get('ho_va_ten'),
                'so_dien_thoai': request.form.get('so_dien_thoai'),
                'gioi_tinh': request.form.get('gioi_tinh'),
                'dan_toc': request.form.get('dan_toc'),
                'ngay_sinh': request.form.get('ngay_sinh'),
                'email': request.form.get('email'),
                'khoa_hoc': request.form.get('khoa_hoc'),
                'dia_chi': request.form.get('dia_chi')
            }
            success, msg = NguoiHocModel.update(student_id, form_data)
            flash(msg, 'success' if success else 'danger')
            
        return redirect(url_for('students'))

    # Lọc tìm kiếm người học
    data = NguoiHocModel.get_all()
    tu_khoa = request.args.get('tu_khoa', '').strip().lower()
    if tu_khoa:
        data = [
            s for s in data if
            tu_khoa in s.get('id', '').lower() or
            tu_khoa in s.get('ho_va_ten', '').lower() or
            tu_khoa in s.get('so_dien_thoai', '').lower() or
            tu_khoa in s.get('email', '').lower() or
            tu_khoa in s.get('khoa_hoc', '').lower()
        ]

    return render_template('students.html', students=data, tu_khoa=tu_khoa)

@app.route('/delete-student/<string:student_id>')
def delete_student(student_id):
    NguoiHocModel.delete(student_id)
    flash("🗑️ Đã xóa thông tin người học hoàn toàn khỏi hệ thống!", "warning")
    return redirect(url_for('students'))

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        ds_nguoi_hoc = DataEngine.read_file()
        for nh in ds_nguoi_hoc:
            s_id = nh['id']
            input_val = request.form.get(f'absent_{s_id}')
            if input_val is not None and input_val.strip() != '':
                new_absent = int(input_val)
                nh['diem_danh'] = new_absent
                
                # Tự động đồng bộ hóa trạng thái học vụ dựa trên số buổi vắng
                if new_absent >= 5:
                    nh['canh_bao'] = "Cảnh báo nghỉ học"
                elif new_absent >= 3:
                    nh['canh_bao'] = "Cảnh báo học tập"
                else:
                    nh['canh_bao'] = "Không"
                
        DataEngine.write_file(ds_nguoi_hoc)
        flash("⏱️ Đã chốt sổ điểm danh và đồng bộ tự động hệ thống cảnh báo học vụ!", "success")
        return redirect(url_for('attendance'))
        
    data = NguoiHocModel.get_all()
    return render_template('attendance.html', students=data)

@app.route('/warnings')
def warnings():
    data = NguoiHocModel.get_all()
    warning_list = [s for s in data if s.get('canh_bao') in ['Cảnh báo học tập', 'Cảnh báo nghỉ học', 'Cảnh báo', 'Đuổi học']]
    return render_template('warnings.html', students=warning_list)

@app.route('/reports')
def reports():
    data = NguoiHocModel.get_all()
    
    # Đếm chính xác số liệu để vẽ biểu đồ
    thong_ke_canh_bao = {"Không": 0, "Cảnh báo học tập": 0, "Cảnh báo nghỉ học": 0}
    thong_ke_khoa_hoc = {}
    thong_ke_gioi_tinh = {"Nam": 0, "Nữ": 0}

    for s in data:
        cb = s.get('canh_bao', 'Không')
        if cb in thong_ke_canh_bao:
            thong_ke_canh_bao[cb] += 1
            
        kh = s.get('khoa_hoc', 'Chưa xếp lớp')
        thong_ke_khoa_hoc[kh] = thong_ke_khoa_hoc.get(kh, 0) + 1
        
        gt = s.get('gioi_tinh', 'Khác')
        if gt in thong_ke_gioi_tinh:
            thong_ke_gioi_tinh[gt] += 1

    return render_template('reports.html', 
                           students=data, 
                           tk_canh_bao=thong_ke_canh_bao, 
                           tk_khoa_hoc=thong_ke_khoa_hoc, 
                           tk_gioi_tinh=thong_ke_gioi_tinh)

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)