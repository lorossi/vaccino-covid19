# Vaccini covid-19 italia
Controlla in tempo reale (o quasi) la distribuzione del vaccino contro il covid in Italia.

# Link: https://www.vaccinocovid19.live/

## Fonte dei dati
I dati sono presi direttamente dalla [dashboard Ministeriale](https://app.powerbi.com/view?r=eyJrIjoiMzg4YmI5NDQtZDM5ZC00ZTIyLTgxN2MtOTBkMWM4MTUyYTg0IiwidCI6ImFmZDBhNzVjLTg2NzEtNGNjZS05MDYxLTJjYTBkOTJlNDIyZiIsImMiOjh9) e vengono manipolati dal server per venire mostrati con più agio.

**Saltuariamente** i dati forniti dal Ministero sono **errrati**: il numero di nuovi vaccinati può essere **negativo** e il totale dei vaccinati può **non coincidere** con quanto risulta dalla somma delle tabelle dei vaccinati relativi per fasce di età, impiego o sesso. Le percentuali dei vaccinati sono spesso errate in quanto oscillano di giorno in giorno, quindi questo valore viene ricalcolato riferendosi alla popolazione censita dall'ISTAT. La percentuale di vaccini utilizzati può spesso **superare il 100%** (per esempio, in Campania e Umbria).

Non ho modo di correggere questo tipo di errori (presumo siano tali, perlomeno) che vengono quindi riportati come fossero cifre corrette. I dati esplicitamente sbagliati sono riportati con il colore rosso.

Infine, i dati vengono spesso aggiornati ben oltre la **mezzanotte**. Per quanto sia *abbastanza sicuro* che nessuno venga vaccinato in orario di chiusura di ospedali ed ambulatori, questi dati vengono considerati validi per il giorno corrente e non vengono conteggiati rispetto al giorno precedente.

*I dati sono aggiornati 4 volte all'ora.*

## Dettagli tecnici
Il back-end è scritto in *Python* facendo uso del framework *Flask*, mentre il front-end è scritto in *ECMAScript 2020* (il vecchio *JavaScript*) insieme alla librerie *jQuery* e *Chart.js* (per i grafici) senza fare uso di framework CSS per lo styling,

### Service setup file
*Posizione:*

`/etc/systemd/system/vaccino-covid19.service`

*Contenuto:*

```
[Unit]
Description=Gunicorn instance to serve vaccino-covid19
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/user/vaccino-covid19/vaccinocovid19
Environment="PATH=/user/vaccino-covid19/vaccinocovid19/venv/bin"
ExecStart=gunicorn --workers 4 --bind 127.0.0.1:8000 wsgi:app -e GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git --preload

[Install]
WantedBy=multi-user.target
```
