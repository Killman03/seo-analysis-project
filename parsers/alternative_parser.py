"""
Альтернативный парсер для обхода блокировок Google
"""
import requests
import time
import random
from bs4 import BeautifulSoup
from loguru import logger
from config import Config
from utils.proxy_manager import proxy_manager

class AlternativeParser:
    """Альтернативный парсер с различными методами"""
    
    def __init__(self):
        self.session = proxy_manager.get_session()
        
    def parse_with_serpapi(self, keyword):
        """Парсинг через SerpAPI (требует API ключ)"""
        try:
            # Это пример, нужно зарегистрироваться на serpapi.com
            api_key = Config.SERPAPI_KEY if hasattr(Config, 'SERPAPI_KEY') else None
            if not api_key:
                logger.warning("SerpAPI ключ не настроен")
                return []
            
            url = "https://serpapi.com/search"
            params = {
                'q': keyword,
                'api_key': api_key,
                'gl': Config.GOOGLE_REGION,
                'hl': Config.GOOGLE_LANGUAGE,
                'num': Config.MAX_RESULTS
            }
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            results = []
            if 'organic_results' in data:
                for i, result in enumerate(data['organic_results'], 1):
                    results.append({
                        'position': i,
                        'title': result.get('title', ''),
                        'url': result.get('link', ''),
                        'domain': result.get('displayed_link', ''),
                        'description': result.get('snippet', '')
                    })
            
            logger.info(f"SerpAPI: найдено {len(results)} результатов")
            return results
            
        except Exception as e:
            logger.error(f"Ошибка SerpAPI: {e}")
            return []
    
    def parse_with_scraperapi(self, keyword):
        """Парсинг через ScraperAPI"""
        try:
            api_key = Config.SCRAPER_API_KEY
            if not api_key:
                logger.warning("ScraperAPI ключ не настроен")
                return []
            
            # Построение URL для Google
            search_url = f"https://www.google.com/search?q={keyword}&gl={Config.GOOGLE_REGION}&hl={Config.GOOGLE_LANGUAGE}&num={Config.MAX_RESULTS}"
            
            # ScraperAPI URL
            scraper_url = f"http://api.scraperapi.com?api_key={api_key}&url={search_url}&country_code=kg"
            
            response = requests.get(scraper_url, timeout=60)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self.parse_google_results(soup)
            else:
                logger.error(f"ScraperAPI вернул код: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Ошибка ScraperAPI: {e}")
            return []
    
    def parse_google_results(self, soup):
        """Парсинг результатов Google из HTML"""
        results = []
        
        # Поиск результатов
        search_results = soup.find_all('div', class_='g')
        
        for i, result in enumerate(search_results, 1):
            try:
                # Заголовок
                title_element = result.find('h3')
                if not title_element:
                    continue
                
                title = title_element.get_text(strip=True)
                
                # Ссылка
                link_element = result.find('a')
                if not link_element:
                    continue
                
                url = link_element.get('href', '')
                if url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&')[0]
                
                # Домен
                from urllib.parse import urlparse
                domain = urlparse(url).netloc if url else ''
                
                # Описание
                desc_element = result.find('div', class_='VwiC3b')
                description = desc_element.get_text(strip=True) if desc_element else ''
                
                results.append({
                    'position': i,
                    'title': title,
                    'url': url,
                    'domain': domain,
                    'description': description
                })
                
            except Exception as e:
                logger.debug(f"Ошибка парсинга результата: {e}")
                continue
        
        return results
    
    def parse_with_requests_advanced(self, keyword):
        """Продвинутый парсинг с requests"""
        try:
            # Различные User-Agents
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
            ]
            
            # Случайный User-Agent
            user_agent = random.choice(user_agents)
            
            # Заголовки
            headers = {
                'User-Agent': user_agent,
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
                'Referer': 'https://www.google.com/',
            }
            
            # URL поиска
            search_url = f"https://www.google.com/search?q={keyword}&gl={Config.GOOGLE_REGION}&hl={Config.GOOGLE_LANGUAGE}&num={Config.MAX_RESULTS}&safe=off&pws=0"
            
            # Случайная задержка
            time.sleep(random.uniform(2, 5))
            
            response = requests.get(search_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self.parse_google_results(soup)
            else:
                logger.error(f"Запрос вернул код: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Ошибка продвинутого парсинга: {e}")
            return []
    
    def parse_keyword(self, keyword, method='requests'):
        """Основной метод парсинга"""
        logger.info(f"Альтернативный парсинг: {keyword} методом {method}")
        
        if method == 'serpapi':
            return self.parse_with_serpapi(keyword)
        elif method == 'scraperapi':
            return self.parse_with_scraperapi(keyword)
        elif method == 'requests':
            return self.parse_with_requests_advanced(keyword)
        else:
            logger.error(f"Неизвестный метод: {method}")
            return []
    
    def try_all_methods(self, keyword):
        """Попробовать все методы парсинга"""
        methods = ['requests', 'scraperapi', 'serpapi']
        
        for method in methods:
            try:
                results = self.parse_keyword(keyword, method)
                if results:
                    logger.info(f"Успешно получены результаты методом {method}")
                    return results
                else:
                    logger.warning(f"Метод {method} не дал результатов")
            except Exception as e:
                logger.error(f"Ошибка метода {method}: {e}")
                continue
        
        logger.error("Все методы парсинга не сработали")
        return [] 