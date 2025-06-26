# tìm người cao tuổi nhất trong mỗi phòng ban
import pandas as pd

# Đọc file CSV
df = pd.read_csv('ds_nhan_vien.csv')

# Tìm nhân viên cao tuổi nhất trong mỗi phòng ban
oldest_employees = df.loc[df.groupby('Ten phong ban')['Tuoi'].idxmax()]

# Hiển thị danh sách nhân viên cao tuổi nhất
print("Danh sách nhân viên cao tuổi nhất trong mỗi phòng ban:")
print(oldest_employees[['Ten phong ban', 'Ma nhan vien', 'Ho ten nhan vien', 'Tuoi', 'Chuc vu']].to_string(index=False))
print(f"\nTổng số phòng ban: {len(oldest_employees)}")