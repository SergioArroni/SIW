# -*- coding: utf-8 -*-

#=========================================================
#
# Autor: Sergio Arroni del Riego
#
#=========================================================

import argparse
import nltk
nltk.download('omw-1.4')
from textblob import TextBlob as tb
from nltk.corpus import stopwords


def main(args):
    """main

        Contiene toda la logica del Si

        Params:
            args, todos los argumentos dados por consola
    """
    t = open(args.file ,"r")
    
    q = open(args.qfile, "r")
    
    texts = list(t)
    
    querys = list(q)
    
    querys_list = [line.rstrip('\n') for line in querys]
    
    texts_list = [line.rstrip('\n') for line in texts]
    
    texts_final = {}
    
    querys_final = {}
    
    for text in texts_list:
        texts_aux = text.split("\t")
        texts_final[texts_aux[0]] = texts_aux[1]
    
    for q in querys_list:
        q_aux = q.split("\t")
        querys_final[q_aux[0]] = q_aux[1]
        
    f = open("./docs/resultados.txt", "a")
    
    # Las similitudes más cercanas a 1 mejor. El coseno va de 0 a infinito y cuanto más cercano a 0 mejor
    
    # Jaccard Reutilizar todo meter un booleano para que lo calcule abajo no arriba
    
    for q in querys_final:
        best_text, best_text_result = find_best_text(querys_final[q], texts_final, ["coseno", "jaccard"], args.l, args.s, args.stop) 
        
        print_sim_q_text(f, q, best_text["coseno"], best_text_result["coseno"], "coseno", args.l, args.s, args.stop)
        print_sim_q_text(f, q, best_text["jaccard"], best_text_result["jaccard"], "jaccard", args.l, args.s, args.stop)
    
    f.close()
    

def find_best_text(q, texts, metodo, lema, stema, stop):
    
    text_correct_cos={}
    text_correct_jac={}
    best_text = {} 
    best_text_result={} 
    bag = {}
    
    q_tokens = tb(q)
    
    bag_q_token = string_to_bag_of_words(q_tokens, lema, stema, stop)
    
    for text in texts:
        text_txB = tb(texts[text])
        bag = string_to_bag_of_words(text_txB, lema, stema, stop)
        
        if "coseno" in metodo :
            result_cos = cos(bag_q_token, bag)
            text_correct_cos[text] = sum(result_cos.values())
        if "jaccard" in metodo:
            result_jac = jac(bag_q_token, bag)
            text_correct_jac[text] = sum(result_jac.values())
        
    if "coseno" in metodo :
        best_text["coseno"]=max(text_correct_cos, key=text_correct_cos.get)
        best_text_result["coseno"]=max(text_correct_cos.values())
    if "jaccard" in metodo:
        best_text["jaccard"]=max(text_correct_jac, key=text_correct_jac.get)
        best_text_result["jaccard"]=max(text_correct_jac.values())
        
    return best_text, best_text_result

def print_sim_q_text(f, q, text, result, metodo, lema, stema, stop):
    f.write(f"\n-------------------------------------------------------------- Para la query q: {q} -------------------------------------------------------\n")
    f.write(f"El mejor texto es el {text} con un resultado de: {result}\nPara el metodo: {metodo}\nCon un valor de lematizacion de: {lema}, de stematizacion de: {stema} y un StopWords de NLTK de: {stop}\n")
    

def string_to_bag_of_words(text, lema=False, stema=False, stop=False):
   
    tokens = text.words
    bag = {}
    if stop:
        stops = set(stopwords.words('english'))
    else:
        stops = {}

    for token in tokens:
        if token in bag:
            bag[token] += 1
        else:
            
            if token in stops:
                continue
            
            if lema:
                token = token.lemmatize()
            elif stema:
                token = token.stem()
                
            bag[token] = 1
    
    return bag

def cos(x, y):
    coef = {}
    for palabra in x:
        if not palabra in y:
            coef[palabra] = 0
            continue
        coef[palabra] = inter(x,y, palabra) / (x[palabra] * y[palabra])
    return coef
    
def jac(x, y):
    coef = {}
    for palabra in x:
        coef[palabra] = inter(x,y, palabra) / (union(x, y, palabra))
    return coef
    
def inter(x, y, palabra):
    if palabra in x and palabra in y:
        return min(x[palabra], y[palabra])
    return 0

def union(x, y, palabra):
    result = 0
    if palabra in x:
       result += x[palabra]
    if palabra in y:
        result += y[palabra]
    return result

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
    parser.add_argument("-stop", help="Si no se quiere usar un fichero de stop words. Default: false", action="store_false")
    '''
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