# chuyển tất cả nhân viên nữ từ phòng kỹ thuật sang phòng kinh doanh
import pandas as pd

# Đọc file CSV
df = pd.read_csv('ds_nhan_vien.csv')

# Lọc các nhân viên nữ thuộc phòng Kỹ thuật, không phải Giám đốc hoặc Quản lý
condition = (df['Gioi tinh'] == 'Nu') & (df['Ten phong ban'] == 'Ky thuat') & (df['Chuc vu'] == 'Nhan vien')

# Hiển thị danh sách nhân viên được chuyển
transferred_employees = df[condition][['Ma nhan vien', 'Ho ten nhan vien', 'Ten phong ban', 'Gioi tinh', 'Chuc vu']]
print("Danh sách nhân viên nữ được chuyển từ phòng Kỹ thuật sang phòng Kinh doanh:")
print(transferred_employees.to_string(index=False))
print(f"\nTổng số nhân viên được chuyển: {len(transferred_employees)}")

# Cập nhật phòng ban thành Kinh doanh và ghi chú
df.loc[condition, 'Ten phong ban'] = 'Kinh doanh'
df.loc[condition, 'Ghi chu'] = 'Đã chuyển từ phòng Kỹ thuật sang Kinh doanh'

# Lưu lại file CSV
df.to_csv('ds_nhan_vien_updated.csv', index=False)

print("\nĐã cập nhật file CSV. Kết quả được lưu vào file ds_nhan_vien_updated.csv")