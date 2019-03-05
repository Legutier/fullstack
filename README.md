# Test Fullstack Tech-K
Test desarrollado por : Lukas Gutiérrez Lisboa.
## Backend

###Scrapper

Se genero una vista basada en clases la cual al recibir una orden POST, scrapea
la página y entrega todo esto en la base de datos. Se puede mejorar con multithreading
viendo como hacer que sqlite no bloquee la base de datos mediante django.

### APIs:
Se generaron APIs usando Django REST Framework. Las cuales manejan sus queries
mediante ORM a django.

#### Scrapper[Métodos principales: GET/POST/DELETE]:
  * POST no requiere argumentos. Puesto que inicia el scrapping a la página indicada.
  * GET entrega todos los libros en la BBDD
  * DELETE borra el libro deseado mediante su Primary key(id).

### CategoryList [Métodos principales: GET]:
  * GET entrega todas las categorías existentes.

## Supuestos
  * Las Categorías poseen una relación uno-a-muchos con los libros.
  * El API sólo consigue y entrega la data pedida,
    el trabajo de filtrar la misma se hace mediante frontend(javascript).
  * la página debe estar recabando la data constantemente, por eso se usó reactJS.
  (sin embargo la vista de página se actualiza cada 45 segundos.)
