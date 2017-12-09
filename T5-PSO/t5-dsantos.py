#!/usr/bin/env python3

import json, requests, os, bs4, shutil

url = 'https://xkcd.com/info.0.json'
comics = []

pasta = 'xkcd'
if os.path.isdir(pasta):    # verifica se a pasta ja existe
    print('A pasta existe.')
    shutil.rmtree(pasta)
    os.makedirs(pasta) 
else:
    os.makedirs(pasta)      #  cria a pasta caso nao exista
    

print('Acessando a pagina %s...' %url)
print(' ')

res = requests.get(url, stream=True)
try:
    res.raise_for_status()
    
    ult_comic = json.loads(res.text)
    id_comic = ult_comic['num']
except Exception as exc:
    print('Ocorreu um problema: %s'(exc))

#pega url com id das comics
comics.append("https://xkcd.com/"+str(id_comic)) 
for i in range(1, 4):
        comics.append("https://xkcd.com/"+str(id_comic - i)) 

#lista que contem somente o nome das comics
nomes = []

#pega url com nome e baixa comics
for comic in comics:
    res = requests.get(comic, stream=True)
    try:
        res.raise_for_status()
    
        soup = bs4.BeautifulSoup(res.text)
    
        for fig in soup.select('#comic img'):
            comicUrl = 'http:' + fig.get('src')
        
            print(' ')
            print('Realizando o download de %s.' %comicUrl)
        
            res = requests.get(comicUrl, stream=True)
            res.raise_for_status()
        
            imgFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
        
            for chunk in res.iter_content(100000):
                imgFile.write(chunk)
        
            imgFile.close()
        
            print('Download de %s concluido!' %comicUrl)
            nomes.append(os.path.basename(comicUrl))
    except Exception as exc:
        print('Ocorreu um problema: %s'(exc))

#templatetemplate de álbum
inicio_html = ' <!doctype html>  <html lang="en"> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> <meta name="description" content=""> <meta name="author" content=""> <link rel="icon" href="../../../../favicon.ico"> <title>Álbum comics</title> <link href="../../../../dist/css/bootstrap.min.css" rel="stylesheet"> <link href="album.css" rel="stylesheet"> </head> <body> <header> <div class="collapse bg-dark" id="navbarHeader"> <div class="container"> <div class="row"> <div class="col-sm-8 py-4"> <h4 class="text-white"></h4> </div> <div class="col-sm-4 py-4"> </div> </div> </div> </div> <div class="navbar navbar-dark bg-dark"> </div> </header> <main role="main"> <section class="jumbotron text-center"> <div class="container"> <h1 class="jumbotron-heading">Álbum das quatro comics mais recentes do site https://xkcd.com</h1> </div> </section> <div class="album text-muted"> <div class="container"> <div class="row">'
            
fim_html = '</div> </div> </div> </main> <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" \ crossorigin="anonymous"></script> <script src="../../../../assets/js/vendor/popper.min.js"></script> <script src="../../../../dist/js/bootstrap.min.js"></script> <script src="../../../../assets/js/vendor/holder.min.js"></script> <script> Holder.addTheme("thumb", { bg: "#55595c", fg: "#eceeef", text: "Thumbnail" }); </script> </body> </html>'

# abre o arquivo HTML para escrita
arq_html = open('album.html', 'w')

# escrevendo no arquivo HTML
html = ''
html = html + inicio_html

i = 1
for n in nomes:
    html = html + '<div class="card"> <p class="card-text">' + str(i) + '.</p>'
    html = html + '<img src="xkcd/' + n + '"alt="Card image cap"> </div>'
    i += 1

html = html + fim_html
arq_html.write(html)
print(' ')
print('Site HTML garado localmente com sucesso!!!')

# fechando os arquivos
arq_html.close()