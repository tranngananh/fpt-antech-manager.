# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fpt_antech_secret_key_123'
    DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    
    # Định nghĩa tên file bằng tiếng Việt đồng bộ
    NGUOI_HOC_FILE = os.path.join(DATA_DIR, 'nguoi_hoc.json')
    DIEM_DANH_FILE = os.path.join(DATA_DIR, 'diem_danh.json')
    CANH_BAO_FILE = os.path.join(DATA_DIR, 'canh_bao.json')
    KHOA_HOC_FILE = os.path.join(DATA_DIR, 'khoa_hoc.json')