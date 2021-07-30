from selenium import webdriver

path = "C:/Program Files (x86)/chromedriver.exe"
PAGE_URL = "https://sede.administracionespublicas.gob.es/"
driver = webdriver.Chrome(path)

driver.get(PAGE_URL)