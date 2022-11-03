# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

import math
import argparse


class PageRank:

    def __init__(self, args: argparse.Namespace) -> None:
        '''__init__

        Constructor de la clase PageRank

        Parameters:
            args (argparse.Namespace): Argumentos de entrada
        Output:
            None
        '''
        self.edges = {}
        self.nodes = []
        self.calculated_page_rank = {}
        self.calculated_page_rank_ant = {}
        self.iter = args.iter
        self.damping = args.d
        self.limit = args.l
        self.file = args.file
        self.init = args.init
        self.paro = 0
        self.parse_graph()
        self.page_rank()

    def parse_graph(self) -> None:
        '''parse_graph

        Carga el grafo del fichero de entrada

        Parameters:
            None
        Output:
            None
        '''
        f = open(self.file, 'r')
        file = [line.rstrip('\n') for line in f]
        for line in file:
            key = line.split(",")[0]
            value = line.split(",")[1]
            if key in self.edges.keys():
                self.edges[key].append(value)
            else:
                self.edges[key] = [value]
        for line in file:
            key = line.split(",")[0]
            value = line.split(",")[1]
            if not (value in self.edges.keys()):
                self.edges[value] = [value]
        print(f"El grafo cargado:\t{self.edges}")
        f.close()
        self.nodes = list(self.edges.keys())

    def calculate_value(self, x: str, node: list) -> float:
        '''calculate_value

        Calcula el valor de la formula de PageRank

        Parameters:
            x (str): Nodo del grafo
            node (list): Nodo del grafo
        Output:
            float: Valor de la formula de PageRank
        '''
        if len(self.calculated_page_rank_ant.items()) == 0:
            if x == node:
                return self.init/len(self.nodes)
            else:
                return 0
        elif node in self.edges[x]:
            return self.calculated_page_rank_ant[x]/len(self.edges[x])
        else:
            return 0

    def page_rank(self) -> None:
        '''page_rank

        Calcula el PageRank de cada nodo del grafo cargado

        Parameters:
            None
        Output:
            None
        '''
        magic_number = (1.0 - self.damping) / len(self.edges)

        for iter in range(self.iter):
            for node in self.nodes:
                self.calculated_page_rank[node] = magic_number + self.damping * sum((
                    [self.calculate_value(x, node) for x in self.nodes]))

            self.paro = iter
            if self.eval_limit() == False:
                break

            self.calculated_page_rank_ant = self.calculated_page_rank.copy()

    def eval_limit(self) -> bool:
        '''eval_limit

        Evalúa si el limite de error de cada PageRank de cada nodo, es menor que el limite establecido

        Parameters:
            None
        Output:
            bool: True si todos los errores del PageRank son menores que el limite establecido, False en caso contrario
        '''
        if len(self.calculated_page_rank_ant.values()) > 0:
            limits = [math.fabs(self.calculated_page_rank_ant[node] -
                                self.calculated_page_rank[node]) <= self.limit for node in self.nodes]
            is_True = False

            if False in limits:
                is_True = True

            return is_True

    def __str__(self) -> str:
        '''__str__

        Devuelve el PageRank y más valores de cada nodo del grafo cargado
        
        Parameters:
            None
        Output:
            str: PageRank y más valores de cada nodo del grafo cargado
        '''
        return f"Fichero Cargado:\t{self.file}\nPageRank:\t{self.calculated_page_rank}\nPageRankTotal:\t{sum(self.calculated_page_rank.values())}\nIteraciones:\t{self.iter}\nDamping:\t{self.damping}\nLimit:\t{self.limit}\nPeso inicial:\t{self.init}\nParo en la iteracion:\t{self.paro}\n\n"
