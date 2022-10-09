# SIW

## Similitud entre textos P3
He realizado los opcionales de lematizacion, de stematizacion y de stop words utilizando el fichero de stop words de NLTK. Tambien realice la implementación de medidas de similitud que incorporan frecuencia de aparición de los términos en consultas y documentos. :)

- Para ejecutar el archivo se le pasan los parametros por consola, si pulsas -h te sacara la ayuda, pero en resumen:
    ```
        -l  Si se quiere usar o no lematizacion         [False]
        -s  Si se quiere usar o no stematizacion        [False] 
        -stop  Si se quiere usar o no stop words        [False]
        --qfile Ruta archivo de querys                  [cran-querys.txt]
        --file Ruta archivo de textos                   [cran-1400.txt]
    ```
- Los ficherps cran-1400.txt y cran-querys.txt son los que utilice para las salidas resultados_lema, stema, stop y  false. Cada una de estas salidas corresponde a unos parametros diferentes, tanto el nombre como el documento son bastantes descriptivos, estos documentos se encuentran en la carpeta docs.

- Tambien, probe a introducir una query entre los textos para comprobar que me salia el maximo de correlacion, esta prueba se encuentra en cran-1400_plus.txt y el resultado esta en resultados_lema_plus

 