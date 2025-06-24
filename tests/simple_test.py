"""
Простой тест для проверки базовой функциональности
"""
import sys
import os
from loguru import logger

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Тест базовой функциональности"""
    logger.info("🧪 Тестирование базовой функциональности")
    
    try:
        # Тест импорта модулей
        from config import Config
        logger.info("✅ Конфигурация загружена")
        
        from utils import proxy_manager
        logger.info("✅ Менеджер прокси загружен")
        
        from database import db_manager
        logger.info("✅ Менеджер БД загружен")
        
        # Тест User-Agent
        user_agent = proxy_manager.get_random_user_agent()
        logger.info(f"✅ User-Agent: {user_agent[:50]}...")
        
        # Тест сессии
        session = proxy_manager.get_session()
        logger.info("✅ Сессия создана")
        
        # Тест конфигурации
        logger.info(f"✅ Google регион: {Config.GOOGLE_REGION}")
        logger.info(f"✅ Yandex регион: {Config.YANDEX_REGION}")
        logger.info(f"✅ Ключевых слов: {len(Config.KEYWORDS)}")
        
        # Тест простого запроса
        test_url = "https://httpbin.org/ip"
        try:
            response = session.get(test_url, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Тестовый запрос выполнен успешно")
            else:
                logger.warning(f"⚠️ Тестовый запрос вернул код: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Ошибка тестового запроса: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        return False

def test_google_parser_simple():
    """Простой тест парсера Google"""
    logger.info("🔍 Тестирование парсера Google")
    
    try:
        from parsers.google_parser import GoogleParser
        
        parser = GoogleParser(use_selenium=False)
        
        # Тестируем с простым запросом
        keyword = "кофемашина"
        results = parser.parse_keyword(keyword)
        
        if results:
            logger.info(f"✅ Найдено {len(results)} результатов")
            for i, result in enumerate(results[:2], 1):
                logger.info(f"  {i}. {result['title'][:50]}...")
        else:
            logger.warning("⚠️ Результаты не найдены (возможно блокировка)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка парсера Google: {e}")
        return False

def test_database_connection():
    """Тест подключения к базе данных"""
    logger.info("💾 Тестирование подключения к БД")
    
    try:
        from database import db_manager
        
        # Инициализация БД
        db_manager.init_database()
        logger.info("✅ База данных инициализирована")
        
        # Тест получения данных
        competitors = db_manager.get_competitors_analysis(limit=5)
        logger.info(f"✅ Получено {len(competitors)} записей конкурентов")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка БД: {e}")
        return False

def main():
    """Основная функция тестирования"""
    logger.info("🚀 Начинаем простое тестирование")
    
    tests = [
        ("Базовая функциональность", test_basic_functionality),
        ("Парсер Google", test_google_parser_simple),
        ("База данных", test_database_connection),
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
        logger.info("Система готова к работе!")
    else:
        logger.warning("⚠️ Некоторые тесты не пройдены")
        logger.info("Проверьте настройки и попробуйте снова")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 