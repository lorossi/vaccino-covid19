# Vaccini covid-19 italia

Controlla in tempo reale (o quasi) la distribuzione del vaccino contro il covid in Italia.

## Link: [vaccinocovid19.live](https://www.vaccinocovid19.live/)

## Fonte dei dati

I dati sono presi direttamente dalla [dashboard Ministeriale](https://www.governo.it/it/cscovid19/report-vaccini/) (o meglio, dalla [repo contenente i dati](https://github.com/italia/covid19-opendata-vaccini)) e vengono manipolati dal server per venire mostrati con più agio.

**Saltuariamente** i dati forniti dal Ministero sono **errrati**: il numero di nuovi vaccinati può essere **negativo** e il totale dei vaccinati può **non coincidere** con quanto risulta dalla somma delle tabelle dei vaccinati relativi per fasce di età, impiego o sesso. Le percentuali dei vaccinati sono spesso errate in quanto oscillano di giorno in giorno, quindi questo valore viene ricalcolato riferendosi alla popolazione censita dall'ISTAT. La percentuale di vaccini utilizzati può spesso **superare il 100%** (per esempio, in Campania e Umbria).

Non ho modo di correggere questo tipo di errori (presumo siano tali, perlomeno) che vengono quindi riportati come fossero cifre corrette. I dati esplicitamente sbagliati sono riportati con il colore rosso.

Calcolare la percentuale dei vaccinati di ogni territorio si sta dimostrando affare per nulla semplice. Difatti, non è disponibile il valore in tempo reale delle prime e seconde dosi inoculate divise per territorio e le percentuali ufficiali tendono... ad oscillare. Per ora questo valore è calcolato facendo il rapporto tra il totale di dosi consegnate e la popolazione di un territorio, ma presto (grazie ai richiami, o perlomeno così mi auguro) questa stima non sarà più corretta.

Attualmente, questo valore viene calcolato dapprima sommando il numero di prime e seconde dosi inoculate in ogni territorio, poi sottraendo il numero di seconde dose inoculate il giorno precedente nel territorio stesso. Così la percentuale non sarà accurata al 100% ma il valore trovato sarà molto simile a quello reale (soprattutto all'aumentare del numero totale di vaccinazioni).

Infine, i dati vengono spesso aggiornati ben oltre la **mezzanotte**. Per quanto sia *abbastanza sicuro* che nessuno venga vaccinato in orario di chiusura di ospedali ed ambulatori, questi dati vengono considerati validi per il giorno corrente e non vengono conteggiati rispetto al giorno precedente.

*I dati sono aggiornati 4 volte all'ora.*

## Dettagli tecnici

Il back-end è scritto in *Python* facendo uso del framework *Flask*, mentre il front-end è scritto in *ECMAScript 2020* (il vecchio *JavaScript*) insieme alla librerie *jQuery* e *Chart.js* (per i grafici) senza fare uso di framework CSS per lo styling. Non so quanto sia un vantaggio, ma l'intero sito (dati esclusi) pesa solo ~200KB.

Il file GeoJson della mappa italiana è stata ottenuta modificando leggermente [questa](https://gist.github.com/datajournalism-it/f1abb68e718b54f6a0fe) repository, dapprima modificando le feauture per includere i nomi "corretti" (così come forniti dal Ministero della salute) e i codici ISTAT delle province, poi per ridurne la dimensione da ~3MB a ~45KB usando [questo sito](https://mapshaper.org/). La dimensione totale dei file trasferiti è passata da ~6MB a ~500KB (e la banda ringrazia).

### Service setup file

*Posizione:*

`/etc/systemd/system/vaccino-covid19.service`

*Contenuto:*

```plaintext
[Unit]
Description=Gunicorn instance to serve vaccino-covid19
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/vaccino-covid19/vaccinocovid19
Environment="PATH=/root/vaccino-covid19/vaccinocovid19/venv/bin"
ExecStart=gunicorn --workers 4 --bind 127.0.0.1:8000 wsgi:app --preload
[Install]
WantedBy=multi-user.target
```

*Avvio, pausa e riavvio:*

```bash
sudo systemctl start vaccino-covid19
sudo systemctl enable vaccino-covid19
sudo systemctl stop vaccino-covid19
sudo systemctl restart vaccino-covid19

### Nginx setup file
*Posizione:*

`/etc/nginx/sites-available/vaccino-covid19`

*Contenuto*

```plaintext
server {
  server_name vaccinocovid19.live www.vaccinocovid19.live;
  location / {
    include proxy_params;
    proxy_pass http://127.0.0.1:8000;
  }
}
```

## Licenza

Il sito  è distribuito con Licenza Creative Commons - Attribuzione Non commerciale 4.0 Internazionale
