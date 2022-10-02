# -*- coding: utf-8 -*-

#=========================================================
#
# Autor: Sergio Arroni del Riego
#
#=========================================================

import argparse

from textblob import TextBlob as tb


def main(args):
    """main

        Contiene toda la logica del Si

        Params:
            args, todos los argumentos dados por consola
    """
    
    texts = open(args.file ,"r")
    
    querys = open(args.qfile, "r")
    
    querys_list = querys.split("\n")
    
    texts_list = texts.split("\n")
    
    texts_final = {}
    
    for text in texts_list:
        texts_aux = text.split("\t")
        texts_final[texts_aux[0]] = texts_aux[1]
    
    f = open("./docs/resultados.txt")
    
    # Las similitudes más cercanas a 1 mejor. El coseno va de 0 a infinito y cuanto más cercano a 0 mejor
    
    # Jaccard
    
    for q in querys_list:
        best_text = find_best_text(q, texts_final, "cosine", args.l, args.s) 
        print_sim_q_text(f, q, best_text, "cosino")
        
        best_text = find_best_text(q, texts_final, "jaccard") 
        print_sim_q_text(f, q, best_text, "cosino")
    
    f.close()
    
    querys.close()
    
    texts.close()
    

def find_best_text(q, texts, metodo, lema, stema):
    
    text_correct = ""
    bag = {}
    q_tokens = tb(q).words
    
    for text in texts:
        text = tb(text)
        bag = string_to_bag_of_words(text, lema, stema)
        
    return text_correct

def print_sim_q_text(f, q, text, metodo):

    print(q)
    
    return
    
def string_to_bag_of_words(text, lema, stema):
    
    tokens = text.words
    bag = {}
    
    stop_bag = {}
    
    for token in tokens:
        if token in bag:
            bag[token] += 1
        else:
            
            if token in stop_bag:
                continue
            
            if lema:
                token.lemmatize()
            elif stema:
                token.stem()
                
            bag[token] = 0
    
    return bag

def presentacion():
    """Presentacion
    
    Funcion que muestra una presentacion en ASCII muy bonita
    
    """
    
    print("Trabajo de similitud entre textos para la asignatura SIW :)\nAñade el argumento \"-h\" a la hora de ejecutar para optener la ayuda del Script")                                                                       
    print("Autor: Sergio Arroni del Riego - UO276341\n\n\n")

def parse_args():
    """Parse_args
    
    Funcion que permite usar la consola para añadir parametros de una forma usable. 
    
    """
    parser = argparse.ArgumentParser(description='Similitud entre textos para la asignatura SIW')
    parser.add_argument("--file", help="Fichero donde extraera los textos a consultar. Default: ./data/cran-1400.txt",type=str, default="./data/cran-1400.txt")
    parser.add_argument("--qfile", help="Fichero donde extraera las consultas. Default: ./data/cran-queries.txt",type=str, default="./data/cran-queries.txt")
    parser.add_argument("-l", help="Si se quiere lematizar los textos a consultar. Default: false", action="store_true")
    parser.add_argument("-s", help="Si se quiere stematizar los textos a consultar. Default: false", action="store_true")
    '''
    parser.add_argument("-a", help="Tipo de exploracion que realizara: Anchura [a]. Default: true", action="store_true", default="true")
    parser.add_argument("-p", help="TTipo de exploracion que realizara: Profundidad [p]", action="store_true")
    '''
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    """__main__
    
    Primero imprime la presentacion del trabajo y luego el main con la logica del mismo
    
    """
    presentacion()
    main(parse_args())