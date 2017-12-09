#!/usr/bin/env python3

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import sys
import re
import json
import operator

arq = sys.argv[1]
ref_arquivo = open(arq,"r")

list = re.findall(r'SRC=[0-9.]*', ref_arquivo.read()) 

#Questão 1
print("Número total de pacotes: " + str(list.__len__()))
#Fim Questão 1

#Questão 2 
for i in range(0,list.__len__()):
    list[i]=list[i].replace('SRC=','')
    
# Lista de IPs sem repeticao
l = []
for i in range(0,list.__len__()):
    if list[i] not in l:
        l.append(list[i])

# Conta as repeticoes
inventario = {}
cont = 0
for ip_unico in l:
    for i in range(0,list.__len__()):
        if ip_unico == list[i]:
            cont += 1
    inventariob = {ip_unico: cont}
    inventario.update(inventariob)
    cont = 0

inventario = sorted(inventario.items(), key=operator.itemgetter(1), reverse=True)

cont = 0
for ip in inventario:
    if cont < 10:
        url = ("http://ipvigilante.com/"+ip[0]+"/full")
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data) 
        print("SRC=" + str(data["data"]["ipv4"]) + "  País=" + str(data["data"]["country_name"]) + "  Quantidade de pacotes=" + str(ip[1]))
        cont +=1

ref_arquivo.close()
#Fim Questão 2

#Questão 3
ref_arquivo = open(arq,"r")
list = re.findall(r'DST=[0-9.]*', ref_arquivo.read()) 

for i in range(0,list.__len__()):
    list[i]=list[i].replace('DST=','')
    
# Lista de IPs sem repeticao
l = []
for i in range(0,list.__len__()):
    if list[i] not in l:
        l.append(list[i])

# Conta as repeticoes
inventario = {}
cont = 0
for ip_unico in l:
    for i in range(0,list.__len__()):
        if ip_unico == list[i]:
            cont += 1
    inventariob = {ip_unico: cont}
    inventario.update(inventariob)
    cont = 0

inventario = sorted(inventario.items(), key=operator.itemgetter(1), reverse=True)

cont = 0
for ip in inventario:
    if cont < 10:
        url = ("http://ipvigilante.com/"+ip[0]+"/full")
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data) 
        print("DST=" + str(data["data"]["ipv4"]) + "  País=" + str(data["data"]["country_name"]) + "  Quantidade de pacotes=" + str(ip[1]))
        cont +=1

ref_arquivo.close()
#Fim Questão 3

#Questão 4
ref_arquivo = open(arq,"r")
list = re.findall(r'PROTO=[A-Z]*', ref_arquivo.read()) 

for i in range(0,list.__len__()):
    list[i]=list[i].replace('DST=','')

contTCP = 0
contUDP = 0
contICMP = 0

for i in range(0,list.__len__()):
    if list[i] == 'PROTO=TCP':
        contTCP += 1
    if list[i] == 'PROTO=UDP':
        contUDP += 1
    if list[i] == 'PROTO=ICMP':
        contICMP += 1
    
print("Quantidade de pacotes com protocolo TCP=" + str(contTCP))
print("Quantidade de pacotes com protocolo UDP=" + str(contUDP))
print("Quantidade de pacotes com protocolo ICMP=" + str(contICMP))
ref_arquivo.close()
#Fim Questão 4

