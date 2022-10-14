# SIW

## Detección de documentos cuasi-duplicados P4
Respecto a la practica anterior, el bag_of_words esta usando lematizacion, palabras vacias,
signos de puntuacion y minusculas.

Respecto a esta practica permito parametrizar los n-gramas. He provado con unigramas, bigramas y trigramas, para todos ellos me ha salido los mismos elemeentos cuasi-duplicados (restrictiveness = 10), que son los mismos que hay en el archivo articles_1000.truth

- Para ejecutar el archivo se le pasan los parametros por consola, si pulsas -h te sacara la ayuda, pero en resumen:
    ```
        -r  Numero de restrictiveness que se quiera aplicar         [10]
        -n  Numero de ngramas que se quieran usar                   [1] 
        --file Ruta archivo de textos                               [articles_1000.train]
    ```
- En docs encontraras las salidas para cada n-grama provado, tambien mi scrip genera un resultados.txt en el que guardo cada doc y su simhash, esto lo hice para comprobar que todo me fuera bien y tenian sentido los simhash.