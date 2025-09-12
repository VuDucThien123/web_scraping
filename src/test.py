from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # Tắt chế độ GUI - Graphical User Interface, chạy nền mà ko cần giao diện đồ hoạ
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage') # Tắt thông báo chrome đang được điều khiển (trong chế độ GUI)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://tuoitre.vn/")
print(driver.title)
print(driver.current_url)