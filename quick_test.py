"""
Быстрый тест парсера Google с Selenium
"""
import sys
import os
from loguru import logger

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_test():
    """Быстрый тест парсера"""
    logger.info("🚀 Быстрый тест парсера Google")
    
    try:
        from parsers.google_parser import GoogleParser
        
        # Создаем парсер с Selenium
        parser = GoogleParser(use_selenium=True)
        
        # Тестируем один запрос
        keyword = "кофемашина Бишкек"
        logger.info(f"Тестируем запрос: {keyword}")
        
        results = parser.parse_keyword(keyword)
        
        if results:
            logger.info(f"✅ Успешно! Найдено {len(results)} результатов")
            
            # Показываем первые 3 результата
            for i, result in enumerate(results[:3], 1):
                logger.info(f"  {i}. {result['title']}")
                logger.info(f"     URL: {result['url']}")
                logger.info(f"     Домен: {result['domain']}")
                logger.info("")
            
            return True
        else:
            logger.error("❌ Результаты не найдены")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return False
    finally:
        # Закрываем браузер
        if 'parser' in locals():
            parser.close()

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1) 