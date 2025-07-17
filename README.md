# Ứng dụng Cào Dữ liệu Web

Ứng dụng Python với giao diện GUI cho phép cào dữ liệu từ các trang web và lưu vào file Excel.

## Tính năng

- ✅ Giao diện GUI thân thiện với người dùng
- ✅ Hỗ trợ nhập nhiều URL cùng lúc
- ✅ Tùy chỉnh CSS selector để trích xuất dữ liệu
- ✅ Cào dữ liệu tiêu đề, nội dung, ngày đăng, hình ảnh
- ✅ Lưu kết quả vào file Excel với nhiều sheet
- ✅ Hiển thị kết quả real-time trong bảng
- ✅ Xử lý lỗi và thông báo trạng thái
- ✅ Hỗ trợ dừng quá trình cào dữ liệu

## Cài đặt

1. **Cài đặt Python 3.7+**

2. **Cài đặt các thư viện cần thiết:**
```bash
pip install -r requirements.txt
```

## Sử dụng

1. **Chạy ứng dụng:**
```bash
python main.py
```

2. **Hướng dẫn sử dụng:**

   - **Thêm URL**: Nhập URL vào ô "URL" và nhấn "Thêm URL"
   - **Xóa URL**: Chọn URL trong danh sách và nhấn "Xóa URL"
   - **Cấu hình CSS Selector**:
     - Tiêu đề: `h1, .title, .post-title`
     - Nội dung: `.content, .post-content, article`
   - **Bắt đầu cào dữ liệu**: Nhấn "Bắt đầu Cào Dữ liệu"
   - **Lưu Excel**: Nhấn "Lưu Excel" sau khi hoàn thành

## Cấu trúc dữ liệu

Dữ liệu được lưu trong file Excel với 3 sheet:

1. **Dữ liệu**: Chứa thông tin chính
   - URL
   - Tiêu đề
   - Nội dung
   - Ngày đăng
   - Hình ảnh
   - Thời gian cào

2. **Thống kê**: Thông tin tổng quan
   - Tổng số URL
   - Số URL thành công/thất bại
   - Thời gian tạo file

3. **Cấu hình**: Thông tin cấu hình
   - URL mẫu
   - Tiêu đề mẫu
   - Thống kê dữ liệu

## CSS Selector phổ biến

### Tiêu đề
- `h1` - Tiêu đề chính
- `.title` - Class title
- `.post-title` - Tiêu đề bài viết
- `meta[property="og:title"]` - Meta title

### Nội dung
- `.content` - Class content
- `.post-content` - Nội dung bài viết
- `article` - Thẻ article
- `.entry-content` - Nội dung entry

### Ngày đăng
- `time[datetime]` - Thẻ time với datetime
- `.date` - Class date
- `.published` - Class published
- `meta[property="article:published_time"]` - Meta published time

## Xử lý lỗi

Ứng dụng có các cơ chế xử lý lỗi:

- **Timeout**: Tự động timeout sau 30 giây
- **User-Agent**: Sử dụng User-Agent giả lập trình duyệt
- **Retry**: Tự động thử lại khi gặp lỗi network
- **Validation**: Kiểm tra tính hợp lệ của dữ liệu

## Lưu ý

- Đảm bảo tuân thủ robots.txt của website
- Không cào dữ liệu quá nhanh để tránh bị chặn
- Một số website có thể chặn bot, cần điều chỉnh User-Agent
- Dữ liệu được lưu với encoding UTF-8 để hỗ trợ tiếng Việt

## Tùy chỉnh

Bạn có thể tùy chỉnh ứng dụng bằng cách:

1. **Thêm CSS selector mới** trong file `web_scraper.py`
2. **Thay đổi User-Agent** trong class `WebScraper`
3. **Điều chỉnh timeout** và delay giữa các request
4. **Thêm trường dữ liệu mới** trong hàm `scrape_url`

## Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:

1. Kết nối internet
2. URL có hợp lệ không
3. CSS selector có đúng không
4. Website có chặn bot không 