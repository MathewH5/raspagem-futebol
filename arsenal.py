from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configurar o WebDriver (neste caso, Chrome)
driver = webdriver.Chrome()

# Abrir a página da web
driver.get('https://footystats.org/pt/clubs/arsenal-fc-59')

# Aguardar algum tempo para que o conteúdo dinâmico seja carregado (você pode ajustar o tempo conforme necessário)
import time
time.sleep(5)

# Obter o código-fonte da página após o carregamento dinâmico
page_source = driver.page_source

# Fechar o WebDriver
driver.quit()

# Analisar a página usando BeautifulSoup
site = BeautifulSoup(page_source, 'html.parser')

# Agora você pode buscar os elementos no site
partida = site.findAll('li', {'class': 'matchHistoryEvent'})

for jogo in partida:
    casa = jogo.find('div', attrs={'class': 'homeTeamInfo'})
    Home_team_text = casa.find('p', attrs={'class': 'fs09e'}).get_text().strip()
    visitante = jogo.find('div', itemprop='awayTeam')
    away_team_text=visitante.find('p', class_='fs09e').get_text().strip()

    resultado = jogo.find('div', attrs={'class': 'scoreline'})
    gols_element = resultado.find('span', attrs={'class': 'black'}) if resultado else None
    if gols_element:
        gols = gols_element.get_text().strip()
        print(Home_team_text, gols, away_team_text)
    #else:
        #gols = " - "  # Ou qualquer mensagem que você preferir




#print(partida)
