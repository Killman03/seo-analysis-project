"""
Модуль управления прокси и обхода блокировок
"""
import random
import time
import requests
import zipfile
from fake_useragent import UserAgent
from loguru import logger
from config import Config


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (Config.PROXY_HOST, Config.PROXY_PORT, Config.PROXY_USER, Config.PROXY_PASS)


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

        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return pluginfile
    
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