# utils.py -  điều kiện của cảnh báo học vụ  và đuổi học 
from config import Config
from models import DataEngine

def evaluate_academic_warning(student_id, absences):
    """Điều kiện: vắng >=3 cảnh báo học tập, vắng >=5 cảnh báo nghỉ học"""
    ds_nguoi_hoc = DataEngine.read_file()
    nh = next((s for s in ds_nguoi_hoc if s['id'] == student_id), None)
    
    if not nh:
        return
        
    if absences >= 5:
        nh['canh_bao'] = "Cảnh báo nghỉ học"
    elif absences >= 4:
        nh['canh_bao'] = "Cảnh báo học tập"
    else:
        nh['canh_bao'] = "Không"
        
    DataEngine.write_file(ds_nguoi_hoc)