"""
Модуль управления прокси и обхода блокировок
"""
import random
import time
import requests
from fake_useragent import UserAgent
from loguru import logger
from config import Config

class ProxyManager:
    """Менеджер прокси и User-Agent"""
    
    def __init__(self):
        self.proxy_list = Config.PROXY_LIST
        self.user_agents = Config.USER_AGENTS
        self.ua = UserAgent()
        self.current_proxy_index = 0
        
    def get_random_user_agent(self):
        """Получить случайный User-Agent"""
        try:
            return self.ua.random
        except:
            return random.choice(self.user_agents)
    
    def get_proxy(self):
        """Получить следующий прокси из списка"""
        if not self.proxy_list:
            return None
            
        proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return proxy
    
    def get_headers(self):
        """Получить заголовки для запроса"""
        return {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def random_delay(self):
        """Случайная задержка между запросами"""
        delay = random.uniform(Config.DELAY_MIN, Config.DELAY_MAX)
        logger.info(f"Задержка {delay:.2f} секунд")
        time.sleep(delay)
    
    def check_proxy(self, proxy):
        """Проверить работоспособность прокси"""
        try:
            proxies = {"http": proxy, "https": proxy}
            response = requests.get(
                "http://httpbin.org/ip", 
                proxies=proxies, 
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def get_session(self):
        """Получить сессию с настройками"""
        session = requests.Session()
        session.headers.update(self.get_headers())
        
        if Config.USE_PROXY and self.proxy_list:
            proxy = self.get_proxy()
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
        
        return session

# Глобальный экземпляр менеджера прокси
proxy_manager = ProxyManager() 