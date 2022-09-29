# -*- coding: utf-8 -*-

#=========================================================
#
# Autor: Sergio Arroni del Riego
#
#=========================================================
import time
from types import NoneType
import requests as request
from bs4 import BeautifulSoup as bs4
from urllib.parse import urljoin, urlparse

import urllib.robotparser as rp
import argparse

urls = []
max_dw = 5
ERROR_STATUS = -1

def main(args):
    """main

        Contiene toda la logica del Crawler

        Params:
            args, todos los argumentos dados por consola
    """
    global max_dw
    
    semillas = args.file
    seconds=args.s
    max=args.m
    metodo = "a"
    semillas = parse(semillas)
    
    if args.a:
        metodo = "a"
    if args.p:
        metodo = "p"

    max_dw = max

    f = open(f'docs/URLS.txt', 'w')

    cont = 0
    urls = []


    urls = scan(semillas[0] , seconds, semillas, metodo)

    if type(urls) == int and urls < 0:
        print("Ha ocurrido un error en la peticion, por favor consulte su red e intentelo otra vez :)") 
    
    for url in urls:
        f.write(f"\t{cont}\t{url}\n")
        cont += 1
    f.close()
    
def scan(url, seconds, semillas, metodo):
    """scan

        Escanea la pagina pasada como url, este metodo tiene la logica comun para anchura y profundidad

        Params:
            url, la pagina que hay que escanear
            seconds, segundos que hay que esperar entre peticiones
            semillas, todos las urls que quedan por explorar
            metodo, si es un escaneo en profundidad o en anchura
    """
    
    global max_dw, urls
    robots, seconds = robots_parser(url, seconds)
    
    if not robots:
        return urls
    
    urls.append(url)

    time.sleep(seconds)
    html = request.get(url)

    if not html.status_code==200:
        return ERROR_STATUS

    print(f"Crawling {url}\tquedan {max_dw} archivos por descargar")

    max_dw -= 1 
    f = open(f'docs/Doc_{max_dw+1}.html', 'wb')
    f.write(html.content)
    f.close()

    if max_dw == 0: 
        return urls

    html = bs4(html.text, 'html.parser')
    links = html.find_all("a", href=True) 
    
    if metodo == "a":
        urls = scan_a(semillas[0] , seconds, semillas, links, metodo)
    else:
        urls = scan_p(semillas[0] , seconds, semillas, links, metodo)
        
    return urls
    
       

def scan_p(url, seconds, semillas, links, metodo ):
    """scan_p

        Escanea la pagina pasada como url, este metodo realiza la busqueda en profundidad de nuevas urls que escanear 

        Params:
            url, la pagina que hay que escanear
            seconds, segundos que hay que esperar entre peticiones
            semillas, todos las urls que quedan por explorar
            links, lista con los links que se han encontrado en la url dada
            metodo, si es un escaneo en profundidad o en anchura
    """
    for l in (links):
        if max_dw == 0:
            return urls

        l = normalize_link(url, l.get('href'))

        if l in urls:
            continue
        
        semillas.insert(0, l)

        scan(semillas[0], seconds, semillas, metodo)
    return urls

def scan_a(url, seconds, links_all, links, metodo ):
    """scan_a

        Escanea la pagina pasada como url, este metodo realiza la busqueda en anchura de nuevas urls que escanear 

        Params:
            url, la pagina que hay que escanear
            seconds, segundos que hay que esperar entre peticiones
            semillas, todos las urls que quedan por explorar
            links, lista con los links que se han encontrado en la url dada
            metodo, si es un escaneo en profundidad o en anchura
    """
    
    for l in (links):
        if max_dw == 0:
            return urls

        l = normalize_link(url, l.get('href'))

        if l in urls:
            continue

        links_all.pop(0)
        links_all.append(l)

        scan(links_all[0] ,seconds, links_all, metodo)
    return urls

def normalize_link(url, link):
    """normalize_link

        Normaliza el link dado a la url 

        Params:
            url, la base de la url a normalizar
            link, link a normalizar
    """
    if link.startswith("/") or link.startswith("#"):
        return urljoin(url, link)
    return link

def robots_parser(url, seconds):
        """robots_parser

        Revisa el Robots.txt de la url dada y devuelve el tiempo, si lo hubiera, de espera entre peticiones y si se puede o no descargar y analizar la pagina.

        Params:
            url, url a comprobar
        """
        url_all = url
        url = urlparse(url_all)
        base = url[0] + '://' + url[1]
        if base[-1] == '/':
            base = base[:-1]
        
        robots_url = urljoin(base, '/robots.txt')

        robot_parser = rp.RobotFileParser()
        robot_parser.set_url(robots_url)
        robot_parser.read()

        if not robot_parser.can_fetch("*", url_all.encode('utf-8')):
            print(f"[DANGER] Cannot scrap {url_all.encode('utf-8')}")
            return False
        if not (type(robot_parser.crawl_delay('*')) is NoneType):
            seconds = robot_parser.crawl_delay('*')
        return True, seconds

def parse(dir):
    """Parse

    Funcion que parsea el texto del argumento con el fichero de semillas a una lista de semillas

    Params:
        dir, direccion del fichero
    """
    semillas = []
    f = open(dir, 'r')
    aux = f.read()
    f.close()
    aux = aux.split("\n")
    for a in aux:
        if not (a[0] == "#"):
            semillas.append(a.strip("\t\n\r"))
    return semillas

def presentacion():
    """Presentacion
    
    Funcion que muestra una presentacion en ASCII muy bonita
    
    """
    
    print("Crawler para la asignatura SIW :)\nAñade el argumento \"-h\" a la hora de ejecutar para optener la ayuda del Crawler")                                                                       
    print("Autor: Sergio Arroni del Riego - UO276341\n\n\n")

def parse_args():
    """Parse_args
    
    Funcion que permite usar la consola para añadir parametros de una forma usable. 
    
    """
    parser = argparse.ArgumentParser(description='WebCrawler para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera las semillas de inicio. Default: semillas.txt",type=str, default="semillas.txt")
    parser.add_argument("--m", help="Numero maximo de descargar. Default: 10", type=int, default=10)
    parser.add_argument("--s", help="Numero de segundos que esperara entre cada iteracion. Default: 10", type=int, default=10)
    parser.add_argument("-a", help="Tipo de exploracion que realizara: Anchura [a]. Default: true", action="store_true", default="true")
    parser.add_argument("-p", help="TTipo de exploracion que realizara: Profundidad [p]", action="store_true")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    """__main__
    
    Primero imprime la presentacion del Crawler y luego el main con la logica del mismo
    
    """
    presentacion()
    main(parse_args())