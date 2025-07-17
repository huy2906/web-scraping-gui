import pandas as pd
import os
from datetime import datetime
import logging

class DataManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def save_to_excel(self, data, filename):
        """
        Lưu dữ liệu ra file Excel
        
        Args:
            data (list): Danh sách dữ liệu cần lưu
            filename (str): Tên file Excel
        """
        try:
            if not data:
                raise ValueError("Không có dữ liệu để lưu")
            
            # Tạo DataFrame
            df = pd.DataFrame(data)
            
            # Tạo writer object
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Sheet chính chứa dữ liệu
                df.to_excel(writer, sheet_name='Dữ liệu', index=False)
                
                # Sheet thống kê
                self._create_summary_sheet(writer, data)
                
                # Sheet cấu hình
                self._create_config_sheet(writer, data)
            
            self.logger.info(f"Đã lưu dữ liệu vào file: {filename}")
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lưu file Excel: {str(e)}")
            raise
    
    def _create_summary_sheet(self, writer, data):
        """Tạo sheet thống kê"""
        summary_data = {
            'Thông tin': [
                'Tổng số URL đã cào',
                'Số URL thành công',
                'Số URL thất bại',
                'Ngày tạo file',
                'Thời gian tạo'
            ],
            'Giá trị': [
                len(data),
                len([d for d in data if d.get('title')]),
                len([d for d in data if not d.get('title')]),
                datetime.now().strftime('%Y-%m-%d'),
                datetime.now().strftime('%H:%M:%S')
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Thống kê', index=False)
    
    def _create_config_sheet(self, writer, data):
        """Tạo sheet cấu hình"""
        if not data:
            return
        
        # Lấy thông tin từ dữ liệu đầu tiên
        first_data = data[0]
        
        config_data = {
            'Thông số': [
                'URL mẫu',
                'Tiêu đề mẫu',
                'Độ dài nội dung trung bình',
                'Số hình ảnh trung bình',
                'Định dạng ngày'
            ],
            'Giá trị': [
                first_data.get('url', ''),
                first_data.get('title', '')[:50] + '...' if len(first_data.get('title', '')) > 50 else first_data.get('title', ''),
                f"{sum(len(d.get('content', '')) for d in data) // len(data)} ký tự",
                f"{sum(len(d.get('images', [])) for d in data) // len(data)} hình",
                'YYYY-MM-DD HH:MM:SS'
            ]
        }
        
        config_df = pd.DataFrame(config_data)
        config_df.to_excel(writer, sheet_name='Cấu hình', index=False)
    
    def load_from_excel(self, filename):
        """
        Đọc dữ liệu từ file Excel
        
        Args:
            filename (str): Tên file Excel
            
        Returns:
            list: Danh sách dữ liệu
        """
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Không tìm thấy file: {filename}")
            
            # Đọc sheet dữ liệu chính
            df = pd.read_excel(filename, sheet_name='Dữ liệu')
            
            # Chuyển đổi thành list of dicts
            data = df.to_dict('records')
            
            self.logger.info(f"Đã đọc dữ liệu từ file: {filename}")
            return data
            
        except Exception as e:
            self.logger.error(f"Lỗi khi đọc file Excel: {str(e)}")
            raise
    
    def export_to_csv(self, data, filename):
        """
        Xuất dữ liệu ra file CSV
        
        Args:
            data (list): Danh sách dữ liệu
            filename (str): Tên file CSV
        """
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            self.logger.info(f"Đã xuất dữ liệu ra file CSV: {filename}")
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xuất file CSV: {str(e)}")
            raise
    
    def validate_data(self, data):
        """
        Kiểm tra tính hợp lệ của dữ liệu
        
        Args:
            data (list): Danh sách dữ liệu
            
        Returns:
            dict: Kết quả validation
        """
        if not data:
            return {'valid': False, 'errors': ['Không có dữ liệu']}
        
        errors = []
        valid_count = 0
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                errors.append(f"Dòng {i+1}: Dữ liệu không phải dictionary")
                continue
            
            # Kiểm tra các trường bắt buộc
            if not item.get('url'):
                errors.append(f"Dòng {i+1}: Thiếu URL")
            else:
                valid_count += 1
            
            if not item.get('title'):
                errors.append(f"Dòng {i+1}: Thiếu tiêu đề")
            
            if not item.get('content'):
                errors.append(f"Dòng {i+1}: Thiếu nội dung")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'valid_count': valid_count,
            'total_count': len(data)
        } 