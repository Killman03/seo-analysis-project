"""
Модели базы данных для SEO-анализа
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import Config

Base = declarative_base()

class Keyword(Base):
    """Модель ключевых слов"""
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    keyword = Column(String(500), nullable=False, index=True)
    search_engine = Column(String(50), nullable=False)  # google, yandex
    region = Column(String(50), nullable=False)  # kg, 10363
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    search_results = relationship("SearchResult", back_populates="keyword")

class SearchResult(Base):
    """Модель результатов поиска"""
    __tablename__ = 'search_results'
    
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), nullable=False)
    position = Column(Integer, nullable=False)
    title = Column(String(1000), nullable=False)
    url = Column(String(2000), nullable=False)
    domain = Column(String(500), nullable=False)
    description = Column(Text)
    search_engine = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    keyword = relationship("Keyword", back_populates="search_results")
    page_data = relationship("PageData", back_populates="search_result", uselist=False)

class PageData(Base):
    """Модель данных страницы"""
    __tablename__ = 'page_data'
    
    id = Column(Integer, primary_key=True)
    search_result_id = Column(Integer, ForeignKey('search_results.id'), nullable=False)
    title = Column(String(1000))
    description = Column(Text)
    keywords = Column(Text)
    h1_tags = Column(Text)  # JSON array
    h2_tags = Column(Text)  # JSON array
    h3_tags = Column(Text)  # JSON array
    word_count = Column(Integer, default=0)
    images_count = Column(Integer, default=0)
    links_count = Column(Integer, default=0)
    
    # Техническое SEO
    has_title = Column(Boolean, default=False)
    has_description = Column(Boolean, default=False)
    has_keywords = Column(Boolean, default=False)
    has_h1 = Column(Boolean, default=False)
    has_images_with_alt = Column(Boolean, default=False)
    has_canonical = Column(Boolean, default=False)
    has_robots = Column(Boolean, default=False)
    has_schema = Column(Boolean, default=False)
    is_https = Column(Boolean, default=False)
    
    # Анализ ключевых слов
    keyword_density = Column(Float, default=0.0)
    keyword_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    search_result = relationship("SearchResult", back_populates="page_data")

class Competitor(Base):
    """Модель конкурентов"""
    __tablename__ = 'competitors'
    
    id = Column(Integer, primary_key=True)
    domain = Column(String(500), nullable=False, unique=True, index=True)
    name = Column(String(500))
    description = Column(Text)
    website_url = Column(String(2000))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Статистика
    total_positions = Column(Integer, default=0)
    avg_position = Column(Float, default=0.0)
    top_3_positions = Column(Integer, default=0)
    top_10_positions = Column(Integer, default=0)

class Backlink(Base):
    """Модель обратных ссылок"""
    __tablename__ = 'backlinks'
    
    id = Column(Integer, primary_key=True)
    competitor_id = Column(Integer, ForeignKey('competitors.id'), nullable=False)
    source_url = Column(String(2000), nullable=False)
    target_url = Column(String(2000), nullable=False)
    anchor_text = Column(String(1000))
    domain_authority = Column(Float, default=0.0)
    page_authority = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    competitor = relationship("Competitor")

class AnalysisSession(Base):
    """Модель сессий анализа"""
    __tablename__ = 'analysis_sessions'
    
    id = Column(Integer, primary_key=True)
    session_name = Column(String(500), nullable=False)
    keywords_count = Column(Integer, default=0)
    results_count = Column(Integer, default=0)
    status = Column(String(50), default='running')  # running, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)

# Создание таблиц
def create_tables():
    """Создание всех таблиц в базе данных"""
    engine = create_engine(Config.DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

# Создание сессии
def get_session():
    """Получение сессии базы данных"""
    engine = create_engine(Config.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session() 