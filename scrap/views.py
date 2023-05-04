from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup

# Create your views here.
Pages = {'Diario Ole' : 'https://www.ole.com.ar/river-plate', 
         'El Grafico' : 'https://www.elgrafico.com.ar/etiqueta/river',
         'TycSport': 'https://www.tycsports.com/river-plate.html',
         'Clarin' : 'https://www.clarin.com/tema/river-plate.html'
           }


def home(request):
    return render(request, 'scrap/home.html', {})


def diario(request, slug):
    if slug not in Pages.keys():
        return redirect('Home')
    url = Pages[slug]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    arr = []

    if slug == 'Diario Ole':
        titulos = soup.find_all('div', class_='sc-c062d4fd-0 jBHJMD')
        http = Pages[slug].split('/river')[0]
        for x in titulos:
            dic = {}
            dic['title'] = x.find('h2').text
            dic['url'] = f"{http}{x.a['href']}"
            dic['image'] = x.img['src']
            dic['relation'] = x.h3.text
            arr.append(dic)

    elif slug == 'El Grafico':
        titulos = soup.find_all('div', class_='eg-article')
        http = Pages[slug].split('/etiq')[0]
        for x in titulos:
            dic = {}
            dic['title'] = x.h3.text
            dic['url'] = f"{http}{x.a['href']}"
            print(x.a['href'])
            dic['image'] = x.img['src']
            dic['relation'] = x.span.text
            arr.append(dic)

    elif slug == 'Clarin':
        titulos = soup.find_all('li', class_='box col-lg-3 col-md-4 col-sm-6 col-xs-12 noPadding border')
        http = Pages[slug].split('/tema')[0]
        for x in titulos:
            dic = {}
            dic['title'] = x.h2.text
            dic['url'] = http + x.a['href']
            dic['image'] = x.img['data-big']
            dic['relation'] = 'River Plate'
            arr.append(dic)

    elif slug == 'TycSport':
        titulos = soup.find_all('div', class_='col-6 card')
        http = Pages[slug].split('/river')[0]
        for x in titulos:
            dic = {}
            dic['title'] = x.h3.text
            dic['url'] = http + x.a['href']
            dic['image'] = x.find('img', {'data-src' : True})['data-src']
            dic['relation'] = x.p.text if x.p is not None else 'Nuevo'
            arr.append(dic)
    
    return render(request, 'scrap/page.html', {'notices': arr, 'title': slug})

def tournamentTable(request):
    url = 'https://www.promiedos.com.ar/primera'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', {'class': 'tablesorter1'})

    headers = []
    for x in table.find_all('tr'):
        for y in x.find_all('th'):
            headers.append(y.text)

    table_values = []
    for x in table.find_all('tr')[1:]:
        td_tags = x.find_all('td')

        td_val = [y.text for y in td_tags]
        imagen = [y.img for y in td_tags][1]
        dic = {
            'puesto': td_val[0],
            'equipo': td_val[1],
            'img': imagen['src'],
            'puntos': td_val[2],
            'pj': td_val[3],
            'pg': td_val[4],
            'pe': td_val[5],
            'pp': td_val[6],
            'gf': td_val[7],
            'gc': td_val[8],
            'dif': td_val[9],
        }
        table_values.append(dic)
    return render(request, 'scrap/tournament.html', {
        'headers' : headers, 'tables' : table_values,
    })