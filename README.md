# SEO Анализ Конкурентов - Кыргызстан

Комплексная программа для парсинга SEO-данных топовых конкурентов из Google и Яндекса с учетом региональных настроек Кыргызстана (Бишкек).

## 🚀 Возможности

### 📊 Сбор данных
- **Топ-10 доменов** по ключевым запросам
- **Мета-данные** (title, description, H1-H3)
- **Позиции в выдаче** с историей изменений
- **Анализ плотности ключевых слов**
- **Техническое SEO** (HTTPS, canonical, robots, schema)

### 🌍 Региональные настройки
- **Google**: `gl=kg` (Кыргызстан) и `hl=ru` (русский язык)
- **Yandex**: `lr=10363` (Бишкек)

### 🛡️ Обход блокировок
- Ротация User-Agent
- Поддержка прокси (ScraperAPI, Luminati)
- Случайные задержки между запросами
- Обработка капчи (2Captcha)

### 💾 Хранение данных
- **PostgreSQL** с оптимизированной схемой
- **CSV экспорт** для быстрого анализа
- **JSON отчеты** с детальной статистикой

### 🤖 Автоматизация
- **Ежедневный анализ** в 9:00
- **Еженедельный анализ** по воскресеньям
- **Ежемесячный анализ** с полным отчетом
- **Cron интеграция**

### 📈 Визуализация
- **Интерактивный дашборд** на Streamlit
- **Графики и диаграммы** (Plotly)
- **Реальное время** обновления данных

## 🏗️ Архитектура

```
seo-analysis-project/
├── config.py                 # Конфигурация
├── seo_analyzer.py           # Основной модуль анализа
├── dashboard.py              # Streamlit дашборд
├── scheduler.py              # Автоматизация
├── requirements.txt          # Зависимости
├── env_example.txt           # Пример переменных окружения
├── parsers/                  # Модули парсинга
│   ├── google_parser.py      # Парсер Google
│   ├── yandex_parser.py      # Парсер Yandex
│   └── page_parser.py        # Парсер страниц
├── database/                 # Модули БД
│   ├── models.py             # Модели данных
│   └── manager.py            # Менеджер БД
├── utils/                    # Утилиты
│   ├── logger.py             # Логирование
│   └── proxy_manager.py      # Управление прокси
├── data/                     # Экспортированные данные
│   ├── csv/                  # CSV файлы
│   └── reports/              # Отчеты
└── logs/                     # Логи
```

## 🛠️ Установка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd seo-analysis-project
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка базы данных
```bash
# Установка PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Создание базы данных
sudo -u postgres createdb seo_analysis
sudo -u postgres createuser seo_user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE seo_analysis TO seo_user;"
```

### 4. Настройка переменных окружения
```bash
cp env_example.txt .env
# Отредактируйте .env файл с вашими настройками
```

### 5. Инициализация базы данных
```bash
python -c "from database import db_manager; db_manager.init_database()"
```

## 🚀 Использование

### Быстрый старт
```bash
# Ручной анализ (тест)
python scheduler.py manual

# Запуск дашборда
streamlit run dashboard.py

# Автоматический планировщик
python scheduler.py scheduler
```

### Команды планировщика
```bash
python scheduler.py daily      # Ежедневный анализ
python scheduler.py weekly     # Еженедельный анализ
python scheduler.py monthly    # Ежемесячный анализ
python scheduler.py manual     # Ручной анализ
python scheduler.py scheduler  # Запуск планировщика
```

### Настройка Cron
```bash
# Ежедневный анализ в 9:00
0 9 * * * cd /path/to/project && python scheduler.py daily

# Еженедельный анализ по воскресеньям в 10:00
0 10 * * 0 cd /path/to/project && python scheduler.py weekly

# Ежемесячный анализ в первое число месяца в 11:00
0 11 1 * * cd /path/to/project && python scheduler.py monthly
```

## 📊 Дашборд

Запустите дашборд командой:
```bash
streamlit run dashboard.py
```

### Возможности дашборда:
- **📈 Общий обзор** - статистика и графики
- **🏆 Конкуренты** - анализ топ-конкурентов
- **🔍 Ключевые слова** - детальный анализ запросов
- **📋 Отчеты** - экспорт и генерация отчетов

## ⚙️ Конфигурация

### Основные настройки (config.py)
```python
# Региональные настройки
GOOGLE_REGION = "kg"      # Кыргызстан
GOOGLE_LANGUAGE = "ru"    # Русский язык
YANDEX_REGION = "10363"   # Бишкек

# Настройки парсинга
MAX_RESULTS = 10          # Количество результатов
DELAY_MIN = 2            # Минимальная задержка
DELAY_MAX = 5            # Максимальная задержка
```

### Ключевые запросы
Добавьте свои ключевые слова в `config.py`:
```python
KEYWORDS = [
    "купить iPhone Бишкек",
    "кофемашина в Бишкеке",
    "доставка еды Бишкек",
    # Добавьте свои запросы
]
```

## 🔧 Настройка прокси

### ScraperAPI
```python
# В .env файле
SCRAPER_API_KEY=your_api_key_here
USE_PROXY=True
```

### Собственные прокси
```python
# В .env файле
PROXY_LIST=proxy1:port:user:pass,proxy2:port:user:pass
USE_PROXY=True
```

## 📈 Структура базы данных

### Основные таблицы:
- **keywords** - ключевые слова
- **search_results** - результаты поиска
- **page_data** - мета-данные страниц
- **competitors** - информация о конкурентах
- **backlinks** - обратные ссылки
- **analysis_sessions** - сессии анализа

## 🛡️ Безопасность

- Ротация User-Agent
- Случайные задержки
- Поддержка прокси
- Обработка капчи
- Логирование всех операций

## 📝 Логирование

Логи сохраняются в `logs/seo_parser.log`:
- Ротация файлов (10 MB)
- Хранение 30 дней
- Сжатие в ZIP

## 🔄 Автоматизация

### Airflow DAG (опционально)
```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'seo_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('seo_analysis', default_args=default_args, schedule_interval='0 9 * * *')

daily_analysis = PythonOperator(
    task_id='daily_seo_analysis',
    python_callable=run_daily_analysis,
    dag=dag,
)
```

## 🐛 Устранение неполадок

### Частые проблемы:

1. **Ошибка подключения к БД**
   - Проверьте настройки в `.env`
   - Убедитесь, что PostgreSQL запущен

2. **Блокировка от поисковых систем**
   - Увеличьте задержки в `config.py`
   - Настройте прокси
   - Используйте Selenium

3. **Ошибки парсинга**
   - Проверьте логи в `logs/`
   - Обновите селекторы в парсерах

## 📞 Поддержка

Для вопросов и предложений создавайте Issues в репозитории.

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей.

---

**Разработано для анализа регионального SEO в Кыргызстане** 🇰🇬
