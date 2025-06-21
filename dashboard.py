"""
Интерактивный дашборд для SEO-анализа конкурентов
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from database import db_manager
from config import Config

# Настройка страницы
st.set_page_config(
    page_title="SEO Анализ Конкурентов - Кыргызстан",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Заголовок
st.title("📊 SEO Анализ Конкурентов - Кыргызстан")
st.markdown("---")

# Боковая панель
st.sidebar.header("⚙️ Настройки")

# Выбор периода
period = st.sidebar.selectbox(
    "Период анализа:",
    ["Последние 7 дней", "Последние 30 дней", "Последние 90 дней", "Все время"],
    index=0
)

# Выбор поисковой системы
search_engine = st.sidebar.selectbox(
    "Поисковая система:",
    ["Все", "Google", "Yandex"],
    index=0
)

# Функция получения данных
def get_analysis_data(days=7):
    """Получение данных анализа"""
    try:
        data = db_manager.get_recent_analysis(days=days)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Ошибка получения данных: {e}")
        return pd.DataFrame()

def get_competitors_data():
    """Получение данных конкурентов"""
    try:
        data = db_manager.get_competitors_analysis(limit=20)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Ошибка получения данных конкурентов: {e}")
        return pd.DataFrame()

# Основной контент
tab1, tab2, tab3, tab4 = st.tabs(["📈 Обзор", "🏆 Конкуренты", "🔍 Ключевые слова", "📋 Отчеты"])

with tab1:
    st.header("📈 Общий обзор")
    
    # Получение данных
    days_map = {"Последние 7 дней": 7, "Последние 30 дней": 30, "Последние 90 дней": 90, "Все время": 365}
    df = get_analysis_data(days_map[period])
    
    if not df.empty:
        # Фильтрация по поисковой системе
        if search_engine != "Все":
            engine_filter = "google" if search_engine == "Google" else "yandex"
            df = df[df['search_engine'] == engine_filter]
        
        # Статистика
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Всего результатов", len(df))
        
        with col2:
            unique_domains = df['domain'].nunique()
            st.metric("Уникальных доменов", unique_domains)
        
        with col3:
            avg_position = df['position'].mean()
            st.metric("Средняя позиция", f"{avg_position:.1f}")
        
        with col4:
            top_10_count = len(df[df['position'] <= 10])
            st.metric("Топ-10 позиций", top_10_count)
        
        # График позиций
        st.subheader("Распределение позиций")
        fig_positions = px.histogram(
            df, 
            x='position', 
            nbins=20,
            title="Распределение позиций в поисковой выдаче"
        )
        fig_positions.update_layout(xaxis_title="Позиция", yaxis_title="Количество")
        st.plotly_chart(fig_positions, use_container_width=True)
        
        # Топ доменов
        st.subheader("Топ доменов по количеству позиций")
        domain_stats = df.groupby('domain').agg({
            'position': ['count', 'mean']
        }).round(2)
        domain_stats.columns = ['Количество позиций', 'Средняя позиция']
        domain_stats = domain_stats.sort_values('Количество позиций', ascending=False).head(10)
        
        fig_domains = px.bar(
            domain_stats.reset_index(),
            x='domain',
            y='Количество позиций',
            title="Топ-10 доменов по количеству позиций"
        )
        fig_domains.update_layout(xaxis_title="Домен", yaxis_title="Количество позиций")
        st.plotly_chart(fig_domains, use_container_width=True)
        
        # Таблица с данными
        st.subheader("Последние результаты")
        st.dataframe(
            df[['keyword', 'search_engine', 'position', 'domain', 'title', 'created_at']].head(20),
            use_container_width=True
        )
    else:
        st.warning("Нет данных для отображения")

with tab2:
    st.header("🏆 Анализ конкурентов")
    
    competitors_df = get_competitors_data()
    
    if not competitors_df.empty:
        # Метрики конкурентов
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_competitor = competitors_df.iloc[0]
            st.metric("Лучший конкурент", top_competitor['domain'])
        
        with col2:
            total_positions = competitors_df['total_positions'].sum()
            st.metric("Всего позиций", total_positions)
        
        with col3:
            avg_positions = competitors_df['avg_position'].mean()
            st.metric("Средняя позиция", f"{avg_positions:.1f}")
        
        # График конкурентов
        st.subheader("Топ конкурентов")
        fig_competitors = px.bar(
            competitors_df.head(15),
            x='domain',
            y=['total_positions', 'top_3_positions', 'top_10_positions'],
            title="Анализ конкурентов",
            barmode='group'
        )
        fig_competitors.update_layout(xaxis_title="Домен", yaxis_title="Количество позиций")
        st.plotly_chart(fig_competitors, use_container_width=True)
        
        # Круговая диаграмма
        st.subheader("Распределение позиций")
        fig_pie = px.pie(
            competitors_df.head(10),
            values='total_positions',
            names='domain',
            title="Доля позиций топ-10 конкурентов"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Таблица конкурентов
        st.subheader("Детальная таблица конкурентов")
        st.dataframe(competitors_df, use_container_width=True)
    else:
        st.warning("Нет данных о конкурентах")

with tab3:
    st.header("🔍 Анализ ключевых слов")
    
    # Поиск по ключевому слову
    keyword_search = st.text_input("Поиск по ключевому слову:")
    
    if keyword_search:
        # Получение позиций по ключевому слову
        google_positions = db_manager.get_keyword_positions(keyword_search, 'google')
        yandex_positions = db_manager.get_keyword_positions(keyword_search, 'yandex')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Google")
            if google_positions:
                google_df = pd.DataFrame(google_positions)
                fig_google = px.bar(
                    google_df,
                    x='domain',
                    y='position',
                    title=f"Позиции в Google для '{keyword_search}'",
                    color='position',
                    color_continuous_scale='RdYlGn_r'
                )
                fig_google.update_layout(xaxis_title="Домен", yaxis_title="Позиция")
                st.plotly_chart(fig_google, use_container_width=True)
                
                st.dataframe(google_df, use_container_width=True)
            else:
                st.info("Нет данных для Google")
        
        with col2:
            st.subheader("Yandex")
            if yandex_positions:
                yandex_df = pd.DataFrame(yandex_positions)
                fig_yandex = px.bar(
                    yandex_df,
                    x='domain',
                    y='position',
                    title=f"Позиции в Yandex для '{keyword_search}'",
                    color='position',
                    color_continuous_scale='RdYlGn_r'
                )
                fig_yandex.update_layout(xaxis_title="Домен", yaxis_title="Позиция")
                st.plotly_chart(fig_yandex, use_container_width=True)
                
                st.dataframe(yandex_df, use_container_width=True)
            else:
                st.info("Нет данных для Yandex")
    
    # Статистика ключевых слов
    st.subheader("Статистика ключевых слов")
    
    df = get_analysis_data(days_map[period])
    if not df.empty:
        keyword_stats = df.groupby('keyword').agg({
            'position': ['count', 'mean', 'min']
        }).round(2)
        keyword_stats.columns = ['Количество позиций', 'Средняя позиция', 'Лучшая позиция']
        keyword_stats = keyword_stats.sort_values('Количество позиций', ascending=False)
        
        fig_keywords = px.scatter(
            keyword_stats.reset_index(),
            x='Средняя позиция',
            y='Количество позиций',
            size='Количество позиций',
            hover_data=['keyword'],
            title="Анализ ключевых слов"
        )
        st.plotly_chart(fig_keywords, use_container_width=True)
        
        st.dataframe(keyword_stats, use_container_width=True)

with tab4:
    st.header("📋 Отчеты и экспорт")
    
    # Генерация отчета
    if st.button("🔄 Сгенерировать новый отчет"):
        with st.spinner("Генерация отчета..."):
            try:
                report_file = db_manager.generate_report()
                if report_file:
                    st.success(f"Отчет сгенерирован: {report_file}")
                    
                    # Загрузка отчета
                    with open(report_file, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)
                    
                    st.json(report_data)
                else:
                    st.error("Ошибка генерации отчета")
            except Exception as e:
                st.error(f"Ошибка: {e}")
    
    # Экспорт данных
    st.subheader("Экспорт данных")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Экспорт в CSV"):
            with st.spinner("Экспорт данных..."):
                try:
                    csv_file = db_manager.export_results()
                    if csv_file:
                        st.success(f"Данные экспортированы: {csv_file}")
                        
                        # Скачивание файла
                        with open(csv_file, 'r', encoding='utf-8') as f:
                            csv_data = f.read()
                        
                        st.download_button(
                            label="📥 Скачать CSV",
                            data=csv_data,
                            file_name=os.path.basename(csv_file),
                            mime="text/csv"
                        )
                    else:
                        st.error("Ошибка экспорта")
                except Exception as e:
                    st.error(f"Ошибка: {e}")
    
    with col2:
        if st.button("📈 Экспорт конкурентов"):
            with st.spinner("Экспорт данных конкурентов..."):
                try:
                    competitors_df = get_competitors_data()
                    if not competitors_df.empty:
                        csv_file = db_manager.export_to_csv(
                            f"competitors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            competitors_df.to_dict('records')
                        )
                        if csv_file:
                            st.success(f"Данные конкурентов экспортированы: {csv_file}")
                        else:
                            st.error("Ошибка экспорта")
                    else:
                        st.warning("Нет данных для экспорта")
                except Exception as e:
                    st.error(f"Ошибка: {e}")
    
    # Настройки
    st.subheader("⚙️ Настройки системы")
    
    st.info(f"""
    **Конфигурация:**
    - Регион Google: {Config.GOOGLE_REGION}
    - Регион Yandex: {Config.YANDEX_REGION}
    - Максимум результатов: {Config.MAX_RESULTS}
    - Задержка: {Config.DELAY_MIN}-{Config.DELAY_MAX} сек
    - Использование прокси: {Config.USE_PROXY}
    """)

# Футер
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>SEO Анализ Конкурентов - Кыргызстан | Разработано для анализа регионального SEO</p>
    </div>
    """,
    unsafe_allow_html=True
)

