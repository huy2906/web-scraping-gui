# Cấu hình cho ứng dụng Web Scraping

# Cấu hình request
REQUEST_CONFIG = {
    'timeout': 30,  # Timeout cho mỗi request (giây)
    'delay': 1,     # Delay giữa các request (giây)
    'max_retries': 3,  # Số lần thử lại tối đa
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# CSS Selector mặc định
DEFAULT_SELECTORS = {
    'title': 'h1, .title, .post-title, meta[property="og:title"]',
    'content': '.content, .post-content, article, .entry-content',
    'date': 'time[datetime], .date, .published, meta[property="article:published_time"]',
    'images': 'img[src], img[data-src]'
}

# Cấu hình giao diện
UI_CONFIG = {
    'window_size': '1000x700',
    'url_list_height': 6,
    'result_table_height': 15,
    'max_title_length': 50,
    'max_content_length': 100
}

# Cấu hình file Excel
EXCEL_CONFIG = {
    'sheet_names': {
        'data': 'Dữ liệu',
        'summary': 'Thống kê',
        'config': 'Cấu hình'
    },
    'max_images_per_url': 5
}

# Cấu hình logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
} 