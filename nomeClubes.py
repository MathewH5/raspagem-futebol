import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options

ligas = ["https://footystats.org/pt/portugal/liga-nos",
         "https://footystats.org/pt/brazil/serie-a",
         "https://footystats.org/pt/france/ligue-1",
         "https://footystats.org/pt/brazil/serie-a",
         "https://footystats.org/pt/netherlands/eredivisie",
         "https://footystats.org/pt/england/premier-league",
         "https://footystats.org/pt/germany/bundesliga",
         "https://footystats.org/pt/saudi-arabia/professional-league",
         "https://footystats.org/pt/spain/la-liga",
         "https://footystats.org/pt/argentina/primera-division",
         "https://footystats.org/pt/italy/serie-a"]  # Adicione mais nomes conforme necessário

for liga in ligas:

    driver = webdriver.Chrome()

    # Abrir a página da web
    driver.get(liga)

    try:
        botao_fechar = driver.find_element(By.CSS_SELECTOR, 'img[id="clever_40359_close_btn"]')
        if botao_fechar:
            botao_fechar.click()
    except NoSuchElementException:
        pass  # Lidar com a exceção caso a propaganda não seja encontrada
    #elemento = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Procurar Equipas e Ligas"]')
    #elemento.send_keys(liga)  # Usar o nome da lista
    #time_prcourado = liga
    #elemento.send_keys(Keys.RETURN)

    #time.sleep(2)

    #primeira_opcao = driver.find_element(By.CSS_SELECTOR, 'ul > li a.cf')
    #primeira_opcao.click()

    #time.sleep(3)

    page_source = driver.page_source

    site = BeautifulSoup(page_source, 'html.parser')

    links_elementos = driver.find_elements(By.CSS_SELECTOR, 'td.team.borderRightContent a.bold')
    links = [link.get_attribute('href') for link in links_elementos]
    print(links)

    dic_time = {'time':[], 'vitoria':[], 'empates':[], 'derrotas':[], 'golsFeitos':[], 'golsTomados':[], 'over1.5':[], 'over2.5':[],'mediaGols':[], 'link':links}

    liga_name_element = driver.find_element(By.CSS_SELECTOR, 'h1.fs14e')
    liga_prcourado = liga_name_element.text.strip()

    tabela = site.find('div', attrs={'class': 'table-wrapper'})
    tbody = tabela.find('tbody')
    time = tbody.findAll('tr')

    contador = 0
    print(time)
    for jogo in time:
        #nome = jogo.find('td', attrs={'class': 'team borderRightContent'}).find('a').get_text().strip()
        #nome = jogo.find_element(By.CSS_SELECTOR, 'td.team > a.bold').text.strip()
        #vitoria = jogo.find_element(By.CSS_SELECTOR, 'td.win').get_text().strip()
        #empates = jogo.find_element(By.CSS_SELECTOR, 'td.draw').get_text().strip()
        #derrotas = jogo.find_element(By.CSS_SELECTOR, 'td.loss').get_text().strip()
        #gf = jogo.find_element(By.CSS_SELECTOR, 'td.gf').get_text().strip()
        #gc = jogo.find_element(By.CSS_SELECTOR, 'td.ga').get_text().strip()
        #over1_5 = jogo.find_element(By.CSS_SELECTOR, 'td.over15').get_text().strip()
        #over2_5 = jogo.find_element(By.CSS_SELECTOR, 'td.over25').get_text().strip()
        #mediaGols = jogo.find_element(By.CSS_SELECTOR, 'td.avg').get_text().strip()

        nome = jogo.find('td', class_='team borderRightContent').find('a', class_='bold').text
        vitorias = jogo.find('td', class_='win').text
        empates = jogo.find('td', class_='draw').text
        derrotas = jogo.find('td', class_='loss').text
        gf = jogo.find('td', class_='gf').text
        gc = jogo.find('td', class_='ga').text
        over15_elements = jogo.find_all('td', class_='over15')
        if len(over15_elements) >= 2:
            over1_5 = over15_elements[1].text
        else:
            over1_5 = "N/A"
        over2_5 = jogo.find('td', class_='over25').text
        mediaGols = jogo.find('td', class_='avg').text

        dic_time['time'].append(nome)
        dic_time['vitoria'].append(vitorias)
        dic_time['empates'].append(empates)
        dic_time['derrotas'].append(derrotas)
        dic_time['golsFeitos'].append(gf)
        dic_time['golsTomados'].append(gc)
        dic_time['over1.5'].append(over1_5)
        dic_time['over2.5'].append(over2_5)
        dic_time['mediaGols'].append(mediaGols)

        print("Time #", contador + 1)
        print("Nome:", nome)
        print("Vitórias:", vitorias)
        print("Empates:", empates)
        print("Derrotas:", derrotas)
        print("Gols Feitos:", gf)
        print("Gols Tomados:", gc)
        print("Over 1.5:", over1_5)
        print("Over 2.5:", over2_5)
        print("Média de Gols:", mediaGols)
        # Resto do seu código

        # No final do loop, incremente o contador
        contador += 1

    df = pd.DataFrame(dic_time)
    # Suponhamos que você tenha um valor para 'elemento.send_keys' como 'cruzeiro'
    nome_do_arquivo = f'C:/Users/mathe/Downloads/{liga_prcourado}_historico.csv'
    # Em seguida, use o nome_do_arquivo na chamada df.to_csv
    df.to_csv(nome_do_arquivo, encoding='utf-8-sig', sep=',', index=False)


