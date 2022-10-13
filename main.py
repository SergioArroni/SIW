# -*- coding: utf-8 -*-

# =========================================================
#
# Autor: Sergio Arroni del Riego
#
# =========================================================

import bag_og_words as bag
import sim_hash as simhash

if __name__ == "__main__":
    """__main__

    Primero imprime la presentacion del trabajo y luego el main con la logica del mismo

    """

    #bag.bag_of_words()
    f = open("./docs/resultados.txt", "w")
    f.write(str(simhash.SimHash()))
    f.close()
    
