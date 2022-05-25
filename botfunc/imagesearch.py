import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import random


class Gimage:
    @staticmethod
    # cria uma pasta para salvar as imagem
    def criar_pasta():
        folder_name = 'images'
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        return folder_name

    @staticmethod
    # acessa a pasta onde as imagens estão salvas e sorteia uma delas para mandar no grupo
    def sortear_imagem(pesquisa):
        imagens = []
        for _, _, arquivo in os.walk('images'):
            for line in arquivo:
                if pesquisa in line:
                    imagens.append(str(line))
            return random.choice(imagens)

    @staticmethod
    # remove as imagens da pasta onde foram salvas
    def remover_imagem(pesquisa):
        for _, _, arquivo in os.walk('images'):
            for line in arquivo:
                if pesquisa in line:
                    os.remove(f'images/{line}')
                    print(f'{line} removido!')

    def __init__(self):
        self.folder_name = Gimage.criar_pasta()
        self.chromePath = r'C:\Users\Mateu\Desktop\pastas\telebot\driver\chromedriver.exe'

    # indica a pasta para o salvamento das imagens e o nome com o qual elas serão salvas
    def download_image(self, url, num, pesquisa):
        # faz download da imagem
        reponse = requests.get(url)
        if reponse.status_code == 200:
            with open(os.path.join(self.folder_name, str(num) + pesquisa + ".jpg"), 'wb') as file:
                file.write(reponse.content)

    # abre a página do google imagens e pesquisa o termo solicitado pelo usuário
    def pesquisar(self, pesquisa):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=self.chromePath, options=options)
        search_URL = f"https://www.google.com/search?q={pesquisa}&source=lnms&tbm=isch"
        driver.get(search_URL)

        # identifica os containers onde estão as imagens
        page_html = driver.page_source
        pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
        containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})
        len_containers = len(containers)

        # percorre o número de containers encontrado
        for i in range(1, len_containers + 1):
            # pula um container a cada 25, pois esse não possuem imagens
            if i % 25 == 0:
                continue
            # determina quantas imagens o código irá baixar, quanto menos imagens mais rápido
            elif i > 10:
                break
            else:
                # percorre os containers com as imagens e espera elas carregarem a melhor resolução antes de baixa-las
                xPath = f"""//*[@id="islrg"]/div[1]/div[{i}]"""
                previewImageXPath = f"""//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img"""
                previewImageElement = driver.find_element(by=By.XPATH, value=previewImageXPath)
                previewImageURL = previewImageElement.get_attribute("src")
                # clica na imagem para abri-la, para acessar o link que não esta encripitado pelo google
                driver.find_element(by=By.XPATH, value=xPath).click()

                # determina o horário em que a execução do download começou
                timeStarted = time.time()
                while True:
                    imageElement = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz
                    /div/div[1]/div[1]/div[3]/div/a/img""")
                    imageURL = imageElement.get_attribute('src')
                    if imageURL != previewImageURL:
                        break
                    else:
                        # define o começo da espera para a imagem carregar na resolução correta
                        currentTime = time.time()
                        # se o tempo for superior a 10s o código retorta timeout e baixa a imagem em baixa resolução
                        if currentTime - timeStarted > 10:
                            print("Timeout!")
                            break
                # baixando a imagem
                try:
                    self.download_image(imageURL, i, pesquisa)
                    print(f"Baixando a imagem {i} de {len_containers + 1} imagens. URL: {imageURL}")
                except (ValueError, Exception):
                    print(f"Não conseguimos baixar a imagem {i}!")

    def imagem_anime(self, pesquisa):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('start-maximized')
        drive = webdriver.Chrome(executable_path=self.chromePath, options=options)
        drive.get(f'https://kitsu.io/anime?text={pesquisa}')
        time.sleep(5)
        soup = bs4.BeautifulSoup(drive.page_source, 'html.parser')
        soup = soup.find('img', class_="lazyloaded")
        soup = soup.get('src')
        image = requests.get(soup)
        with open(os.path.join(os.path.relpath(self.folder_name), pesquisa + ".jpg"), 'wb') as file:
            file.write(image.content)
