"""
Парсер Google с региональными настройками Кыргызстана
"""
import re
import urllib.parse
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from config import Config
from utils.proxy_manager import proxy_manager

class GoogleParser:
    """Парсер результатов поиска Google"""
    
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
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument(f"--user-agent={proxy_manager.get_random_user_agent()}")
        
        if Config.USE_PROXY and Config.PROXY_LIST:
            proxy = proxy_manager.get_proxy()
            if proxy:
                chrome_options.add_argument(f"--proxy-server={proxy}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": proxy_manager.get_random_user_agent()
            })
        except Exception as e:
            logger.error(f"Ошибка создания WebDriver: {e}")
            self.driver = None
        
    def build_search_url(self, keyword, page=1):
        """Построить URL для поиска"""
        params = {
            'q': keyword,
            'num': Config.MAX_RESULTS,
            'gl': Config.GOOGLE_REGION,  # Кыргызстан
            'hl': Config.GOOGLE_LANGUAGE,  # Русский
            'start': (page - 1) * Config.MAX_RESULTS,
            'safe': 'off',  # Отключаем безопасный поиск
            'pws': '0',  # Отключаем персонализацию
        }
        
        base_url = "https://www.google.com/search"
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
        """Парсинг органических результатов"""
        results = []
        
        # Различные селекторы для поиска результатов
        selectors = [
            'div.g',  # Стандартный селектор
            'div[data-hveid]',  # Альтернативный селектор
            'div.rc',  # Еще один вариант
            'div[jscontroller]',  # Современный селектор
            'div[jsname]',  # Новый селектор
        ]
        
        organic_results = []
        for selector in selectors:
            try:
                if '.' in selector:
                    class_name = selector.split('.')[-1]
                    organic_results = soup.find_all('div', class_=class_name)
                else:
                    # Для селекторов с атрибутами
                    if '[' in selector:
                        attr_name = selector.split('[')[1].split(']')[0]
                        if '=' in attr_name:
                            name, value = attr_name.split('=')
                            organic_results = soup.find_all('div', attrs={name.strip(): value.strip().strip('"')})
                        else:
                            organic_results = soup.find_all('div', attrs={attr_name: True})
                    else:
                        organic_results = soup.find_all('div')
                
                if organic_results:
                    logger.info(f"Найдены результаты с селектором: {selector}")
                    break
            except Exception as e:
                logger.debug(f"Ошибка с селектором {selector}: {e}")
                continue
        
        if not organic_results:
            # Попробуем найти любые div с ссылками
            organic_results = soup.find_all('div')
            organic_results = [div for div in organic_results if div.find('a', href=True)]
            logger.info("Используем fallback селектор")
        
        logger.info(f"Найдено {len(organic_results)} потенциальных результатов")
        
        for i, result in enumerate(organic_results, 1):
            try:
                # Поиск заголовка и ссылки
                title_element = None
                link_element = None
                
                # Различные селекторы для заголовка
                title_selectors = ['h3', 'a h3', '.LC20lb', '.DKV0Md', '.r', '.title']
                for selector in title_selectors:
                    try:
                        if selector == 'h3':
                            title_element = result.find('h3')
                        elif selector.startswith('.'):
                            title_element = result.select_one(selector)
                        else:
                            title_element = result.select_one(selector)
                        
                        if title_element and title_element.get_text(strip=True):
                            break
                    except:
                        continue
                
                # Поиск ссылки
                link_element = result.find('a', href=True)
                
                if not title_element or not link_element:
                    continue
                
                title = title_element.get_text(strip=True)
                url = link_element.get('href', '')
                
                # Извлекаем реальный URL из Google redirect
                if url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&')[0]
                elif url.startswith('/url?'):
                    # Альтернативный формат
                    import urllib.parse
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
                    if 'q' in parsed:
                        url = parsed['q'][0]
                
                # Пропускаем внутренние ссылки Google
                if 'google.com' in url or not url.startswith('http'):
                    continue
                
                # Описание
                description_element = None
                desc_selectors = ['.VwiC3b', '.s3v9rd', '.st', '.aCOpRe', '.snippet-content']
                for selector in desc_selectors:
                    try:
                        description_element = result.select_one(selector)
                        if description_element and description_element.get_text(strip=True):
                            break
                    except:
                        continue
                
                description = description_element.get_text(strip=True) if description_element else ""
                
                # Домен
                domain = self.extract_domain(url)
                
                # Проверяем, что у нас есть все необходимые данные
                if title and url and domain:
                    results.append({
                        'position': i,
                        'title': title,
                        'url': url,
                        'domain': domain,
                        'description': description
                    })
                    logger.debug(f"Добавлен результат {i}: {title[:50]}...")
                
            except Exception as e:
                logger.debug(f"Ошибка при парсинге результата {i}: {e}")
                continue
        
        logger.info(f"Успешно обработано {len(results)} результатов")
        return results
    
    def parse_with_requests(self, keyword, page=1):
        """Парсинг с помощью requests"""
        try:
            url = self.build_search_url(keyword, page)
            logger.info(f"Парсинг Google: {keyword}, страница {page}")
            
            # Добавляем дополнительные заголовки
            headers = {
                'User-Agent': proxy_manager.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            }
            
            # Добавляем случайную задержку
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, headers=headers, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Проверка на капчу
            captcha_indicators = [
                "captcha", "robot", "verify", "security check",
                "sorry/index", "consent", "unusual traffic"
            ]
            
            page_text = response.text.lower()
            if any(indicator in page_text for indicator in captcha_indicators):
                logger.warning("Обнаружена капча в Google")
                return self.handle_captcha(keyword, page)
            
            # Проверка на блокировку
            if "sorry/index" in response.url or "consent" in response.url:
                logger.warning("Google требует согласие или блокирует запрос")
                return []
            
            results = self.parse_organic_results(soup)
            logger.info(f"Найдено {len(results)} результатов для '{keyword}'")
            
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге Google: {e}")
            return []
    
    def parse_with_selenium(self, keyword, page=1):
        """Парсинг с помощью Selenium"""
        try:
            if not self.driver:
                self.setup_selenium()
            
            if not self.driver:
                logger.error("Не удалось создать WebDriver")
                return []
            
            url = self.build_search_url(keyword, page)
            logger.info(f"Парсинг Google (Selenium): {keyword}, страница {page}")
            
            self.driver.get(url)
            
            # Ждем загрузки результатов
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "div"))
                )
                # Дополнительная пауза для полной загрузки
                time.sleep(3)
            except:
                logger.warning("Таймаут ожидания загрузки страницы")
            
            # Получаем HTML
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            results = self.parse_organic_results(soup)
            logger.info(f"Найдено {len(results)} результатов для '{keyword}'")
            
            return results
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге Google (Selenium): {e}")
            return []
    
    def handle_captcha(self, keyword, page):
        """Обработка капчи"""
        logger.warning("Требуется ручное решение капчи")
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
            try:
                self.driver.quit()
            except:
                pass 