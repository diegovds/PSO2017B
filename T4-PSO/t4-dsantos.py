#!/usr/bin/env python3

import os
import sys
import time

#Obs. O arquivo t4-dsantos.py deve estar dentro da pasta que se deseja listar.

#Lista que recebe os objetos Arquivo
l = []

#Classe que manipula os objetos Arquivo
class Arquivo(object):
   
    def __init__(self, diretorio, tam, ultMod):
        self.__diretorio = diretorio
        self.__tam = tam
        self.__ultMod = ultMod
     
    def __repr__(self):
        return "%s %6s:Bytes %s" % (self.__ultMod, self.__tam, self.__diretorio)
 
    def get_diretorio(self):
        return self.__diretorio
 
    def get_tam(self):
        return self.__tam

    def get_ultMod(self):
        return self.__ultMod

#Função que calcula o tamanho somente das pastas.
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
    
#Função que percorre pastas, adiciona objetos Arquivo na lista e ordena a lista em ordem crescente de modificação.
def listar_arquivos(path):
    i=0
    for root, dirs, files in os.walk(path):
        if i < 1:
            diretorio = root
            tam = get_size(root)
            ultMod = time.strftime("%Y-%m-%d", time.gmtime(os.path.getmtime(root)))
            
            a = Arquivo(diretorio, tam, ultMod)
            l.append(a)
            
            i += 1
            
        for f in files:
            diretorio = root + '/' + f
            tam = os.path.getsize(os.path.join(os.path.abspath(root), f))
            ultMod = time.strftime("%Y-%m-%d", time.gmtime(os.path.getmtime(os.path.join(os.path.abspath(root), f))))
            
            a = Arquivo(diretorio, tam, ultMod)
            l.append(a)
        
        for d in dirs:
            diretorio = root + '/' + d
            tam = get_size(root + '/' + d)
            ultMod = time.strftime("%Y-%m-%d", time.gmtime(os.path.getmtime(os.path.join(os.path.abspath(root), d))))
            
            a = Arquivo(diretorio, tam, ultMod)
            l.append(a)
    
    l_ordenada = sorted(l, key = Arquivo.get_ultMod)
    
    for i in range(0,l_ordenada.__len__()):
        print(l_ordenada[i])
    
#Main
pasta = sys.argv[1]
listar_arquivos(pasta)
    