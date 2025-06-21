"""
Парсер мета-данных страниц конкурентов
"""
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from loguru import logger
from config import Config
from utils.proxy_manager import proxy_manager

class PageParser:
    """Парсер мета-данных страниц"""
    
    def __init__(self):
        self.session = proxy_manager.get_session()
        
    def get_page_content(self, url):
        """Получить содержимое страницы"""
        try:
            logger.info(f"Парсинг страницы: {url}")
            
            response = self.session.get(url, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            # Проверяем кодировку
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'
            
            return response.text
            
        except Exception as e:
            logger.error(f"Ошибка при получении страницы {url}: {e}")
            return None
    
    def extract_meta_data(self, html, url):
        """Извлечение мета-данных из HTML"""
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        meta_data = {
            'url': url,
            'title': '',
            'description': '',
            'keywords': '',
            'h1': [],
            'h2': [],
            'h3': [],
            'images': [],
            'links': [],
            'word_count': 0
        }
        
        try:
            # Title
            title_tag = soup.find('title')
            if title_tag:
                meta_data['title'] = title_tag.get_text(strip=True)
            
            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                meta_data['description'] = meta_desc.get('content', '')
            
            # Meta keywords
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords:
                meta_data['keywords'] = meta_keywords.get('content', '')
            
            # Заголовки H1-H3
            for i in range(1, 4):
                headers = soup.find_all(f'h{i}')
                meta_data[f'h{i}'] = [h.get_text(strip=True) for h in headers]
            
            # Изображения
            images = soup.find_all('img')
            meta_data['images'] = [
                {
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                }
                for img in images if img.get('src')
            ]
            
            # Ссылки
            links = soup.find_all('a', href=True)
            meta_data['links'] = [
                {
                    'href': urljoin(url, link.get('href')),
                    'text': link.get_text(strip=True),
                    'title': link.get('title', '')
                }
                for link in links
            ]
            
            # Подсчет слов
            text_content = soup.get_text()
            meta_data['word_count'] = len(text_content.split())
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении мета-данных: {e}")
        
        return meta_data
    
    def analyze_keyword_density(self, html, keyword):
        """Анализ плотности ключевых слов"""
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        text_content = soup.get_text().lower()
        
        # Очищаем текст от лишних символов
        text_content = re.sub(r'[^\w\s]', ' ', text_content)
        words = text_content.split()
        
        # Подсчитываем вхождения ключевых слов
        keyword_parts = keyword.lower().split()
        keyword_phrases = []
        
        # Однословные ключевые слова
        for word in keyword_parts:
            count = words.count(word)
            keyword_phrases.append({
                'keyword': word,
                'count': count,
                'density': (count / len(words)) * 100 if words else 0
            })
        
        # Многословные фразы
        if len(keyword_parts) > 1:
            full_phrase = ' '.join(keyword_parts)
            phrase_count = text_content.count(full_phrase)
            keyword_phrases.append({
                'keyword': full_phrase,
                'count': phrase_count,
                'density': (phrase_count / len(words)) * 100 if words else 0
            })
        
        return {
            'total_words': len(words),
            'keyword_analysis': keyword_phrases
        }
    
    def check_technical_seo(self, html, url):
        """Проверка технического SEO"""
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        technical_checks = {
            'has_title': False,
            'has_description': False,
            'has_keywords': False,
            'has_h1': False,
            'has_images_with_alt': False,
            'has_canonical': False,
            'has_robots': False,
            'has_schema': False,
            'is_https': False,
            'has_ssl': False
        }
        
        try:
            # Проверка HTTPS
            parsed_url = urlparse(url)
            technical_checks['is_https'] = parsed_url.scheme == 'https'
            
            # Проверка мета-тегов
            technical_checks['has_title'] = bool(soup.find('title'))
            technical_checks['has_description'] = bool(soup.find('meta', attrs={'name': 'description'}))
            technical_checks['has_keywords'] = bool(soup.find('meta', attrs={'name': 'keywords'}))
            technical_checks['has_h1'] = bool(soup.find('h1'))
            technical_checks['has_canonical'] = bool(soup.find('link', attrs={'rel': 'canonical'}))
            technical_checks['has_robots'] = bool(soup.find('meta', attrs={'name': 'robots'}))
            
            # Проверка изображений с alt
            images = soup.find_all('img')
            images_with_alt = [img for img in images if img.get('alt')]
            technical_checks['has_images_with_alt'] = len(images_with_alt) > 0
            
            # Проверка Schema.org разметки
            schema_scripts = soup.find_all('script', type='application/ld+json')
            technical_checks['has_schema'] = len(schema_scripts) > 0
            
        except Exception as e:
            logger.error(f"Ошибка при проверке технического SEO: {e}")
        
        return technical_checks
    
    def parse_page(self, url, keyword=None):
        """Полный парсинг страницы"""
        try:
            # Получаем содержимое страницы
            html = self.get_page_content(url)
            if not html:
                return None
            
            # Извлекаем мета-данные
            meta_data = self.extract_meta_data(html, url)
            
            # Анализируем ключевые слова
            keyword_analysis = {}
            if keyword:
                keyword_analysis = self.analyze_keyword_density(html, keyword)
            
            # Проверяем техническое SEO
            technical_seo = self.check_technical_seo(html, url)
            
            # Объединяем все данные
            result = {
                **meta_data,
                'keyword_analysis': keyword_analysis,
                'technical_seo': technical_seo
            }
            
            logger.info(f"Успешно проанализирована страница: {url}")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге страницы {url}: {e}")
            return None 