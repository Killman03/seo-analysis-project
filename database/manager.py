"""
Менеджер базы данных для SEO-анализа
"""
import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, case
from loguru import logger
from config import Config
from database.models import (
    Base, Keyword, SearchResult, PageData, Competitor, 
    Backlink, AnalysisSession, create_tables, get_session
)

class DatabaseManager:
    """Менеджер базы данных"""
    
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        
    def init_database(self):
        """Инициализация базы данных"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("База данных инициализирована")
        except Exception as e:
            logger.error(f"Ошибка инициализации БД: {e}")
    
    def save_search_results(self, keyword, search_engine, region, results):
        """Сохранение результатов поиска"""
        session = self.Session()
        try:
            # Создаем или получаем ключевое слово
            keyword_obj = session.query(Keyword).filter_by(
                keyword=keyword,
                search_engine=search_engine,
                region=region
            ).first()
            
            if not keyword_obj:
                keyword_obj = Keyword(
                    keyword=keyword,
                    search_engine=search_engine,
                    region=region
                )
                session.add(keyword_obj)
                session.flush()
            
            # Сохраняем результаты поиска
            for result_data in results:
                search_result = SearchResult(
                    keyword_id=keyword_obj.id,
                    position=result_data['position'],
                    title=result_data['title'],
                    url=result_data['url'],
                    domain=result_data['domain'],
                    description=result_data.get('description', ''),
                    search_engine=search_engine
                )
                session.add(search_result)
                session.flush()
                
                # Сохраняем данные страницы если есть
                if 'page_data' in result_data and result_data['page_data']:
                    page_data = result_data['page_data']
                    page_obj = PageData(
                        search_result_id=search_result.id,
                        title=page_data.get('title', ''),
                        description=page_data.get('description', ''),
                        keywords=page_data.get('keywords', ''),
                        h1_tags=json.dumps(page_data.get('h1', []), ensure_ascii=False),
                        h2_tags=json.dumps(page_data.get('h2', []), ensure_ascii=False),
                        h3_tags=json.dumps(page_data.get('h3', []), ensure_ascii=False),
                        word_count=page_data.get('word_count', 0),
                        images_count=len(page_data.get('images', [])),
                        links_count=len(page_data.get('links', [])),
                        has_title=page_data.get('technical_seo', {}).get('has_title', False),
                        has_description=page_data.get('technical_seo', {}).get('has_description', False),
                        has_keywords=page_data.get('technical_seo', {}).get('has_keywords', False),
                        has_h1=page_data.get('technical_seo', {}).get('has_h1', False),
                        has_images_with_alt=page_data.get('technical_seo', {}).get('has_images_with_alt', False),
                        has_canonical=page_data.get('technical_seo', {}).get('has_canonical', False),
                        has_robots=page_data.get('technical_seo', {}).get('has_robots', False),
                        has_schema=page_data.get('technical_seo', {}).get('has_schema', False),
                        is_https=page_data.get('technical_seo', {}).get('is_https', False),
                        keyword_density=page_data.get('keyword_analysis', {}).get('keyword_density', 0.0),
                        keyword_count=page_data.get('keyword_analysis', {}).get('keyword_count', 0)
                    )
                    session.add(page_obj)
            
            session.commit()
            logger.info(f"Сохранено {len(results)} результатов для '{keyword}' в {search_engine}")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка сохранения результатов: {e}")
        finally:
            session.close()
    
    def get_competitors_analysis(self, limit=20):
        """Получение анализа конкурентов"""
        session = self.Session()
        try:
            # Агрегируем данные по доменам
            competitors_data = session.query(
                SearchResult.domain,
                func.count(SearchResult.id).label('total_positions'),
                func.avg(SearchResult.position).label('avg_position'),
                func.sum(case((SearchResult.position <= 3, 1), else_=0)).label('top_3_positions'),
                func.sum(case((SearchResult.position <= 10, 1), else_=0)).label('top_10_positions')
            ).group_by(SearchResult.domain).order_by(
                func.count(SearchResult.id).desc()
            ).limit(limit).all()
            
            return [
                {
                    'domain': row.domain,
                    'total_positions': row.total_positions,
                    'avg_position': float(row.avg_position) if row.avg_position else 0.0,
                    'top_3_positions': row.top_3_positions,
                    'top_10_positions': row.top_10_positions
                }
                for row in competitors_data
            ]
            
        except Exception as e:
            logger.error(f"Ошибка получения анализа конкурентов: {e}")
            return []
        finally:
            session.close()
    
    def get_keyword_positions(self, keyword, search_engine='google'):
        """Получение позиций по ключевому слову"""
        session = self.Session()
        try:
            results = session.query(SearchResult).join(Keyword).filter(
                Keyword.keyword == keyword,
                SearchResult.search_engine == search_engine
            ).order_by(SearchResult.position).all()
            
            return [
                {
                    'position': result.position,
                    'domain': result.domain,
                    'title': result.title,
                    'url': result.url,
                    'description': result.description
                }
                for result in results
            ]
            
        except Exception as e:
            logger.error(f"Ошибка получения позиций: {e}")
            return []
        finally:
            session.close()
    
    def get_recent_analysis(self, days=7):
        """Получение недавних анализов"""
        session = self.Session()
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            results = session.query(SearchResult).join(Keyword).filter(
                SearchResult.created_at >= cutoff_date
            ).order_by(SearchResult.created_at.desc()).all()
            
            return [
                {
                    'keyword': result.keyword.keyword,
                    'search_engine': result.search_engine,
                    'position': result.position,
                    'domain': result.domain,
                    'title': result.title,
                    'created_at': result.created_at.isoformat()
                }
                for result in results
            ]
            
        except Exception as e:
            logger.error(f"Ошибка получения недавних анализов: {e}")
            return []
        finally:
            session.close()
    
    def create_analysis_session(self, session_name, keywords_count):
        """Создание сессии анализа"""
        session = self.Session()
        try:
            analysis_session = AnalysisSession(
                session_name=session_name,
                keywords_count=keywords_count
            )
            session.add(analysis_session)
            session.commit()
            return analysis_session.id
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка создания сессии анализа: {e}")
            return None
        finally:
            session.close()
    
    def update_analysis_session(self, session_id, status, results_count=None, error_message=None):
        """Обновление статуса сессии анализа"""
        session = self.Session()
        try:
            analysis_session = session.query(AnalysisSession).filter_by(id=session_id).first()
            if analysis_session:
                analysis_session.status = status
                if results_count is not None:
                    analysis_session.results_count = results_count
                if error_message:
                    analysis_session.error_message = error_message
                if status in ['completed', 'failed']:
                    analysis_session.completed_at = datetime.utcnow()
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка обновления сессии анализа: {e}")
        finally:
            session.close()
    
    def export_to_csv(self, filename, data):
        """Экспорт данных в CSV"""
        import pandas as pd
        import os
        
        try:
            os.makedirs(Config.CSV_OUTPUT_DIR, exist_ok=True)
            filepath = os.path.join(Config.CSV_OUTPUT_DIR, filename)
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"Данные экспортированы в {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Ошибка экспорта в CSV: {e}")
            return None

# Глобальный экземпляр менеджера БД
db_manager = DatabaseManager() 