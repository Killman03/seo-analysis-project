"""
Быстрый запуск различных компонентов SEO-анализа
"""
import sys
import os
import argparse
from loguru import logger

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_analysis():
    """Запуск анализа"""
    from seo_analyzer import SEOAnalyzer
    
    logger.info("Запуск SEO-анализа")
    
    analyzer = SEOAnalyzer(use_selenium=True, parse_pages=True)
    
    try:
        # Анализ ключевых слов
        analyzer.analyze_keywords_batch()
        
        # Анализ конкурентов
        analyzer.analyze_competitors()
        
        # Экспорт результатов
        analyzer.export_results()
        
        logger.info("Анализ завершен успешно")
        
    except Exception as e:
        logger.error(f"Ошибка анализа: {e}")
    finally:
        analyzer.cleanup()

def run_dashboard():
    """Запуск дашборда"""
    import subprocess
    import webbrowser
    import time
    
    logger.info("Запуск дашборда")
    
    try:
        # Запуск Streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
        # Открытие браузера через 3 секунды
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
        
        logger.info("Дашборд запущен на http://localhost:8501")
        logger.info("Нажмите Ctrl+C для остановки")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            logger.info("Дашборд остановлен")
            
    except Exception as e:
        logger.error(f"Ошибка запуска дашборда: {e}")

def run_test():
    """Запуск тестов"""
    from test_parser import main as test_main
    
    logger.info("Запуск тестов")
    test_main()

def run_simple_test():
    """Запуск простых тестов"""
    from simple_test import main as simple_test_main
    
    logger.info("Запуск простых тестов")
    simple_test_main()

def run_scheduler():
    """Запуск планировщика"""
    from scheduler import run_scheduler as scheduler_main
    
    logger.info("Запуск планировщика")
    scheduler_main()

def run_manual():
    """Ручной анализ"""
    from scheduler import run_manual_analysis
    
    logger.info("Запуск ручного анализа")
    run_manual_analysis()

def init_database():
    """Инициализация базы данных"""
    from database import db_manager
    
    logger.info("Инициализация базы данных")
    db_manager.init_database()
    logger.info("База данных инициализирована")

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description="SEO Анализ Конкурентов - Кыргызстан",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python run.py analysis     # Запуск анализа
  python run.py dashboard    # Запуск дашборда
  python run.py test         # Запуск тестов
  python run.py simple-test  # Простые тесты
  python run.py scheduler    # Запуск планировщика
  python run.py manual       # Ручной анализ
  python run.py init-db      # Инициализация БД
        """
    )
    
    parser.add_argument(
        "command",
        choices=["analysis", "dashboard", "test", "simple-test", "scheduler", "manual", "init-db"],
        help="Команда для выполнения"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Подробный вывод"
    )
    
    args = parser.parse_args()
    
    # Настройка логирования
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    
    # Выполнение команды
    if args.command == "analysis":
        run_analysis()
    elif args.command == "dashboard":
        run_dashboard()
    elif args.command == "test":
        run_test()
    elif args.command == "simple-test":
        run_simple_test()
    elif args.command == "scheduler":
        run_scheduler()
    elif args.command == "manual":
        run_manual()
    elif args.command == "init-db":
        init_database()

if __name__ == "__main__":
    main() 