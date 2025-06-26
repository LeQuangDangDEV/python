# tính lương của từng người theo phòng ban, ai có ương cao nhất sẽ được làm giám đốc, ngoại trừ người có lương cao nhất ra 10 người lương cao nhất được làm quản lí, còn lại là nhân viên bình thường.
import pandas as pd
import numpy as np
from datetime import datetime

def tinh_tuoi(ngay_sinh):
    """Tính tuổi từ ngày sinh"""
    try:
        birth_date = pd.to_datetime(ngay_sinh)
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

def phan_loai_chuc_vu_10k():
    print("Đang đọc file dữ liệu 10,000 nhân viên...")
    
    # Đọc file CSV
    try:
        df = pd.read_csv('ds_nhan_vien.csv', encoding='utf-8')
    except:
        df = pd.read_csv('ds_nhan_vien.csv', encoding='latin-1')
    
    # Làm sạch tên cột
    df.columns = df.columns.str.strip()
    
    # Tính tuổi cho tất cả nhân viên
    df['Tuoi'] = df['Ngay sinh'].apply(tinh_tuoi)
    
    # Tạo cột chức vụ
    df['Chuc vu'] = 'Nhan vien'  # Mặc định là nhân viên
    
    # Lấy danh sách phòng ban
    phong_ban_list = df['Ten phong ban'].unique()
    
    print(f"Tổng số nhân viên: {len(df):,}")
    print(f"Số phòng ban: {len(phong_ban_list)}")
    print("\n" + "="*80)
    
    # Dictionary để lưu thông tin giám đốc và quản lý
    giam_doc_info = []
    quan_ly_info = []
    
    # Xử lý từng phòng ban
    for i, phong_ban in enumerate(phong_ban_list, 1):
        print(f"\n[{i}/{len(phong_ban_list)}] Đang xử lý phòng ban: {phong_ban}")
        
        # Lọc nhân viên thuộc phòng ban
        mask = df['Ten phong ban'] == phong_ban
        nv_indices = df[mask].index.tolist()
        
        # Sắp xếp theo lương giảm dần
        nv_sorted = df.loc[nv_indices].sort_values('Luong co ban', ascending=False)
        
        so_nv = len(nv_sorted)
        print(f"  Số nhân viên: {so_nv}")
        
        # Phân loại chức vụ
        for j, (idx, row) in enumerate(nv_sorted.iterrows()):
            if j == 0:  # Giám đốc
                df.loc[idx, 'Chuc vu'] = 'Giam doc'
                giam_doc_info.append({
                    'Phong ban': phong_ban,
                    'Ma NV': row['Ma nhan vien'],
                    'Ho ten': row['Ho ten nhan vien'],
                    'Tuoi': row['Tuoi'],
                    'Gioi tinh': row['Gioi tinh'],
                    'Luong': row['Luong co ban'],
                    'Ngay sinh': row['Ngay sinh']
                })
            elif j <= 10:  # 10 quản lý tiếp theo
                df.loc[idx, 'Chuc vu'] = 'Quan ly'
                quan_ly_info.append({
                    'Phong ban': phong_ban,
                    'Ma NV': row['Ma nhan vien'],
                    'Ho ten': row['Ho ten nhan vien'],
                    'Tuoi': row['Tuoi'],
                    'Gioi tinh': row['Gioi tinh'],
                    'Luong': row['Luong co ban'],
                    'Ngay sinh': row['Ngay sinh']
                })
        
        print(f"  ✓ Đã phân loại: 1 Giám đốc, {min(10, so_nv-1)} Quản lý, {max(0, so_nv-11)} Nhân viên")
    
    # Lưu file
    print(f"\n{'='*80}")
    print("Đang lưu file...")
    df.to_csv('ds_nhan_vien.csv', index=False, encoding='utf-8-sig')
    print("✓ Đã lưu file ds_nhan_vien.csv thành công!")
    
    # Hiển thị thống kê tổng quan
    print(f"\n{'='*80}")
    print("THỐNG KÊ TỔNG QUAN")
    print("="*80)
    
    thong_ke = df['Chuc vu'].value_counts()
    print(f"Tổng số Giám đốc: {thong_ke.get('Giam doc', 0):,}")
    print(f"Tổng số Quản lý: {thong_ke.get('Quan ly', 0):,}")
    print(f"Tổng số Nhân viên: {thong_ke.get('Nhan vien', 0):,}")
    
    # Hiển thị chi tiết Giám đốc
    print(f"\n{'='*80}")
    print("DANH SÁCH GIÁM ĐỐC THEO PHÒNG BAN")
    print("="*80)
    
    for gd in sorted(giam_doc_info, key=lambda x: x['Luong'], reverse=True):
        print(f"\n🏢 Phòng ban: {gd['Phong ban']}")
        print(f"   👤 Họ tên: {gd['Ho ten']} ({gd['Ma NV']})")
        print(f"   🎂 Tuổi: {gd['Tuoi']} ({gd['Gioi tinh']}) - Sinh: {gd['Ngay sinh']}")
        print(f"   💰 Lương: {gd['Luong']:,} VNĐ")
    
    # Hiển thị chi tiết Quản lý (nhóm theo phòng ban)
    print(f"\n{'='*80}")
    print("DANH SÁCH QUẢN LÝ THEO PHÒNG BAN")
    print("="*80)
    
    # Nhóm quản lý theo phòng ban
    quan_ly_by_dept = {}
    for ql in quan_ly_info:
        dept = ql['Phong ban']
        if dept not in quan_ly_by_dept:
            quan_ly_by_dept[dept] = []
        quan_ly_by_dept[dept].append(ql)
    
    for phong_ban in sorted(quan_ly_by_dept.keys()):
        print(f"\n🏢 Phòng ban: {phong_ban}")
        managers = sorted(quan_ly_by_dept[phong_ban], key=lambda x: x['Luong'], reverse=True)
        
        for i, ql in enumerate(managers, 1):
            print(f"   {i:2d}. {ql['Ho ten']} ({ql['Ma NV']})")
            print(f"       🎂 {ql['Tuoi']} tuổi ({ql['Gioi tinh']}) - 💰 {ql['Luong']:,} VNĐ")
    
    # Thống kê lương trung bình theo chức vụ
    print(f"\n{'='*80}")
    print("THỐNG KÊ LƯƠNG TRUNG BÌNH")
    print("="*80)
    
    luong_stats = df.groupby('Chuc vu')['Luong co ban'].agg(['count', 'mean', 'min', 'max'])
    for chuc_vu, stats in luong_stats.iterrows():
        if chuc_vu != 'Nhan vien':  # Không hiển thị nhân viên
            print(f"\n{chuc_vu.upper()}:")
            print(f"  Số lượng: {int(stats['count']):,} người")
            print(f"  Lương TB: {stats['mean']:,.0f} VNĐ")
            print(f"  Lương thấp nhất: {stats['min']:,.0f} VNĐ")
            print(f"  Lương cao nhất: {stats['max']:,.0f} VNĐ")
    
    print(f"\n{'='*80}")
    print("✅ HOÀN THÀNH XỬ LÝ 10,000 NHÂN VIÊN!")
    print("="*80)
    
    return df

# Chạy chương trình
if __name__ == "__main__":
    df_result = phan_loai_chuc_vu_10k()