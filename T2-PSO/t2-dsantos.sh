#!/bin/bash

tarefa1(){
    echo " "
    echo "Número total de pacotes"
    cat $1 | wc -l
    echo " "
}

tarefa1 $1

tarefa2(){
    echo " "
    echo "Top 10 IPs fonte e quantos pacotes cada um"
    cat $1 | sed 's/.*SRC=*// ; s/ * .*//' | sort -n | uniq -u | head -10
    echo " "
}

tarefa2 $1

tarefa3(){
    echo " "
    echo "Top 10 IPs destino e quantos pacotes cada um"
    cat $1 | sed 's/.*DST=*// ; s/ * .*//' | sort -n | uniq -u | head -10
    echo " "
}

tarefa3 $1

tarefa4(){
    echo " "
    echo "Contagem de pacotes por protocolo (TCP, UDP, ICMP):"
    echo "Protocolo TCP:" 
    cat $1 | grep -wc PROTO=TCP 
    echo "Protocolo UDP:" 
    cat $1 | grep -wc PROTO=UDP 
    echo "Protocolo ICMP:" 
    cat $1 | grep -wc PROTO=ICMP
    
    echo " "
}

tarefa4 $1