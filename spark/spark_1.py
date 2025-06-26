import pandas as pd
from datetime import datetime, date

def process_employee_data(file_name):
 
    try:
        # Đọc file CSV
        df = pd.read_csv(file_name)
        
        # Chuyển đổi cột ngày sinh thành datetime
        df['Ngay sinh'] = pd.to_datetime(df['Ngay sinh'])
        
        # Tính tuổi
        today = date.today()
        df['Tuoi'] = df['Ngay sinh'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)))
        
        # Tăng 15% lương cho nhân viên trên 30 tuổi
        mask_over_30 = df['Tuoi'] > 30
        df.loc[mask_over_30, 'Luong moi'] = df.loc[mask_over_30, 'Luong co ban'] * 1.15
        df.loc[~mask_over_30, 'Luong moi'] = df['Luong co ban']
        
        # Làm tròn lương mới
        df['Luong moi'] = df['Luong moi'].round().astype(int)
        
        # Cập nhật ghi chú
        df['Ghi chu'] = df['Tuoi'].apply(lambda x: 'Tăng lương 15%' if x > 30 else 'Không tăng lương')
        
        return df
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {file_name}")
        return None
    except Exception as e:
        print(f"Lỗi xử lý: {str(e)}")
        return None

def display_results(df):
    """
    Hiển thị kết quả xử lý
    """
    if df is None:
        return
    
    print("=" * 100)
    print("DANH SÁCH NHÂN VIÊN SAU KHI XỬ LÝ LƯƠNG")
    print("=" * 100)
    
    # Thông tin tổng quan
    total_employees = len(df)
    employees_over_30 = len(df[df['Tuoi'] > 30])
    employees_30_or_under = total_employees - employees_over_30
    
    print(f"Tổng số nhân viên: {total_employees:,}")
    print(f"Nhân viên trên 30 tuổi (được tăng lương): {employees_over_30:,}")
    print(f"Nhân viên 30 tuổi trở xuống: {employees_30_or_under:,}")
    print()
    
    # Hiển thị danh sách chi tiết
    print("CHI TIẾT NHÂN VIÊN ĐƯỢC TĂNG LƯƠNG:")
    print("=" * 100)
    print(f"{'STT':<5} {'Mã NV':<10} {'Họ tên':<25} {'Phòng ban':<12} {'Tuổi':<5} {'Lương cũ':<15} {'Lương mới':<15} {'Ghi chú':<15}")
    print("-" * 100)
    
    over_30_df = df[df['Tuoi'] > 30]
    for index, row in over_30_df.iterrows():
        print(f"{index+1:<5} {row['Ma nhan vien']:<10} {row['Ho ten nhan vien']:<25} "
              f"{row['Ten phong ban']:<12} {row['Tuoi']:<5} "
              f"{row['Luong co ban']:,}VND{'':<5} "
              f"{row['Luong moi']:,}VND{'':<5} "
              f"{row['Ghi chu']:<15}")
        
        # Thêm dòng ngắt sau mỗi 50 nhân viên
        if (index + 1) % 50 == 0:
            print("-" * 100)
    
    print("=" * 100)
    
    # Thống kê theo phòng ban
    print("\nTHỐNG KÊ THEO PHÒNG BAN:")
    print("=" * 80)
    
    dept_stats = df.groupby('Ten phong ban').agg({
        'Ma nhan vien': 'count',
        'Tuoi': 'mean',
        'Luong co ban': 'mean',
        'Luong moi': 'mean',
        'Tuoi': lambda x: (x > 30).sum()  # Đếm số nhân viên trên 30 tuổi
    }).round(2)
    dept_stats.columns = ['Số NV', 'Tuổi TB', 'Lương cũ TB', 'Lương mới TB', 'NV >30 tuổi']
    
    print(f"{'Phòng ban':<15} {'Số NV':<8} {'Tuổi TB':<8} {'Lương cũ TB':<15} {'Lương mới TB':<15} {'NV >30 tuổi':<10}")
    print("-" * 80)
    
    for dept, stats in dept_stats.iterrows():
        print(f"{dept:<15} {int(stats['Số NV']):<8} {stats['Tuổi TB']:<8.1f} "
              f"{stats['Lương cũ TB']:,.0f}VND{'':<5} {stats['Lương mới TB']:,.0f}VND{'':<5} "
              f"{int(stats['NV >30 tuổi']):<10}")
    
    print("=" * 80)

def save_results(df, output_file):
    """
    Lưu kết quả vào file CSV gốc
    """
    if df is None:
        return
    try:
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nĐã lưu kết quả vào file: {output_file}")
    except Exception as e:
        print(f"Lỗi khi lưu file: {str(e)}")

# Chạy chương trình chính
if __name__ == "__main__":
    csv_file_name = "ds_nhan_vien.csv"
    
    # Xử lý dữ liệu
    df_processed = process_employee_data(csv_file_name)
    
    # Hiển thị kết quả
    display_results(df_processed)
    
    # Lưu kết quả vào file gốc
    save_results(df_processed, csv_file_name)