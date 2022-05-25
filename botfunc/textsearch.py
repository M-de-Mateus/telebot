import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class Insta:
    def __init__(self):
        self.chromePath = r'chromedriver.exe'

    def pesquisar(self, pesquisa):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        drive = webdriver.Chrome(executable_path=self.chromePath, chrome_options=options)
        drive.get('https://www.all-hashtag.com/')
        sleep(10)
        drive.find_element(By.ID, 'keyword').send_keys(f'{pesquisa}')
        drive.find_element(By.ID, 'keyword').send_keys(Keys.ENTER)
        sleep(3)
        soup = bs4.BeautifulSoup(drive.page_source, 'html.parser')
        soup = soup.find(id='copy-hashtags')
        texto = soup.get_text()
        return texto
