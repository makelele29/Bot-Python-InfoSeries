# -*- coding: utf-8 -*-
__author__ = 'Javier Castillo'

from bs4 import BeautifulSoup
import requests
import re
class seriesdb:
    def __init__(self,serie=""):
        if serie!="":
            self.url = 'https://www.themoviedb.org/search/tv?query='+serie.replace("_"," ")
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept-Language':'es-es,es;q=0.8'}
            req = requests.get(self.url, headers=headers)
            html = BeautifulSoup(req.text)
            h= html.find_all("a", { "class" : "result" })[0]
            self.url="https://www.themoviedb.org"+h.get('href')
            req = requests.get(self.url, headers=headers)
            html = BeautifulSoup(req.text)
            self.serie = html
    def name(self):
        h= self.serie.find_all("h2", { "class" : "tv_series" })[0]
        return re.sub(r"\([0-9]+\)","",h.find('a').getText())
    def image(self):
        h= self.serie.find_all("div", { "class" : "image_content" })[0]
        return h.find('img')['data-src']
    def overview(self):
        h= self.serie.find_all("div", { "class" : "overview" })[0]
        return h.find('p').getText().encode("utf-8")
    def status(self):
        h= self.serie.find_all("section", { "class" : "facts left_column" })[0]
        return h.find('p').getText().replace("Estatus ","").encode("utf-8")
    def duracion(self):
        h= self.serie.find_all("section", { "class" : "facts left_column" })[0]
        return h.find_all('p')[4].getText().encode("utf-8").replace("Duración ","").replace("m"," minutos")
    def temporadas(self):
        temporadas=self.serie.findAll('a', href=re.compile('.*/season/.*'))
        return (len(temporadas)-2)
    def enlace(self):
        return self.url
    def season(self,url,temporada):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept-Language':'es-es,es;q=0.8'}
        self.url=url+"/season/"+str(temporada)
        req = requests.get(self.url, headers=headers)
        html = BeautifulSoup(req.text)
        self.serie = html
        cont=0;
        h= self.serie.find_all("h3", { "class" : "episode_sort space" })[0].getText().replace("Episodios ","")
        return int(h)
