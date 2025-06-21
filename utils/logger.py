"""
Модуль логирования для SEO-парсера
"""
import os
import sys
from loguru import logger
from config import Config

def setup_logger():
    """Настройка логирования"""
    # Создаем директорию для логов если её нет
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
    
    # Удаляем стандартный обработчик
    logger.remove()
    
    # Добавляем обработчик для консоли
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=Config.LOG_LEVEL,
        colorize=True
    )
    
    # Добавляем обработчик для файла
    logger.add(
        Config.LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=Config.LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    return logger

# Инициализируем логгер
setup_logger() 