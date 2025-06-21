"""
Модуль утилит для SEO-анализа
"""
from .logger import setup_logger
from .proxy_manager import ProxyManager, proxy_manager

__all__ = ['setup_logger', 'ProxyManager', 'proxy_manager'] 