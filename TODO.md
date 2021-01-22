# TODO LIST

- Finally push this version to production *eheh...*
- ~Add charts~ **DONE**
- ~Add chart and table for relative and absolute variation of new doses and new vaccines~ **DONE**
- ~Add time chart of vaccination~ **DONE**
- ~Calculate number of vaccines by producer~ **DONE**
- ~Calculate variation in doses~, ~variation by gender~, variation by age range **NOT POSSIBLE**, ~variation by category~ **DONE**
- ~Add missing chart~ **DONE**
- ~Show both first and second subministration in the first chart and on top of the page~ **DONE**
- ~Add cloropleth map of COLORI TERRITORI SECONDO SPERANZA~ **DONE**
    - ~GeoJson https://gist.github.com/datajournalism-it/f1abb68e718b54f6a0fe~
    - ~Cloropleth map https://leafletjs.com/examples/geojson/ - https://leafletjs.com/examples/choropleth/~
- ~Ragiona sulle percentuali. Come sono calcolate? *Elaboro*: attualmente, la percentuale di popolazione vaccinata è calcolata facendo il rapporto tra dosi totali inoculate e popolazione del territorio. Tuttavia, ciò non tiene conto della secoda dose. Le percentuali comunicate ufficialmente risalgono al giorno prima e sono spesso sbagliate. Come ne esco?~
    - ~Un possibile approccio che ho trovato è quello di:~
        1. ~Prendere il totale delle dosi somministrate oggi~
        2. ~Sottrarre le seconde dosi somministrate ieri~
        3. ~Calcolare così la percentuale.~
    - ~L'errore così facendo sarebbe minimo e la percentuale sarebbe accettabilmente corretta~ **HO USATO QUESTO APPROCCIO**
- Comment and clean up the code a little bit more
- Add the history of delivered doses by manifacturer
