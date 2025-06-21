"""
Модуль базы данных для SEO-анализа
"""
from .models import *
from .manager import DatabaseManager, db_manager

__all__ = ['DatabaseManager', 'db_manager'] 