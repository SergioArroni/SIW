# SIW

## Resolviendo consultas con un índice

He realizado las dos funciones de similitid tanto la de bm25 como la de coseno, para alternar entre ellas basta con añadir --bm25 para ejecutar la version bm25, por defecto ejecuta la del coseno, el principal problema de la practica es que esta muy mal optimizada y para documentos grandes tarda mucho, soy consciente de que se podria mejorar. Tambien he realizado el opcional del servicio web, se encuentra en app.py y al ejecutar con flask run, si se accede a la ruta indica en la terminal y se accede al endpoint /indice se cargara el indice y con /query se cargaran las query indicadas.

La version de bm25 no me he parado mucho a calcular a ver si lo hace correctamente.

He utilizado el ejemplo de las pizzas para comprobar que funciona correctamente.

- Para ejecutar el archivo se le pasan los parametros por consola, si pulsas -h te sacara la ayuda, pero en resumen:
    ```
        --index  Ruta del archivo donde se guardara el index                    [10]
        --query  Ruta del archivo de texto que corresponde a las querys         [ejemplos_q.txt] 
        --file Ruta del archivo de textos a indexar                             [ejemplo.txt]
        --query_json Ruta del archivo donde se quiere guardar los resultados    [ejemplo.txt]
        --bm25 Si se quiere utilizar bm25                                       [False]
    ```

- En docs encontraras los resultados y el indice en formato .json