"""
Скрипт для автоматизации SEO-анализа
"""
import schedule
import time
import os
import sys
from datetime import datetime
from loguru import logger
from seo_analyzer import SEOAnalyzer
from config import Config

def run_daily_analysis():
    """Ежедневный анализ"""
    logger.info("Запуск ежедневного SEO-анализа")
    
    try:
        # Создание анализатора
        analyzer = SEOAnalyzer(use_selenium=False, parse_pages=True)
        
        # Анализ ключевых слов
        analyzer.analyze_keywords_batch()
        
        # Анализ конкурентов
        analyzer.analyze_competitors()
        
        # Экспорт результатов
        analyzer.export_results()
        
        # Генерация отчета
        analyzer.generate_report()
        
        logger.info("Ежедневный анализ завершен успешно")
        
    except Exception as e:
        logger.error(f"Ошибка ежедневного анализа: {e}")
    finally:
        try:
            analyzer.cleanup()
        except:
            pass

def run_weekly_analysis():
    """Еженедельный анализ с расширенными данными"""
    logger.info("Запуск еженедельного SEO-анализа")
    
    try:
        # Создание анализатора с Selenium для более детального анализа
        analyzer = SEOAnalyzer(use_selenium=True, parse_pages=True)
        
        # Расширенный анализ ключевых слов
        analyzer.analyze_keywords_batch()
        
        # Детальный анализ конкурентов
        competitors = analyzer.analyze_competitors(limit=50)
        
        # Экспорт расширенных результатов
        analyzer.export_results(f"weekly_analysis_{datetime.now().strftime('%Y%m%d')}.csv")
        
        # Генерация еженедельного отчета
        analyzer.generate_report()
        
        logger.info("Еженедельный анализ завершен успешно")
        
    except Exception as e:
        logger.error(f"Ошибка еженедельного анализа: {e}")
    finally:
        try:
            analyzer.cleanup()
        except:
            pass

def run_monthly_analysis():
    """Ежемесячный анализ с полным отчетом"""
    logger.info("Запуск ежемесячного SEO-анализа")
    
    try:
        # Создание анализатора
        analyzer = SEOAnalyzer(use_selenium=True, parse_pages=True)
        
        # Полный анализ всех ключевых слов
        analyzer.analyze_keywords_batch()
        
        # Полный анализ конкурентов
        competitors = analyzer.analyze_competitors(limit=100)
        
        # Экспорт полных результатов
        analyzer.export_results(f"monthly_analysis_{datetime.now().strftime('%Y%m')}.csv")
        
        # Генерация ежемесячного отчета
        analyzer.generate_report()
        
        logger.info("Ежемесячный анализ завершен успешно")
        
    except Exception as e:
        logger.error(f"Ошибка ежемесячного анализа: {e}")
    finally:
        try:
            analyzer.cleanup()
        except:
            pass

def setup_scheduler():
    """Настройка расписания"""
    # Ежедневный анализ в 9:00
    schedule.every().day.at("09:00").do(run_daily_analysis)
    
    # Еженедельный анализ по воскресеньям в 10:00
    schedule.every().sunday.at("10:00").do(run_weekly_analysis)
    
    # Ежемесячный анализ в первое число месяца в 11:00
    schedule.every().month.at("11:00").do(run_monthly_analysis)
    
    logger.info("Планировщик настроен:")
    logger.info("- Ежедневный анализ: 09:00")
    logger.info("- Еженедельный анализ: воскресенье 10:00")
    logger.info("- Ежемесячный анализ: первое число месяца 11:00")

def run_scheduler():
    """Запуск планировщика"""
    logger.info("Запуск планировщика SEO-анализа")
    setup_scheduler()
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Проверка каждую минуту
        except KeyboardInterrupt:
            logger.info("Планировщик остановлен пользователем")
            break
        except Exception as e:
            logger.error(f"Ошибка планировщика: {e}")
            time.sleep(300)  # Пауза 5 минут при ошибке

def run_manual_analysis():
    """Ручной запуск анализа"""
    logger.info("Ручной запуск SEO-анализа")
    
    try:
        analyzer = SEOAnalyzer(use_selenium=False, parse_pages=True)
        
        # Анализ только части ключевых слов для быстрого теста
        test_keywords = Config.KEYWORDS[:3]  # Первые 3 ключевых слова
        
        for keyword in test_keywords:
            analyzer.analyze_keyword(keyword, ['google'])
        
        analyzer.analyze_competitors(limit=10)
        analyzer.export_results("manual_test.csv")
        
        logger.info("Ручной анализ завершен")
        
    except Exception as e:
        logger.error(f"Ошибка ручного анализа: {e}")
    finally:
        try:
            analyzer.cleanup()
        except:
            pass

if __name__ == "__main__":
    # Проверка аргументов командной строки
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "daily":
            run_daily_analysis()
        elif command == "weekly":
            run_weekly_analysis()
        elif command == "monthly":
            run_monthly_analysis()
        elif command == "manual":
            run_manual_analysis()
        elif command == "scheduler":
            run_scheduler()
        else:
            print("Доступные команды:")
            print("  daily    - Ежедневный анализ")
            print("  weekly   - Еженедельный анализ")
            print("  monthly  - Ежемесячный анализ")
            print("  manual   - Ручной анализ (тест)")
            print("  scheduler - Запуск планировщика")
    else:
        # По умолчанию запускаем планировщик
        run_scheduler() 