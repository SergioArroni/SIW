# -*- coding: utf-8 -*-

#=========================================================
# Clase Crawler
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
    """ Main program """
    global max_dw
    
    semillas = args.file
    seconds=args.s
    max=args.m
    name = args.name
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

    if metodo == "a":
        urls = scan_a(semillas ,semillas[0], seconds)
    else:
        urls = scan_p(semillas[0] , seconds, semillas)

    if type(urls) == int and urls < 0:
        print("Ha ocurrido un error en la peticion, por favor consulte su red e intentelo otra vez :)") 
    
    for url in urls:
        f.write(f"\t{cont}\t{url}\n")
        cont += 1
    f.close()

def scan_p(url, seconds, semillas):
    """ Main program """
    # Code goes over here.
    global max_dw

    robots, seconds = robots_parser(url, seconds)
    if not robots:
        return urls
    urls.append(url)

    time.sleep(seconds)
    html = request.get(url)

    if not html.status_code==200:
        return ERROR_STATUS

    max_dw -= 1 
    f = open(f'docs/Doc_{max_dw+1}.html', 'wb')
    f.write(html.content)
    f.close()

    if max_dw == 0: 
        return urls

    html = bs4(html.text, 'html.parser')
    links = html.find_all("a", href=True) 
    for l in (links):
        if max_dw == 0:
            return urls

        l = normalize_link(url, l.get('href'))

        if l in urls:
            continue
        
        semillas.insert(0, l)

        scan_p(semillas[0], seconds, semillas)
    return urls

def scan_a(links_all , url, seconds):
    """ Main program """
    # Code goes over here.
    global max_dw
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
    for l in (links):
        if max_dw == 0:
            return urls

        l = normalize_link(url, l.get('href'))

        if l in urls:
            continue

        links_all.pop(0)
        links_all.append(l)

        scan_a(links_all ,links_all[0], seconds)
    return urls

def normalize_link(url, link):
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
    
    print(" ________  ________  ________  ___       __   ___       _______   ________     ")
    print("|\   ____\|\   __  \|\   __  \|\  \     |\  \|\  \     |\  ___ \ |\   __  \    ")
    print("\ \  \___|\ \  \|\  \ \  \|\  \ \  \    \ \  \ \  \    \ \   __/|\ \  \|\  \   ")
    print(" \ \  \    \ \   _  _\ \   __  \ \  \  __\ \  \ \  \    \ \  \_|/_\ \   _  _\  ")
    print("  \ \  \____\ \  \\  \\ \  \ \  \ \  \|\__\_\  \ \  \____\ \  \_|\ \ \  \\  \| ")
    print("   \ \_______\ \__\\ _\\ \__\ \__\ \____________\ \_______\ \_______\ \__\\ _\ ")
    print("    \|_______|\|__|\|__|\|__|\|__|\|____________|\|_______|\|_______|\|__|\|__|")                                                                        
    print("Author: Sergio Arroni del Riego\n\n\n")

def parse_args():
    """Parse_args
    Funcion que permite usar la consola para añadir parametros de una forma usable. 
    """
    parser = argparse.ArgumentParser(description='WebCrawler para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera las semillas de inicio. Default: semillas.txt",type=str, default="semillas.txt")
    parser.add_argument("--m", help="Numero maximo de descargar. Default: 10", type=int, default=10)
    parser.add_argument("--s", help="Numero de segundos que esperara entre cada iteracion. Default: 10", type=int, default=10)
    parser.add_argument("--name", help="Nombre del Crawler. Default:TheBestCrawler", type=str, default="TheBestCrawler")
    parser.add_argument("-a", help="Tipo de exploracion que realizara: Anchura [a]. Default: true", action="store_true", default="true")
    parser.add_argument("-p", help="TTipo de exploracion que realizara: Profundidad [p]", action="store_true")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    presentacion()
    main(parse_args())