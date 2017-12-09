#	Diego Viana dos Santos
#	Script em Python que retorna consultas JSON utilizando o api Advisor da Climatempo. 
#	Após o retorno das consultas é realizada a exibição das informações retornadas por meio da biblioteca gráfica Tkinter

#!/usr/bin/env python3

import json, requests
from tkinter import *

#token para acesso a api Advisor da Climatempo
token = "coloque_aqui_o_token"

#Classe que manipula os objetos Previsão
class Previsao(object):
   
    def __init__(self, data, temp_min, temp_max, desc):
        self.__data = data
        self.__temp_min = temp_min
        self.__temp_max = temp_max
        self.__desc = desc
     
    def __repr__(self):
        return "Dia: %s | Temperatua Miníma: %s°C | Temperatua Máxima: %s°C | Descrição: %s" % (self.__data, self.__temp_min, self.__temp_max, self.__desc)
 
    def get_data(self):
        return self.__data
 
    def get_temp_min(self):
        return self.__temp_min

    def get_temp_max(self):
        return self.__temp_max

    def get_desc(self):
        return self.__desc

#Acesso a previsão da cidade
def busca_previsao(cod):
    url_previsao_atual = 'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/' + str(int(cod)) + '/current?token=' + token
    url_previsao = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/' + str(int(cod)) + '/days/15?token=' + token

    try:
        res = requests.get(url_previsao, stream=True)
        res1 = requests.get(url_previsao_atual, stream=True)
        
        dados = json.loads(res.text)
        dados1= json.loads(res1.text)
    
        lb3["text"] = " "
        lb3["bg"] = "green"
        lb3["text"] = "Busca da previsão realizada com sucesso!!!"
    
        previsao_total = dados['data']
        previsao_atual = dados1['data']

        lista = []
        for previsao_dia in previsao_total:
            data = previsao_dia['date_br']
            temp_min = previsao_dia['temperature']['min']
            temp_max = previsao_dia['temperature']['max']
            desc = previsao_dia['text_icon']['text']['phrase']['reduced']
    
            a = Previsao(data, temp_min, temp_max, desc)
            lista.append(a)
    
        textArea.insert(INSERT, dados['name'] + ", " + dados['state'] + " | Temperatua Atual : " + str(float(previsao_atual['temperature'])) + "°C | Descrição: " + previsao_atual['condition'])
        textArea.insert(INSERT, "\n\n")
        for l in lista:
            textArea.insert(INSERT, l)
            textArea.insert(INSERT, "\n")
        textArea.insert(INSERT, "\n")
    
    except requests.exceptions.RequestException as e:
        lb3["text"] = " "
        lb3["bg"] = "red"
        lb3["text"] = "Ocorreu um problema durante a busca da previsão do tempo!!!"
    
#Acesso ao id da cidade
def busca_id_cidade(cidade, estado):
    url_cod = 'http://apiadvisor.climatempo.com.br/api/v1/locale/city?name=' + cidade + '&state=' + estado + '&token=' + token

    try:
        res = requests.get(url_cod, stream=True)
    
        dados = json.loads(res.text)
        
        if len(dados) == 1:
            cod = dados[0]['id']
            busca_previsao(cod)
        else:
            lb3["text"] = " "
            lb3["bg"] = "red"
            lb3["text"] = "Ocorreu um problema durante a busca do id da cidade!!!"
    
    except requests.exceptions.RequestException as e:  
        lb3["text"] = " "
        lb3["bg"] = "red"
        lb3["text"] = "Ocorreu um problema durante a busca da previsão do tempo!!!"

def bt_click():
    cidade = ed1.get()
    estado = ed2.get()
    
    busca_id_cidade(cidade, estado)

#main
janela = Tk()

#Formato(Largura x Altura + distância da esquerda da tela + distância do topo da tela)
janela.geometry("1200x500+100+150")

janela.title("Previsão do tempo")
janela["bg"] = "silver"

#Labels
lb0 = Label(janela, text = "Previsão do tempo:", bg = "blue")
lb0.pack(side = TOP, fill = X)

lb1 = Label(janela, text = "Digite o nome da cidade:", bg = "silver")
lb1.place(x = 5, y = 20)

lb2 = Label(janela, text = "Digite a sigla do estado:", bg = "silver")
lb2.place(x = 500, y = 20)

lb3 = Label(janela, text = " ", bg = "silver")
lb3.place(x = 5, y = 60)

#Entrada de texto
ed1 = Entry(janela)
ed1.place(x = 165, y = 20)

ed2 = Entry(janela)
ed2.place(x = 660, y = 20)

#Botão
bt1 = Button(janela, text = "Buscar previsão!", command = bt_click)
bt1.place(x = 1000, y = 20)

#Área de Texto
textArea = Text(janela, width = 169)
textArea.place(x = 5, y = 100)

#Inicializa a janela
janela.mainloop()