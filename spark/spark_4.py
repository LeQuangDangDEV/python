# tìm 50 nhân viên có lương thấp nhất mỗi phòng ban và sai thải
import pandas as pd

# Đọc file CSV
df = pd.read_csv('ds_nhan_vien.csv')

# Nhóm theo phòng ban và lấy 50 người có lương cơ bản thấp nhất mỗi phòng
def get_lowest_salary_employees(group, n=50):
    return group.nsmallest(n, 'Luong co ban')

# Áp dụng hàm để lấy 50 nhân viên có lương thấp nhất mỗi phòng ban
lowest_salary_employees = df.groupby('Ten phong ban').apply(get_lowest_salary_employees).reset_index(drop=True)

# Hiển thị danh sách nhân viên bị sa thải
print("Danh sách nhân viên bị sa thải (50 người có lương thấp nhất mỗi phòng ban):")
print(lowest_salary_employees[['Ma nhan vien', 'Ho ten nhan vien', 'Ten phong ban', 'Luong co ban']].to_string(index=False))
print(f"\nTổng số nhân viên bị sa thải: {len(lowest_salary_employees)}")

# Cập nhật ghi chú cho những nhân viên bị sa thải
df.loc[df['Ma nhan vien'].isin(lowest_salary_employees['Ma nhan vien']), 'Ghi chu'] = 'Đã sa thải'

# Lưu lại file CSV gốc
df.to_csv('ds_nhan_vien.csv', index=False)

print("\nĐã cập nhật ghi chú 'Đã sa thải' trong file ds_nhan_vien.csv")