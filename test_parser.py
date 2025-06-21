"""
Тестовый скрипт для проверки работы парсеров
"""
import sys
import os
from loguru import logger

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from parsers import GoogleParser, YandexParser, PageParser
from utils import proxy_manager

def test_google_parser():
    """Тест парсера Google"""
    logger.info("Тестирование парсера Google")
    
    try:
        parser = GoogleParser(use_selenium=False)
        
        # Тестируем с одним ключевым словом
        keyword = "купить iPhone Бишкек"
        results = parser.parse_keyword(keyword)
        
        if results:
            logger.info(f"Найдено {len(results)} результатов в Google")
            for i, result in enumerate(results[:3], 1):
                logger.info(f"{i}. {result['title']}")
                logger.info(f"   URL: {result['url']}")
                logger.info(f"   Домен: {result['domain']}")
                logger.info("")
        else:
            logger.warning("Не найдено результатов в Google")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка тестирования Google парсера: {e}")
        return False

def test_yandex_parser():
    """Тест парсера Yandex"""
    logger.info("Тестирование парсера Yandex")
    
    try:
        parser = YandexParser(use_selenium=False)
        
        # Тестируем с одним ключевым словом
        keyword = "купить iPhone Бишкек"
        results = parser.parse_keyword(keyword)
        
        if results:
            logger.info(f"Найдено {len(results)} результатов в Yandex")
            for i, result in enumerate(results[:3], 1):
                logger.info(f"{i}. {result['title']}")
                logger.info(f"   URL: {result['url']}")
                logger.info(f"   Домен: {result['domain']}")
                logger.info("")
        else:
            logger.warning("Не найдено результатов в Yandex")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка тестирования Yandex парсера: {e}")
        return False

def test_page_parser():
    """Тест парсера страниц"""
    logger.info("Тестирование парсера страниц")
    
    try:
        parser = PageParser()
        
        # Тестируем с реальным сайтом
        test_url = "https://www.google.com"
        page_data = parser.parse_page(test_url)
        
        if page_data:
            logger.info("Данные страницы получены:")
            logger.info(f"Title: {page_data.get('title', 'N/A')}")
            logger.info(f"Description: {page_data.get('description', 'N/A')[:100]}...")
            logger.info(f"Word count: {page_data.get('word_count', 0)}")
            logger.info(f"H1 tags: {len(page_data.get('h1', []))}")
            logger.info(f"Images: {len(page_data.get('images', []))}")
            logger.info(f"Links: {len(page_data.get('links', []))}")
        else:
            logger.warning("Не удалось получить данные страницы")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка тестирования парсера страниц: {e}")
        return False

def test_proxy_manager():
    """Тест менеджера прокси"""
    logger.info("Тестирование менеджера прокси")
    
    try:
        # Тест получения User-Agent
        user_agent = proxy_manager.get_random_user_agent()
        logger.info(f"User-Agent: {user_agent}")
        
        # Тест получения заголовков
        headers = proxy_manager.get_headers()
        logger.info(f"Заголовки: {headers}")
        
        # Тест сессии
        session = proxy_manager.get_session()
        logger.info("Сессия создана успешно")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка тестирования менеджера прокси: {e}")
        return False

def main():
    """Основная функция тестирования"""
    logger.info("Начинаем тестирование SEO-парсера")
    
    tests = [
        ("Менеджер прокси", test_proxy_manager),
        ("Google парсер", test_google_parser),
        ("Yandex парсер", test_yandex_parser),
        ("Парсер страниц", test_page_parser),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Тест: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"Критическая ошибка в тесте {test_name}: {e}")
            results[test_name] = False
    
    # Итоговый отчет
    logger.info(f"\n{'='*50}")
    logger.info("ИТОГОВЫЙ ОТЧЕТ")
    logger.info(f"{'='*50}")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nРезультат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        logger.info("🎉 Все тесты пройдены успешно!")
    else:
        logger.warning("⚠️ Некоторые тесты не пройдены")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 