"""
Специальный тест для проверки парсинга Google
"""
import sys
import os
from loguru import logger

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_google_requests():
    """Тест парсинга Google через requests"""
    logger.info("🔍 Тест Google через requests")
    
    try:
        from parsers.google_parser import GoogleParser
        
        parser = GoogleParser(use_selenium=False)
        results = parser.parse_keyword("кофемашина")
        
        if results:
            logger.info(f"✅ Requests: найдено {len(results)} результатов")
            for i, result in enumerate(results[:2], 1):
                logger.info(f"  {i}. {result['title'][:50]}...")
            return True
        else:
            logger.warning("⚠️ Requests: результаты не найдены")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка requests: {e}")
        return False

def test_google_selenium():
    """Тест парсинга Google через Selenium"""
    logger.info("🔍 Тест Google через Selenium")
    
    try:
        from parsers.google_parser import GoogleParser
        
        parser = GoogleParser(use_selenium=True)
        results = parser.parse_keyword("кофемашина")
        
        if results:
            logger.info(f"✅ Selenium: найдено {len(results)} результатов")
            for i, result in enumerate(results[:2], 1):
                logger.info(f"  {i}. {result['title'][:50]}...")
            return True
        else:
            logger.warning("⚠️ Selenium: результаты не найдены")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка Selenium: {e}")
        return False

def test_alternative_parser():
    """Тест альтернативного парсера"""
    logger.info("🔍 Тест альтернативного парсера")
    
    try:
        from parsers.alternative_parser import AlternativeParser
        
        parser = AlternativeParser()
        results = parser.parse_keyword("кофемашина", "requests")
        
        if results:
            logger.info(f"✅ Alternative: найдено {len(results)} результатов")
            for i, result in enumerate(results[:2], 1):
                logger.info(f"  {i}. {result['title'][:50]}...")
            return True
        else:
            logger.warning("⚠️ Alternative: результаты не найдены")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка alternative: {e}")
        return False

def test_direct_request():
    """Тест прямого запроса к Google"""
    logger.info("🔍 Тест прямого запроса к Google")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Простой запрос
        url = "https://www.google.com/search?q=кофемашина&gl=kg&hl=ru&num=5"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Проверяем на капчу
            if "captcha" in response.text.lower():
                logger.warning("⚠️ Обнаружена капча")
                return False
            
            # Ищем результаты
            results = soup.find_all('div', class_='g')
            if results:
                logger.info(f"✅ Прямой запрос: найдено {len(results)} результатов")
                return True
            else:
                logger.warning("⚠️ Прямой запрос: результаты не найдены")
                return False
        else:
            logger.error(f"❌ Прямой запрос вернул код: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка прямого запроса: {e}")
        return False

def test_proxy_request():
    """Тест запроса через прокси"""
    logger.info("🔍 Тест запроса через прокси")
    
    try:
        from utils.proxy_manager import proxy_manager
        
        session = proxy_manager.get_session()
        
        # Тестовый запрос
        test_url = "https://httpbin.org/ip"
        response = session.get(test_url, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ Прокси работает")
            logger.info(f"IP: {response.json().get('origin', 'unknown')}")
            return True
        else:
            logger.warning("⚠️ Прокси не работает")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка прокси: {e}")
        return False

def main():
    """Основная функция тестирования"""
    logger.info("🚀 Тестирование методов парсинга Google")
    
    tests = [
        ("Прямой запрос", test_direct_request),
        ("Прокси", test_proxy_request),
        ("Google Requests", test_google_requests),
        ("Google Selenium", test_google_selenium),
        ("Alternative Parser", test_alternative_parser),
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
        status = "✅ РАБОТАЕТ" if result else "❌ НЕ РАБОТАЕТ"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nРезультат: {passed}/{total} методов работает")
    
    if passed > 0:
        logger.info("🎉 Найден рабочий метод парсинга!")
    else:
        logger.error("❌ Все методы не работают")
        logger.info("Рекомендации:")
        logger.info("1. Настройте прокси в .env файле")
        logger.info("2. Получите API ключ ScraperAPI")
        logger.info("3. Увеличьте задержки между запросами")
    
    return passed > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 