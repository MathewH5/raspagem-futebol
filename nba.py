import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.nba.com/stats/players/traditional?dir=A&sort=TEAM_ABBREVIATION'

option = Options()
option.headless = True
driver = webdriver.Chrome()

driver.get(url)
time.sleep(5)

try:
    # Use um XPath mais específico para encontrar o elemento da coluna de PTS
    pts_column = driver.find_element_by_xpath("//div[@class='Crom_container__C45Ti crom-container']//table[@class='Crom_table__p1iZz']//thead//tr//th[@field='PTS']")
    if pts_column:
        pts_column.click()
        print("Clique na coluna PTS bem-sucedido.")
    else:
        print("Elemento da coluna PTS não encontrado.")
except Exception as e:
    print(f"Erro ao clicar na coluna PTS: {e}")

driver.quit()