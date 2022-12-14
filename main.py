from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
print('Working')
driver = webdriver.Chrome(options=options, executable_path=r'C:\webdrivers\chromedriver.exe')
driver.get('https://youtube.com')
print(driver.page_source)
driver.quit()