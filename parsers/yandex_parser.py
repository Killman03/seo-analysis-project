"""
Парсер Яндекса с региональными настройками Бишкека
"""
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from config import Config
from utils.proxy_manager import proxy_manager

class YandexParser:
    """Парсер результатов поиска Яндекса"""
    
    def __init__(self, use_selenium=False):
        self.use_selenium = use_selenium
        self.driver = None
        self.session = proxy_manager.get_session()
        
    def setup_selenium(self):
        """Настройка Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={proxy_manager.get_random_user_agent()}")
        
        if Config.USE_PROXY and Config.PROXY_LIST:
            proxy = proxy_manager.get_proxy()
            if proxy:
                chrome_options.add_argument(f"--proxy-server={proxy}")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def build_search_url(self, keyword, page=1):
        """Построить URL для поиска в Яндексе"""
        params = {
            'text': keyword,
            'lr': Config.YANDEX_REGION,  # Бишкек
            'p': page - 1,  # Нумерация страниц в Яндексе начинается с 0
            'numdoc': Config.MAX_RESULTS
        }
        
        base_url = "https://yandex.ru/search"
        query_string = urllib.parse.urlencode(params)
        return f"{base_url}?{query_string}"
    
    def extract_domain(self, url):
        """Извлечь домен из URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url
    
    def parse_organic_results(self, soup):
        """Парсинг органических результатов Яндекса"""
        results = []
        
        # Поиск органических результатов
        organic_results = soup.find_all('div', class_='serp-item')
        
        for i, result in enumerate(organic_results, 1):
            try:
                # Заголовок и ссылка
                title_element = result.find('a', class_='link')
                if not title_element:
                    continue
                
                title = title_element.get_text(strip=True)
                url = title_element.get('href', '')
                
                # Описание
                description_element = result.find('div', class_='text-container')
                description = description_element.get_text(strip=True) if description_element else ""
                
                # Домен
                domain = self.extract_domain(url)
                
                # Проверяем, что это не реклама
                if not result.find('div', class_='label'):
                    results.append({
                        'position': i,
                        'title': title,
                        'url': url,
                        'domain': domain,
                        'description': description
                    })
                
            except Exception as e:
                logger.error(f"Ошибка при парсинге результата Яндекса {i}: {e}")
                continue
        
        return results
    
    def parse_with_requests(self, keyword, page=1):
        """Парсинг с помощью requests"""
        try:
            url = self.build_search_url(keyword, page)
            logger.info(f"Парсинг Яндекса: {keyword}, страница {page}")
            
            response = self.session.get(url, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Проверка на капчу
            if "captcha" in response.text.lower() or "robot" in response.text.lower():
                logger.warning("Обнаружена капча в Яндексе")
                return self.handle_captcha(keyword, page)
            
            results = self.parse_organic_results(soup)
            logger.info(f"Найдено {len(results)} результатов в Яндексе для '{keyword}'")
            
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге Яндекса: {e}")
            return []
    
    def parse_with_selenium(self, keyword, page=1):
        """Парсинг с помощью Selenium"""
        try:
            if not self.driver:
                self.setup_selenium()
            
            url = self.build_search_url(keyword, page)
            logger.info(f"Парсинг Яндекса (Selenium): {keyword}, страница {page}")
            
            self.driver.get(url)
            
            # Ждем загрузки результатов
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "serp-item"))
            )
            
            # Получаем HTML
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            results = self.parse_organic_results(soup)
            logger.info(f"Найдено {len(results)} результатов в Яндексе для '{keyword}'")
            
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге Яндекса (Selenium): {e}")
            return []
    
    def handle_captcha(self, keyword, page):
        """Обработка капчи"""
        logger.warning("Требуется ручное решение капчи в Яндексе")
        # Здесь можно интегрировать 2captcha или другие сервисы
        return []
    
    def parse_keyword(self, keyword, page=1):
        """Основной метод парсинга ключевого слова"""
        proxy_manager.random_delay()
        
        if self.use_selenium:
            return self.parse_with_selenium(keyword, page)
        else:
            return self.parse_with_requests(keyword, page)
    
    def close(self):
        """Закрыть браузер"""
        if self.driver:
            self.driver.quit() 