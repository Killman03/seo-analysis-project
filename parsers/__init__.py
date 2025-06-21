"""
Модуль парсеров для SEO-анализа
"""
from .google_parser import GoogleParser
from .yandex_parser import YandexParser
from .page_parser import PageParser

__all__ = ['GoogleParser', 'YandexParser', 'PageParser'] 