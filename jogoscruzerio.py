import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

URL = "https://footystats.org/pt/clubs/cruzeiro-ec-613"

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

site = requests.get(URL, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

dic_informacoes= {'casa':[], 'gols':[], 'visitante':[]}


jogos = soup.findAll('div', attrs={'class': 'matchHistoryEvent'})

for jogo in jogos:
    casa = jogo.find('div', attrs={'class': 'homeTeamInfo'})
    Home_team_text = casa.find('p', attrs={'class': 'fs09e'}).get_text().strip()
    gols = jogo.find('span', class_=re.compile('black')).get_text().strip()
    visitante = jogo.find('div', itemprop='awayTeam')
    away_team_text=visitante.find('p', class_='fs09e').get_text().strip()

    print(Home_team_text, gols, away_team_text)