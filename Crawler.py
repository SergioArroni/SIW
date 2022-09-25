# -*- coding: utf-8 -*-

#=========================================================
# Clase Crawler
#
# Autor: Sergio Arroni del Riego
#
#=========================================================
import time
import requests as request
from bs4 import BeautifulSoup as bs4
from urllib.parse import urljoin, urlparse

import urllib.robotparser as rp

urls = []
max_dw = 5
ERROR_STATUS = -1

def main(url, seconds, max, semillas):
    """ Main program """
    # Code goes over here.
    global max_dw
    max_dw = max
    #return scan_a(semillas ,url, seconds)
    return scan_p(semillas[0] , seconds, semillas)

def scan_p(url, seconds, semillas):
    """ Main program """
    # Code goes over here.
    global max_dw

    urls.append(url)

    #print(urls)

    #print(url)
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

    urls.append(url)

    #print(urls)

    #print(url)
    time.sleep(seconds)
    html = request.get(url)

    if not html.status_code==200:
        return ERROR_STATUS

    print(f"Crawling {url} ,Max downloads {max_dw}")

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

def scanRobots(self,url,link):
        """ScanRobots

        Revisa el robots.txt y devuelve True en caso de que se pueda
        escanear la web y False en caso contrario

        Params:
            url, url base
            link, url a comprobar por robots.txt
        """
        url = urlparse(url)
        base = url[0] + '://' + url[1]
        if base.endswith('/'):
            base = base[:len(base)-1]
        robots_url = urljoin(base, '/robots.txt')

        robot_parser = rp.RobotFileParser()
        robot_parser.set_url(robots_url)
        robot_parser.read()

        if not self.robot_parser.can_fetch("cw_1", link.encode('utf-8')):
            print(f"(!) Cannot scrap {link}")
            print (f"\t # Crawling {link} is prohibited unless you have express written")
            return False
        return True

if __name__ == "__main__":

    semillas=[]

    while True:
        param = input("Ingrese las Urls semillas pulse \"0\" para parar:")

        if param == "0":
            break
        semillas.append(param)

    time_input = int(input("Ingrese el tiempo de espera entre peticiones:"))
    max_input = int(input("Ingrese el maximo de documentos descargados por semilla:"))

    f = open(f'docs/URLS.txt', 'w')

    cont = 0
    urls = []

    urls = main(semillas[0], time_input, max_input, semillas)

    print(f"--------------------------------------------------------------------------{len(urls)}")
    if type(urls) == int and urls < 0:
        print("Ha ocurrido un error en la peticion, por favor consulte su red e intentelo otra vez :)") 
    
    for url in urls:
        f.write(f"\t{cont}\t{url}\n")
        cont += 1
    f.close()