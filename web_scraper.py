import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
import logging

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.stop_flag = False
        
        # Cấu hình logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def stop_scraping(self):
        """Dừng quá trình scraping"""
        self.stop_flag = True
    
    def scrape_url(self, url, title_selector, content_selector):
        """
        Cào dữ liệu từ một URL cụ thể
        
        Args:
            url (str): URL cần cào dữ liệu
            title_selector (str): CSS selector cho tiêu đề
            content_selector (str): CSS selector cho nội dung
            
        Returns:
            dict: Dữ liệu đã cào được hoặc None nếu thất bại
        """
        if self.stop_flag:
            return None
        
        try:
            self.logger.info(f"Đang cào dữ liệu từ: {url}")
            
            # Gửi request
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Lấy tiêu đề
            title = self._extract_title(soup, title_selector, url)
            
            # Lấy nội dung
            content = self._extract_content(soup, content_selector)
            
            # Lấy ngày đăng (nếu có)
            date = self._extract_date(soup)
            
            # Lấy URL hình ảnh (nếu có)
            images = self._extract_images(soup, url)
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'date': date,
                'images': images,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except requests.RequestException as e:
            self.logger.error(f"Lỗi request cho {url}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Lỗi khi cào dữ liệu từ {url}: {str(e)}")
            return None
    
    def _extract_title(self, soup, selector, url):
        """Trích xuất tiêu đề từ trang web"""
        title = ""
        
        # Thử với CSS selector được cung cấp
        if selector:
            selectors = [s.strip() for s in selector.split(',')]
            for sel in selectors:
                elements = soup.select(sel)
                if elements:
                    title = elements[0].get_text(strip=True)
                    break
        
        # Nếu không tìm thấy, thử các selector mặc định
        if not title:
            # Thử với thẻ title
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
            
            # Thử với h1
            if not title:
                h1_tag = soup.find('h1')
                if h1_tag:
                    title = h1_tag.get_text(strip=True)
            
            # Thử với meta title
            if not title:
                meta_title = soup.find('meta', property='og:title')
                if meta_title:
                    title = meta_title.get('content', '')
        
        # Nếu vẫn không có, lấy từ URL
        if not title:
            parsed_url = urlparse(url)
            title = parsed_url.netloc
        
        return title
    
    def _extract_content(self, soup, selector):
        """Trích xuất nội dung từ trang web"""
        content = ""
        
        # Thử với CSS selector được cung cấp
        if selector:
            selectors = [s.strip() for s in selector.split(',')]
            for sel in selectors:
                elements = soup.select(sel)
                if elements:
                    # Lấy tất cả text từ các element
                    for element in elements:
                        text = element.get_text(strip=True)
                        if text:
                            content += text + " "
                    break
        
        # Nếu không tìm thấy, thử các selector mặc định
        if not content:
            # Thử với thẻ article
            article = soup.find('article')
            if article:
                content = article.get_text(strip=True)
            
            # Thử với thẻ main
            elif soup.find('main'):
                content = soup.find('main').get_text(strip=True)
            
            # Thử với div có class content
            else:
                content_divs = soup.find_all('div', class_=re.compile(r'content|post|article', re.I))
                for div in content_divs:
                    text = div.get_text(strip=True)
                    if len(text) > len(content):
                        content = text
        
        # Làm sạch nội dung
        content = self._clean_text(content)
        
        return content
    
    def _extract_date(self, soup):
        """Trích xuất ngày đăng từ trang web"""
        date = ""
        
        # Thử với meta tags
        date_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="publish_date"]',
            'meta[name="date"]',
            'time[datetime]',
            '.date',
            '.published',
            '.post-date'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    date = element.get('content', '')
                else:
                    date = element.get('datetime', '') or element.get_text(strip=True)
                if date:
                    break
        
        return date
    
    def _extract_images(self, soup, base_url):
        """Trích xuất URL hình ảnh từ trang web"""
        images = []
        
        # Tìm tất cả thẻ img
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src:
                # Chuyển đổi URL tương đối thành tuyệt đối
                absolute_url = urljoin(base_url, src)
                images.append(absolute_url)
        
        return images[:5]  # Chỉ lấy 5 hình ảnh đầu tiên
    
    def _clean_text(self, text):
        """Làm sạch text"""
        if not text:
            return ""
        
        # Loại bỏ ký tự xuống dòng thừa
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Loại bỏ khoảng trắng đầu cuối
        text = text.strip()
        
        return text 