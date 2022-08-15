from logging import exception
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
import requests
import time
import datetime

# Precisa fazer o download do webdriver do chrome de acordo com a versão utilizada e colocar na mesma pasta do script
 # https://chromedriver.chromium.org/downloads

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-loggin'])
driver = webdriver.Chrome(options=options)

# Loop for vai até a página setada em  pagina_final
pagina_final = 12000
base_url = 'https://www.reclameaqui.com.br'
url = 'https://www.reclameaqui.com.br/empresa/petz/lista-reclamacoes/?pagina='
avaliadas_path = '&status=EVALUATED'
sleep(3)
lista_reclamacoes = []
colunas_lista_exportada = ['Status reclamacao','Local','Data','reclamacao id','Titulo','Reclamacao','data_resposta_empresa','resposta_empresa','link']

# Iteracao entre páginas e raspagem dos itens
try:
    for i in range(1, pagina_final):  
        driver.get(url + str(i) + avaliadas_path)
        bs_obj = bs(driver.page_source, 'html.parser')
        boxes = bs_obj.find_all('div', {'class': 'sc-1pe7b5t-0 bJdtis'})
        href_links = [box.find('a').get('href') for box in boxes]
        page_links = [f'{base_url}{link}' for link in href_links]
        sleep(2)
        print('\[\033[0;33m\]nova página')
        
        # Itens coletados
        for link in page_links:
            driver.get(link)
            bs_page =  bs(driver.page_source, 'html.parser')
            
            # Reclamacao
            status_reclamacao = bs_page.find('span', {'class': 'sc-1a60wwz-1' }).text
            local_cliente = bs_page.find('span', {'data-testid': 'complaint-location'}).text
            data_reclamacao = bs_page.find('span', {'data-testid': 'complaint-creation-date'}).text
            reclamacao_id = bs_page.find('span', {'data-testid': 'complaint-id'}).text
            titulo = bs_page.find('h1', {'data-testid':'complaint-title'}).text
            reclamacao = bs_page.find('p', {'data-testid':'complaint-description'}).text
            link = driver.current_url           
            
            if status_reclamacao == 'Resolvido':
                sleep(2)               
                resposta_empresa = bs_page.find('p', {'class':'sc-1o3atjt-4 JkSWX'}).text
                data_resposta_empresa = bs_page.find('span', {'class':'sc-1o3atjt-3 ipwWvs'}).text
                         
            elif status_reclamacao == 'Respondida':
                sleep(2)
                resposta_empresa = bs_page.find('p', {'class':'sc-1o3atjt-4 JkSWX'}).text
                data_resposta_empresa = bs_page.find('span', {'class':'sc-1o3atjt-3 ipwWvs'}).text
            
            elif status_reclamacao == 'Não resolvido':     
                continue

            else:
                continue                                                                    
        
            lista_reclamacoes.append([status_reclamacao, local_cliente,data_reclamacao,reclamacao_id,titulo,reclamacao,data_resposta_empresa,resposta_empresa,link])
            print(len(lista_reclamacoes), titulo, status_reclamacao)

except Exception as e:
    print('\033[0;31;47mPlanilha extraída com erro - ' + str(e))
    lista_reclamacoes_array = np.array(lista_reclamacoes)
    df_reclamacoes = pd.DataFrame(lista_reclamacoes_array, columns = list(colunas_lista_exportada))
    df_reclamacoes.to_excel("Petz_Reclame_Aqui_erro.xlsx")
   
finally:
# Extração 
    lista_reclamacoes_array = np.array(lista_reclamacoes)
    df_reclamacoes = pd.DataFrame(lista_reclamacoes_array, columns = list(colunas_lista_exportada))
    df_reclamacoes.to_excel("Petz_Reclame_Aqui.xlsx")
    print('\033[32;40mPlanilha extraída com sucesso')

