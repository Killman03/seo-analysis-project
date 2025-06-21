"""
Конфигурация для SEO-парсинга конкурентов в Кыргызстане
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Региональные настройки
    GOOGLE_REGION = "kg"  # Кыргызстан
    GOOGLE_LANGUAGE = "ru"  # Русский язык
    YANDEX_REGION = "10363"  # Бишкек
    
    # Настройки парсинга
    MAX_RESULTS = 10
    DELAY_MIN = 2
    DELAY_MAX = 5
    TIMEOUT = 30
    
    # User-Agents для ротации
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    # Прокси настройки (если используются)
    PROXY_LIST = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []
    USE_PROXY = os.getenv("USE_PROXY", "False").lower() == "true"
    
    # API ключи
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "")
    SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY", "")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    
    # База данных
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/seo_analysis")
    
    # Ключевые запросы для анализа
    KEYWORDS = [
        "купить кофемашина Бишкек",
        "кофемашина в Бишкеке",
        "доставка кофеварка Бишкек",
        "кофеварка Бишкек",
        "кофемашина Бишкек",
        "ремонт кофемашин Бишкек",
        "кофемашина кыргызстан",
        "кофеварка Кыргызстан",
    ]
    
    # Настройки логирования
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/seo_parser.log"
    
    # Настройки экспорта
    CSV_OUTPUT_DIR = "data/csv"
    PDF_OUTPUT_DIR = "data/reports"
    
    # Настройки дашборда
    DASHBOARD_PORT = 8501
    DASHBOARD_HOST = "localhost"
    
    # Настройки парсинга
    USE_SELENIUM = os.getenv("USE_SELENIUM", "True").lower() == "true"
    USE_ALTERNATIVE_PARSER = os.getenv("USE_ALTERNATIVE_PARSER", "True").lower() == "true"
    
    # Настройки обхода блокировок
    MAX_RETRIES = 3
    RETRY_DELAY = 10 