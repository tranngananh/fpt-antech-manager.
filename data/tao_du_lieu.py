import json 
# 1. Dữ liệu gốc (Đã thay toàn bộ warning -> canh_bao, attendance -> diem_danh)
raw_data = [ 
    { "id": "001", "ho_va_ten": "Nguyễn Văn A", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "15/04/2003", "so_dien_thoai": "0987654001", "email": "nguyenvana01@gmail.com", "dia_chi": "144 Xuân Thủy, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "002", "ho_va_ten": "Trần Thị B", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "22/09/2004", "so_dien_thoai": "0987654002","email": "tranthib02@gmail.com", "dia_chi": "1 Đại Cồ Việt, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 9 },
  { "id": "003", "ho_va_ten": "Bùi Văn C", "dan_toc": "Mường", "gioi_tinh": "Nam", "ngay_sinh": "11/01/2002", "so_dien_thoai": "0987654003","email": "buivanc03@gmail.com", "dia_chi": "207 Giải Phóng, Hà Nội", "canh_bao": "Cảnh báo nghỉ học", "khoa_hoc": "back-end", "diem_danh": 3 },
  { "id": "004", "ho_va_ten": "Đặng Thị D", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "05/06/2005", "so_dien_thoai": "0987654004","email": "dangthid04@gmail.com", "dia_chi": "91 Chùa Láng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "game", "diem_danh": 10 },
  { "id": "005", "ho_va_ten": "Bùi Văn E", "dan_toc": "Tày", "gioi_tinh": "Nam", "ngay_sinh": "30/10/2001", "so_dien_thoai": "0987654005","email": "buivane05@gmail.com", "dia_chi": "1 Tôn Thất Tùng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 7 },
  { "id": "006", "ho_va_ten": "Mạc Thị F", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "14/02/2003", "so_dien_thoai": "0987654006","email": "macthif06@gmail.com", "dia_chi": "Km 9, Nguyễn Trãi, Hà Nội", "canh_bao": "Cảnh báo học tập", "khoa_hoc": "full-stack", "diem_danh": 4 },
  { "id": "007", "ho_va_ten": "Vũ Văn G", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "19/08/2004","so_dien_thoai": "0987654007", "email": "vuvang07@gmail.com", "dia_chi": "69 Chùa Láng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "008", "ho_va_ten": "Đỗ Thị H", "dan_toc": "Dao", "gioi_tinh": "Nữ", "ngay_sinh": "25/12/2002","so_dien_thoai": "0987654008", "email": "dothih08@gmail.com", "dia_chi": "79 Hồ Tùng Mậu, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 9 },
  { "id": "009", "ho_va_ten": "Đào Văn I", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "03/07/2005", "so_dien_thoai": "0987654009","email": "daovani09@gmail.com", "dia_chi": "55 Giải Phóng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "game", "diem_danh": 6 },
  { "id": "010", "ho_va_ten": "Nguyễn Thị J", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "18/11/2001","so_dien_thoai": "0987654010", "email": "nguyenthij10@gmail.com", "dia_chi": "87 Nguyễn Chí Thanh, Hà Nội", "canh_bao": "Cảnh báo nghỉ học", "khoa_hoc": "full-stack", "diem_danh": 2 },
  { "id": "011", "ho_va_ten": "Phạm Văn K", "dan_toc": "Thái", "gioi_tinh": "Nam", "ngay_sinh": "09/03/2004", "so_dien_thoai": "0987654011","email": "phamvank11@gmail.com", "dia_chi": "175 Tây Sơn, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "012", "ho_va_ten": "Trịnh Thị L", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "27/05/2003", "so_dien_thoai": "0987654012","email": "trinhtil12@gmail.com", "dia_chi": "175 Tây Sơn, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 10 },
  { "id": "013", "ho_va_ten": "Bùi Văn M", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "14/10/2002", "so_dien_thoai": "0987654013","email": "buivanm13@gmail.com", "dia_chi": "456 Lĩnh Nam, Hà Nội", "canh_bao": "Không", "khoa_hoc": "game", "diem_danh": 7 },
  { "id": "014", "ho_va_ten": "Đỗ Thị N", "dan_toc": "Mường", "gioi_tinh": "Nữ", "ngay_sinh": "02/12/2005", "so_dien_thoai": "0987654014","email": "dothin14@gmail.com", "dia_chi": "54 P.Triều Khúc, Hà Nội", "canh_bao": "Cảnh báo học tập", "khoa_hoc": "back-end", "diem_danh": 4 },
  { "id": "015", "ho_va_ten": "Đinh Văn O", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "21/01/2004","so_dien_thoai": "0987654015", "email": "dinhvano15@gmail.com", "dia_chi": "35 Phạm Văn Đồng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 9 },
  { "id": "016", "ho_va_ten": "Nguyễn Trần Thanh Ngân", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "19/06/2005", "so_dien_thoai": "0987654016","email": "tranngananh11963hd@gmail.com", "dia_chi": "901 Giải Phóng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 8 },
  { "id": "017", "ho_va_ten": "Nguyễn Thị Thu Nga", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "15/08/2006", "so_dien_thoai": "0987654017","email": "ThuNga2006@gmail.com", "dia_chi": "39 Hồ Tùng Mậu, Hà Nội", "canh_bao": "Không", "khoa_hoc": "game", "diem_danh": 9 },
  { "id": "018", "ho_va_ten": "Nguyễn Bùi Hải Nam", "dan_toc": "Tày", "gioi_tinh": "Nam", "ngay_sinh": "25/01/2006", "so_dien_thoai": "0987654018","email": "hainamnguyen250106@gmail.com", "dia_chi": "Cầu Vĩnh Tuy, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 7 },
  { "id": "019", "ho_va_ten": "Ngô Thị Thảo Ngân", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "04/06/2004","so_dien_thoai": "0987654019", "email": "thaonganngo0406@gmail.com", "dia_chi": "35 Cầu Diễn, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 10 },
  { "id": "020", "ho_va_ten": "Đặng Trịnh Minh Ngọc", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "09/08/2006", "so_dien_thoai": "0987654020","email": "minhngoc090806@gmail.com", "dia_chi": "35 Mỹ Đình, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "021", "ho_va_ten": "Nguyễn Quốc Huy", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "12/03/2001", "so_dien_thoai": "0987654021","email": "huynguyen.quoc01@gmail.com", "dia_chi": "45 Phan Chu Trinh, Hoàn Kiếm, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 9 },
  { "id": "022", "ho_va_ten": "Trần Thu Trang", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "21/09/2003", "so_dien_thoai": "0987654022","email": "trangtran.thu2003@gmail.com", "dia_chi": "67 Lê Duẩn, Hải Châu, Đà Nẵng", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 10 },
  { "id": "023", "ho_va_ten": "Phạm Văn Khánh", "dan_toc": "Mường", "gioi_tinh": "Nam", "ngay_sinh": "05/12/2002","so_dien_thoai": "0987654023", "email": "khanhpham.van98@gmail.com", "dia_chi": "89 Trần Phú, Nha Trang, Khánh Hòa", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "024", "ho_va_ten": "Lê Hoàng Anh", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "18/07/2000","so_dien_thoai": "0987654024", "email": "anhle.hoang2000@gmail.com", "dia_chi": "14 Nguyễn Thái Học, Quy Nhơn, Bình Định", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 7 },
  { "id": "025", "ho_va_ten": "Đỗ Minh Châu", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "26/10/2004","so_dien_thoai": "0987654025", "email": "chaudo.minh2004@gmail.com", "dia_chi": "72 Lý Thường Kiệt, TP. Thái Bình", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 9 },
  { "id": "026", "ho_va_ten": "Vũ Đức Thành", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "09/02/2005", "so_dien_thoai": "0987654026","email": "thanhvu.duc99@gmail.com", "dia_chi": "33 Hồng Bàng, TP. Hải Phòng", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "027", "ho_va_ten": "Ngô Thanh Tùng", "dan_toc": "Thái", "gioi_tinh": "Nam", "ngay_sinh": "14/05/2002", "so_dien_thoai": "0987654027","email": "tungngo.thanh2002@gmail.com", "dia_chi": "58 Điện Biên Phủ, Ba Đình, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 7 },
  { "id": "028", "ho_va_ten": "Bùi Thị Phương", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "30/08/2003", "so_dien_thoai": "0987654028","email": "phuongbui.thi03@gmail.com", "dia_chi": "91 Nguyễn Huệ, TP. Huế", "canh_bao": "Cảnh báo nghỉ học", "khoa_hoc": "front-end", "diem_danh": 2 },
  { "id": "029", "ho_va_ten": "Hoàng Gia Bảo", "dan_toc": "Tày", "gioi_tinh": "Nam", "ngay_sinh": "11/11/2001", "so_dien_thoai": "0987654029","email": "baohoang.gia2001@gmail.com", "dia_chi": "120 Lê Lợi, TP. Thanh Hóa", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "030", "ho_va_ten": "Đặng Văn Phúc", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "07/04/2005", "so_dien_thoai": "0987654030","email": "phucdang.van2005@gmail.com", "dia_chi": "28 Nguyễn Văn Cừ, Long Biên, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 9 },
  { "id": "031", "ho_va_ten": "Nguyễn Thu Nga", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "18/02/2006","so_dien_thoai": "0987654031", "email": "Ngango1234@gmail.com", "dia_chi": "15 Lý Thái Tổ, Bắc Ninh", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 10 },
  { "id": "032", "ho_va_ten": "Trần Minh Đức", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "05/11/2003", "so_dien_thoai": "0987654032","email": "ductran.minh99@gmail.com", "dia_chi": "234 Trần Đại Nghĩa, Hai Bà Trưng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "033", "ho_va_ten": "Lê Thùy Linh", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "14/08/2002", "so_dien_thoai": "0987654033","email": "linhle.thuy2002@gmail.com", "dia_chi": "88 Nguyễn Văn Cừ, Quận 5, TP. Hồ Chí Minh", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 9 },
  { "id": "034", "ho_va_ten": "Phạm Hoàng Long", "dan_toc": "Dao", "gioi_tinh": "Nam", "ngay_sinh": "22/03/2001","so_dien_thoai": "0987654034", "email": "longpham.hoang@gmail.com", "dia_chi": "12 Lạch Tray, Ngô Quyền, Hải Phòng", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 7 },
  { "id": "035", "ho_va_ten": "Vũ Thị Mai", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "30/07/2004", "so_dien_thoai": "0987654035","email": "maivu.thi2004@gmail.com", "dia_chi": "45 Lê Lợi, TP. Vinh, Nghệ An", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 9 },
  { "id": "036", "ho_va_ten": "Hoàng Văn Nam", "dan_toc": "Nùng", "gioi_tinh": "Nam", "ngay_sinh": "12/01/2000", "so_dien_thoai": "0987654036","email": "namhoang.van@gmail.com", "dia_chi": "102 Hùng Vương, TP. Thanh Hóa", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "037", "ho_va_ten": "Đỗ Thúy Quỳnh", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "19/09/2003", "so_dien_thoai": "0987654037","email": "quynhdo.thuy03@gmail.com", "dia_chi": "19 Nguyễn Văn Linh, Hải Châu, Đà Nẵng", "canh_bao": "Cảnh báo học tập", "khoa_hoc": "front-end", "diem_danh": 4 },
  { "id": "038", "ho_va_ten": "Ngô Tiến Đạt", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "25/12/2004", "so_dien_thoai": "0987654038","email": "datngo.tien98@gmail.com", "dia_chi": "56 Quang Trung, Hà Đông, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "039", "ho_va_ten": "Bùi Minh Tú", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "08/04/2005", "so_dien_thoai": "0987654039","email": "tubui.minh2005@gmail.com", "dia_chi": "77 Nguyễn Huệ, Quận 1, TP. Hồ Chí Minh", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 7 },
  { "id": "040", "ho_va_ten": "Đặng Hồng Hạnh", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "03/06/2002", "so_dien_thoai": "0987654040","email": "hanhdang.hong02@gmail.com", "dia_chi": "31 Hùng Vương, TP. Huế", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 9 },
  { "id": "041", "ho_va_ten": "Phùng Thanh Độ", "dan_toc": "Tày", "gioi_tinh": "Nam", "ngay_sinh": "12/09/2001", "so_dien_thoai": "0987654041","email": "doly1989@gmail.com", "dia_chi": "120 Yên Lãng, Đống Đa, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "042", "ho_va_ten": "Nguyễn Minh Khánh", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "03/04/2002","so_dien_thoai": "0987654042", "email": "khanhminh1992@gmail.com", "dia_chi": "45 Trần Duy Hưng, Cầu Giấy, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 9 },
  { "id": "043", "ho_va_ten": "Trần Thu Hà", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "21/07/2003", "so_dien_thoai": "0987654043","email": "hathu1995@gmail.com", "dia_chi": "18 Nguyễn Trãi, Thanh Xuân, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 10 },
  { "id": "044", "ho_va_ten": "Lê Quốc Bảo", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "14/11/2000", "so_dien_thoai": "0987654044","email": "baoquoc1990@gmail.com", "dia_chi": "72 Lê Văn Lương, Thanh Xuân, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 8 },
  { "id": "045", "ho_va_ten": "Phạm Gia Hưng", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "30/01/2004", "so_dien_thoai": "0987654045", "email": "hungpham1998@gmail.com", "dia_chi": "9 Kim Mã, Ba Đình, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 7 },
  { "id": "046", "ho_va_ten": "Đỗ Ngọc Anh", "dan_toc": "Dao", "gioi_tinh": "Nữ", "ngay_sinh": "17/06/2001", "so_dien_thoai": "0987654046","email": "ngocanhdo1993@gmail.com", "dia_chi": "56 Hoàng Quốc Việt, Cầu Giấy, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 9 },
  { "id": "047", "ho_va_ten": "Vũ Thanh Tùng", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "25/08/2003","so_dien_thoai": "0987654047", "email": "tungvu1987@gmail.com", "dia_chi": "101 Nguyễn Chí Thanh, Đống Đa, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "048", "ho_va_ten": "Bùi Hải Yến", "dan_toc": "Mường", "gioi_tinh": "Nữ", "ngay_sinh": "08/12/2002", "so_dien_thoai": "0987654048", "email": "yenbui1996@gmail.com", "dia_chi": "34 Phạm Văn Đồng, Bắc Từ Liêm, Hà Nội", "canh_bao": "Cảnh báo học tập", "khoa_hoc": "front-end", "diem_danh": 4 },
  { "id": "049", "ho_va_ten": "Hoàng Đức Mạnh", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "11/03/2005", "so_dien_thoai": "0987654049","email": "manhhoang1991@gmail.com", "dia_chi": "67 Tây Sơn, Đống Đa, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 9 },
  { "id": "050", "ho_va_ten": "Nguyễn Thị Lan Anh", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "19/10/2000","so_dien_thoai": "0987654050","email": "lananh2000@gmail.com", "dia_chi": "22 Xuân Thủy, Cầu Giấy, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "051", "ho_va_ten": "Kim Thu Nga", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "21/03/2006", "so_dien_thoai": "0987654052","email": "Thnga213@gmail.com", "dia_chi": "7 Kinh Bắc, Bắc Ninh", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 10 },
  { "id": "052", "ho_va_ten": "Nguyễn Hải Nam", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "13/06/2006","so_dien_thoai": "0987654053", "email": "Namngoknghek77@gmail.com", "dia_chi": "19 Cẩm Phả, Hạ Long", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "053", "ho_va_ten": "Trần Thanh Ngân", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "07/08/2006", "so_dien_thoai": "0987654054","email": "Nganduong112@gmail.com", "dia_chi": "67 Thuỷ Nguyên, Hải Phòng", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 9 },
  { "id": "054", "ho_va_ten": "Nguyễn Văn An", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "12/03/2004", "so_dien_thoai": "0987654055","email": "nguyenvanan01@gmail.com", "dia_chi": "12 Chùa Bộc, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 8 },
  { "id": "055", "ho_va_ten": "Lê Thị Mai", "dan_toc": "Thái", "gioi_tinh": "Nữ", "ngay_sinh": "25/07/2005", "so_dien_thoai": "0987654056","email": "lethimai03@gmail.com", "dia_chi": "45 Nguyễn Trãi, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 10 },
  { "id": "056", "ho_va_ten": "Phạm Quốc Huy", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "08/11/2003", "so_dien_thoai": "0987654057","email": "phamquochuy99@gmail.com", "dia_chi": "8 Tây Sơn, Đống Đa, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 7 },
  { "id": "057", "ho_va_ten": "Đỗ Minh Trang", "dan_toc": "Kinh", "gioi_tinh": "Nữ", "ngay_sinh": "19/01/2004", "so_dien_thoai": "0987654058","email": "dominhtrang@gmail.com", "dia_chi": "77 Giải Phóng, Hà Nội", "canh_bao": "Không", "khoa_hoc": "front-end", "diem_danh": 9 },
  { "id": "058", "ho_va_ten": "Hoàng Cửu Bảo", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "30/09/2005","so_dien_thoai": "0987654059", "email": "hoanggiabao02@gmail.com", "dia_chi": "21 Lê Thanh Nghị, Hà Nội", "canh_bao": "Không", "khoa_hoc": "back-end", "diem_danh": 8 },
  { "id": "059", "ho_va_ten": "Vũ Khánh Linh", "dan_toc": "Tày", "gioi_tinh": "Nữ", "ngay_sinh": "14/02/2004", "so_dien_thoai": "0987654060","email": "vukhanhlinh04@gmail.com", "dia_chi": "56 Cầu Giấy, Hà Nội", "canh_bao": "Không", "khoa_hoc": "full-stack", "diem_danh": 9 },
  { "id": "060", "ho_va_ten": "Trịnh Đức Nam", "dan_toc": "Kinh", "gioi_tinh": "Nam", "ngay_sinh": "06/06/2005", "so_dien_thoai": "0987654061","email": "trinhducnam05@gmail.com", "dia_chi": "90 Phạm Hùng, Hà Nội", "canh_bao": "Cảnh báo nghỉ học", "khoa_hoc": "front-end", "diem_danh": 2 }
  
]

nguoi_hoc = []
khoa_hoc = []
diem_danh_list = []
canh_bao_list = []

# Đổi lại thành TONG_SO_NGAY = 10 cho đúng ý bạn
TONG_SO_NGAY = 10

# 2. Xử lý chia tách dữ liệu
for item in raw_data:
    # --- File Học Viên ---
    nguoi_hoc.append({
        "id": item["id"],
        "ho_va_ten": item["ho_va_ten"],
        "dan_toc": item["dan_toc"],
        "gioi_tinh": item["gioi_tinh"],
        "ngay_sinh": item["ngay_sinh"],
        "email": item["email"],
        "dia_chi": item["dia_chi"],
        "khoa_hoc": item["khoa_hoc"], 
        "so_ngay_vang": TONG_SO_NGAY - item["diem_danh"],
        "so_dien_thoai": item["so_dien_thoai"]
    })
    
    # --- File Khóa Học ---
    khoa_hoc.append({
        "id": item["id"],
        "khoa_hoc": item["khoa_hoc"]
    })
    
    #  File Điểm Danh (Đã sửa từ vựng) 
    so_ngay_di_hoc = item["diem_danh"]
    so_ngay_vang = TONG_SO_NGAY - so_ngay_di_hoc
    
    diem_danh_list.append({
        "id": item["id"],
        "ho_va_ten":item["ho_va_ten"],
        "diem_danh": so_ngay_di_hoc,
        "so_ngay_vang": so_ngay_vang
    })
    
    # --- File Cảnh Báo (Đã sửa từ vựng) ---
    canh_bao_list.append({
        "id": item["id"],
        "ho_va_ten":item["ho_va_ten"],
        "canh_bao": item["canh_bao"]
    })

# 3. Lưu ra file JSON
def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_json('data/nguoi_hoc.json', nguoi_hoc)
save_json('data/khoa_hoc.json', khoa_hoc)
save_json('data/diem_danh.json', diem_danh_list)
save_json('data/canh_bao.json', canh_bao_list)

print(" dữ liệu được tạo thành công")