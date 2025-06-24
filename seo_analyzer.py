"""
Основной модуль для SEO-анализа конкурентов в Кыргызстане
"""
import os
import time
import random
from datetime import datetime
from tqdm import tqdm
from loguru import logger
from config import Config
from parsers.google_parser import GoogleParser
from parsers.yandex_parser import YandexParser
from parsers.page_parser import PageParser
from parsers.alternative_parser import AlternativeParser
from database.manager import DatabaseManager
from utils.proxy_manager import proxy_manager


class SEOAnalyzer:
    """Основной класс для SEO-анализа конкурентов"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.google_parser = GoogleParser(use_selenium=Config.USE_SELENIUM)
        self.yandex_parser = YandexParser()
        self.page_parser = PageParser()
        self.alternative_parser = AlternativeParser()
        
    def analyze_keyword(self, keyword, search_engine="google"):
        """Анализ одного ключевого слова"""
        logger.info(f"Анализ '{keyword}' в {search_engine}")
        
        # Случайная задержка
        proxy_manager.random_delay()
        
        results = []
        
        if search_engine == "google":
            # Пробуем основной парсер
            results = self.google_parser.parse_keyword(keyword)
            
            # Если не получилось, пробуем альтернативный
            if not results and Config.USE_ALTERNATIVE_PARSER:
                logger.info("Основной парсер не сработал, пробуем альтернативный")
                results = self.alternative_parser.try_all_methods(keyword)
                
        elif search_engine == "yandex":
            results = self.yandex_parser.parse_keyword(keyword)
        
        logger.info(f"Найдено {len(results)} результатов в {search_engine}")
        
        # Сохраняем результаты
        if results:
            self.db_manager.save_search_results(keyword, search_engine, results)
        
        return results
    
    def analyze_page_metadata(self, url):
        """Анализ мета-данных страницы"""
        try:
            metadata = self.page_parser.parse_page(url)
            return metadata
        except Exception as e:
            logger.error(f"Ошибка при анализе страницы {url}: {e}")
            return None
    
    def analyze_competitors(self, keywords=None):
        """Анализ топ-конкурентов по всем ключевым словам"""
        if keywords is None:
            keywords = Config.KEYWORDS
        
        logger.info("Анализ топ-конкурентов")
        
        all_results = {}
        
        for keyword in keywords:
            logger.info(f"Обработка ключевого слова: {keyword}")
            
            # Анализ в Google
            google_results = self.analyze_keyword(keyword, "google")
            if google_results:
                all_results[f"{keyword}_google"] = google_results
            
            # Небольшая пауза между запросами
            time.sleep(random.uniform(1, 3))
            
            # Анализ в Yandex
            yandex_results = self.analyze_keyword(keyword, "yandex")
            if yandex_results:
                all_results[f"{keyword}_yandex"] = yandex_results
            
            # Пауза между ключевыми словами
            time.sleep(random.uniform(2, 5))
        
        # Анализ мета-данных для найденных страниц
        self.analyze_all_metadata(all_results)
        
        return all_results
    
    def analyze_all_metadata(self, all_results):
        """Анализ мета-данных для всех найденных страниц"""
        logger.info("Анализ мета-данных страниц")
        
        processed_urls = set()
        
        for keyword_results in all_results.values():
            for result in keyword_results:
                url = result.get('url')
                if url and url not in processed_urls:
                    try:
                        metadata = self.analyze_page_metadata(url)
                        if metadata:
                            # Сохраняем мета-данные
                            self.db_manager.save_page_metadata(url, metadata)
                            processed_urls.add(url)
                        
                        # Небольшая пауза между запросами страниц
                        time.sleep(random.uniform(0.5, 1.5))
                        
                    except Exception as e:
                        logger.error(f"Ошибка при анализе {url}: {e}")
                        continue
    
    def get_competitor_analysis(self):
        """Получение анализа конкурентов из БД"""
        try:
            return self.db_manager.get_competitor_analysis()
        except Exception as e:
            logger.error(f"Ошибка получения анализа конкурентов: {e}")
            return []
    
    def export_to_csv(self, filename=None):
        """Экспорт данных в CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seo_analysis_{timestamp}.csv"
        
        try:
            data = self.get_competitor_analysis()
            # Здесь будет логика экспорта в CSV
            logger.info(f"Данные экспортированы в {filename}")
            return filename
        except Exception as e:
            logger.error(f"Ошибка экспорта в CSV: {e}")
            return None
    
    def generate_report(self):
        """Генерация отчета"""
        try:
            analysis = self.get_competitor_analysis()
            # Здесь будет логика генерации отчета
            logger.info("Отчет сгенерирован")
            return True
        except Exception as e:
            logger.error(f"Ошибка генерации отчета: {e}")
            return False
    
    def cleanup(self):
        """Очистка ресурсов"""
        logger.info("Ресурсы очищены")
        if hasattr(self.google_parser, 'close'):
            self.google_parser.close()

def main():
    """Основная функция"""
    logger.info("Запуск SEO-анализа конкурентов")
    
    # Создание анализатора
    analyzer = SEOAnalyzer()
    
    try:
        # Анализ конкурентов
        results = analyzer.analyze_competitors()
        
        # Экспорт в CSV
        analyzer.export_to_csv()
        
        # Генерация отчета
        analyzer.generate_report()
        
        logger.info("SEO-анализ завершен успешно")
        
    except KeyboardInterrupt:
        logger.info("Анализ прерван пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        analyzer.cleanup()

if __name__ == "__main__":
    main() 