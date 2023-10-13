import pandas as pd
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
#options = Options()
#options.add_argument("window-size=400,800")

caminho_arquivo = "C:/Users/mathe/Downloads/nome-todos-os-times.csv"
df = pd.read_csv(caminho_arquivo)
nomes = df["time"]
#nomes = ["cruzeiro", "fluminense", "corinthians"]  # Adicione mais nomes conforme necessário

for nome in nomes:
    # Configurar o WebDriver (neste caso, Chrome)
    driver = webdriver.Chrome()

    # Abrir a página da web
    driver.get('https://footystats.org/pt/clubs/arsenal-fc-59')

    botao_fechar = driver.find_element(By.CSS_SELECTOR, 'img[id="clever_40359_close_btn"]')
    if botao_fechar:
        botao_fechar.click()

    elemento = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Procurar Equipas e Ligas"]')
    elemento.send_keys(nome)  # Usar o nome da lista
    time_prcourado = nome
    elemento.send_keys(Keys.RETURN)
    #elemento.send_keys('cruzeiro')
    #time_prcourado = "cruzeiro"
    #elemento.send_keys(Keys.RETURN)

    time.sleep(2)

    primeira_opcao = driver.find_element(By.CSS_SELECTOR, 'ul > li a.cf')
    primeira_opcao.click()

    time.sleep(3)

    resultado_link_element = driver.find_element(By.CSS_SELECTOR, 'li.matchHistoryEvent > div.matchData > div.scoreline.win-bg > a')

    # Obter o código-fonte da página após o carregamento dinâmico
    page_source = driver.page_source

    # Fechar o WebDriver


    site = BeautifulSoup(page_source, 'html.parser')

    links_elementos = driver.find_elements(By.CSS_SELECTOR, 'li.matchHistoryEvent > div.matchData > div.scoreline.win-bg > a, li.matchHistoryEvent > div.matchData > div.scoreline.draw-bg > a, li.matchHistoryEvent > div.matchData > div.scoreline.loss-bg > a')
    links = [link.get_attribute('href') for link in links_elementos]
    print(links)
    dic_historico = {'time-casa':[], 'gols':[], 'time-visitante':[], 'link':links}


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


            dic_historico['time-casa'].append(Home_team_text)
            dic_historico['gols'].append(gols)
            dic_historico['time-visitante'].append(away_team_text)
            #dic_historico['link'].append(links)

            #resultado_link_element.click()
            #time.sleep(2)  # Aguarde um curto período para carregar a página de detalhes da partida

            # Raspe as informações de estatísticas da página da partida
            #page_source_partida = driver.page_source
            #site_partida = BeautifulSoup(page_source_partida, 'html.parser')

            # Aqui, você deve adicionar a lógica para extrair as informações de estatísticas da página da partida
            # Substitua os seletores CSS pelo seletor real da página de detalhes da partida

            # Exemplo hipotético:
            #estatisticas = site_partida.find('seletor-das-estatisticas')
            #if estatisticas:
                #estatisticas_text = estatisticas.get_text()
                #print(estatisticas_text)

            # Volte para a lista de resultados
            #driver.back()
            #time.sleep(2)  # Aguarde um curto período para retornar à lista de resultados

        #else:
            #gols = " - "  # Ou qualquer mensagem que você preferir


    df = pd.DataFrame(dic_historico)
    # Suponhamos que você tenha um valor para 'elemento.send_keys' como 'cruzeiro'
    nome_do_arquivo = f'C:/Users/mathe/Downloads/historicoTimes/{time_prcourado}_historico.csv'

    df[['gols_casa', 'gols_visitante']] = df['gols'].str.split('-', expand=True)
    df['gols'] = df['gols'].str.replace('-', 'x')
    # Em seguida, use o nome_do_arquivo na chamada df.to_csv
    df.to_csv(nome_do_arquivo, encoding='utf-8-sig', sep=',', index=False)

    #print(partida)
    driver.quit()