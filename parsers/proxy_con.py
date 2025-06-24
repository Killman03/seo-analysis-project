from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def test_setup_selenium():
    """Тестовая функция для проверки работы Selenium с Chrome"""

    service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    # Базовые настройки
    # chrome_options.add_argument("--headless=new")  # Новый headless режим
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Настройки для обхода детекции
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-infobars")

    # Региональные настройки для Кыргызстана
    chrome_options.add_argument("--lang=ru-RU")  # Основной язык интерфейса
    chrome_options.add_argument("--timezone=Asia/Bishkek")  # Часовой пояс
    chrome_options.add_argument("--geo-location=lat=42.87,lon=74.59")  # Координаты Бишкека

    # Фиксированный user-agent (лучше не использовать случайные)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    url = "https://just-magic.org/serv/aqua.php"

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Задержка для загрузки страницы

    except Exception as e:
        print(f"Ошибка при открытии страницы: {e}")

    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    test_setup_selenium()
    print("Тест Selenium завершен успешно")