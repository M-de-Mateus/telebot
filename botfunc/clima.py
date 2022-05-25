import requests


class Clima:
    def __init__(self):
        self.cidade = None
        self.api = 'Sua chave API'
        self.link = None

    # retorna a temperatura do local especificado
    def consultar_temperatura(self, cidade):
        self.cidade = cidade
        self.link = f"https://api.openweathermap.org/data/2.5/weather?q={self.cidade}&appid={self.api}&lang=pt_br"
        requisicao = requests.get(self.link)
        requisicao_dic = requisicao.json()
        if requisicao_dic['cod'] != '404':
            temperatura = requisicao_dic['main']['temp'] - 273.15
            return f'{temperatura:.0f}ºC'
        else:
            return '404'

    # retorna a temperatura máxima do local especificado
    def consultar_tempmax(self, cidade):
        self.cidade = cidade
        self.link = f"https://api.openweathermap.org/data/2.5/weather?q={self.cidade}&appid={self.api}&lang=pt_br"
        requisicao = requests.get(self.link)
        requisicao_dic = requisicao.json()
        if requisicao_dic['cod'] != '404':
            temp_max = requisicao_dic['main']['temp_max'] - 273.15
            return f'{temp_max:.0f}ºC'
        else:
            return '404'

    # retorna a temperatura mínima do local especificado
    def consultar_tempmin(self, cidade):
        self.cidade = cidade
        self.link = f"https://api.openweathermap.org/data/2.5/weather?q={self.cidade}&appid={self.api}&lang=pt_br"
        requisicao = requests.get(self.link)
        requisicao_dic = requisicao.json()
        if requisicao_dic['cod'] != '404':
            temp_min = requisicao_dic['main']['temp_min'] - 273.15
            return f'{temp_min:.0f}ºC'
        else:
            return '404'

    # retorna o clima do local especificado
    def consultar_descricao(self, cidade):
        self.cidade = cidade
        self.link = f"https://api.openweathermap.org/data/2.5/weather?q={self.cidade}&appid={self.api}&lang=pt_br"
        requisicao = requests.get(self.link)
        requisicao_dic = requisicao.json()
        if requisicao_dic['cod'] != '404':
            descricao = requisicao_dic['weather'][0]['description']
            return descricao
        else:
            return '404'

    # retorna a temperatura humidade do local especificado
    def consultar_umidade(self, cidade):
        self.cidade = cidade
        self.link = f"https://api.openweathermap.org/data/2.5/weather?q={self.cidade}&appid={self.api}&lang=pt_br"
        requisicao = requests.get(self.link)
        requisicao_dic = requisicao.json()
        if requisicao_dic['cod'] != '404':
            umidade = requisicao_dic['main']['humidity']
            return f'{umidade}%'
        else:
            return '404'
