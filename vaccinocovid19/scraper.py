# Made by Lorenzo Rossi
# https://www.lorenzoros.si - https://github.com/lorossi

import copy
import ujson
import locale
import logging
import requests
import subprocess
from bs4 import BeautifulSoup
from collections import Counter
from pathlib import Path
from datetime import datetime, timedelta


class Scraper:
    def __init__(self, log=True, verbose=True):
        locale.setlocale(locale.LC_ALL, '')
        self.log = log
        self.verbose = verbose
        self._last_updated = None
        self._data = {}
        self._italy = {}
        self._history = {}
        self._deliveries = {}
        self._territories_color = {}
        self._vaccine_producers = {}
        self._territories_data = None
        if self.log:
            logfile = "logging.log"
            logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                                level=logging.INFO, filename=logfile,
                                filemode="w")
        if self.verbose:
            if self.log:
                (f"Logging in {logfile}")
            else:
                ("No logging in file.")

        self.loadSettings()

    def loadSettings(self):
        with open("src/settings/settings.json") as f:
            settings = ujson.loads(f.read())

        self.output_path = settings["output_path"]
        self.producers_filename = settings["producers_filename"]
        self.history_filename = settings["history_filename"]
        self.today_filename = settings["today_filename"]
        self.italy_filename = settings["italy_filename"]
        self.colors_filename = settings["colors_filename"]

        self._territories_list = []
        if not self._territories_data:
            with open("src/settings/territories_data.json", "r") as f:
                self._territories_data = ujson.load(f)

                for territory in self._territories_data:
                    self._territories_list.append(territory["nome"])

    def saveData(self):
        # create output folders
        logging.info("Creating folders")
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        logging.info("Saving to file")

        if self._vaccine_producers:
            with open(self.output_path + self.producers_filename, "w") as f:
                ujson.dump(self._vaccine_producers, f, indent=2, sort_keys=True)
            logging.info(f"Today file saved. Path: {self.producers_filename}")

        if self._data:
            with open(self.output_path + self.today_filename, "w") as f:
                ujson.dump(self._data, f, indent=2, sort_keys=True)
            logging.info(f"Today file saved. Path: {self.today_filename}")

            with open(self.output_path + self.italy_filename, "w") as f:
                ujson.dump(self._italy, f, indent=2, sort_keys=True)
            logging.info(f"Italy file saved. Path: {self.italy_filename}")

        if self._history:
            with open(self.output_path + self.history_filename, "w") as f:
                # convert dict to json (will be read by js)
                f.write(ujson.dumps(self._history, indent=2, sort_keys=True))
            logging.info(f"JSON history file saved. Path: {self.history_filename}")

        if self._territories_color:
            with open(self.output_path + self.colors_filename, "w") as f:
                # convert dict to json (will be read by js)
                f.write(ujson.dumps(self._territories_color, indent=2, sort_keys=True))
            logging.info(f"JSON history file saved. Path: {self.colors_filename}")

    def loadData(self, all=False, producers=False, today=False, history=False, italy=False, colors=False):
        if producers or all:
            try:
                with open(self.output_path + self.producers_filename, "r") as f:
                    self._vaccine_producers = ujson.load(f)
            except Exception as e:
                logging.error(f"Cannot read data file. error {e}")
                self._vaccine_producers = {}

        if today or all:
            try:
                with open(self.output_path + self.today_filename, "r") as f:
                    self._data = ujson.load(f)
            except Exception as e:
                logging.error(f"Cannot read data file. error {e}")
                self._data = {}

        if history or all:
            try:
                with open(self.output_path + self.history_filename, "r") as f:
                    self._history = ujson.load(f)
            except Exception as e:
                logging.error(f"Cannot read history file. error {e}")
                self._history = {}
        if italy or all:
            try:
                with open(self.output_path + self.italy_filename, "r") as f:
                    self._italy = ujson.load(f)
            except Exception as e:
                logging.error(f"Cannot read italy file. error {e}")
                self._italy = {}

        if colors or all:
            try:
                with open(self.output_path + self.colors_filename, "r") as f:
                    self._territories_color = ujson.load(f)
            except Exception as e:
                logging.error(f"Cannot read colors file. error {e}")
                self._territories_color = {}

    def returnTerritoryData(self, area):
        # load territories population
        if not self._territories_data:
            with open("src/settings/territories_data.json", "r") as f:
                self._territories_data = ujson.load(f)

        for territory in self._territories_data:
            if territory["area"] == area:
                return territory

    def returnTerritoryCode(self, name):
        if not self._territories_data:
            with open("src/settings/territories_data.json", "r") as f:
                self._territories_data = ujson.load(f)

        for territory in self._territories_data:
            if territory["nome"] == name or territory.get("nome_alternativo", None) == name:
                return territory["codice"]

    def scrapeDeliveries(self):
        # initialize old data
        with open("src/settings/urls.json", "r") as f:
            payloads = ujson.load(f)
        # load variation territories data
        json_response = None
        for p in payloads:
            if p["name"] == "consegne-vaccini":
                response = requests.get(p["url"]).text
                json_response = ujson.loads(response)
                break

        # load vaccines brands
        new_vaccine_producers = {
            "produttori": []
        }
        new_vaccine_producers["timestamp"] = datetime.now().isoformat()
        brands = list(set(x["fornitore"] for x in json_response["data"]))
        for brand in brands:
            new_vaccine_producers["produttori"].append({
                "nome_produttore": brand,
                "totale_dosi_consegnate": 0
            })

        for delivery in json_response["data"]:
            for producer in new_vaccine_producers["produttori"]:
                if producer["nome_produttore"] == delivery["fornitore"]:
                    producer["totale_dosi_consegnate"] += delivery["numero_dosi"]
                    break

        for producer in new_vaccine_producers["produttori"]:
            producer["totale_dosi_consegnate_formattato"] = f'{producer["totale_dosi_consegnate"]:n}'

        areas_list = sorted(list(set(x["area"] for x in json_response["data"])))
        timestamps_list = sorted(list(set(x["data_consegna"] for x in json_response["data"])))
        new_deliveries = []

        for t in range(len(timestamps_list)):
            # skip first and last (current) day
            current_day = [x for x in json_response["data"] if x["data_consegna"] == timestamps_list[t]]
            current_day_time = datetime.strptime(timestamps_list[t][:-5], "%Y-%m-%dT%H:%M:%S")
            script_timestamp = current_day_time.strftime("%Y-%m-%d")

            new_delivery_day = {}
            new_delivery_day["timestamp"] = script_timestamp
            new_delivery_day["data_consegna"] = timestamps_list[t]
            new_delivery_day["variazioni"] = []

            total_delivered = 0
            for a in range(len(areas_list)):
                # calculate absolute
                territories = [x for x in current_day if x["area"] == areas_list[a]]

                if len(territories) > 0:
                    # init new dict
                    new_variation = {}
                    # load data from file
                    territory_data = self.returnTerritoryData(areas_list[a])
                    # start filling new dict
                    new_variation["area"] = areas_list[a]
                    new_variation["nuove_dosi_consegnate"] = 0

                    for territory in territories:
                        new_variation["nuove_dosi_consegnate"] += territory["numero_dosi"]

                    total_delivered += new_variation["nuove_dosi_consegnate"]
                new_delivery_day["variazioni"].append(new_variation)

            new_delivery_day["variazioni"].append({"area": "ITA", "nuove_dosi_consegnate": total_delivered})
            new_deliveries.append(new_delivery_day)

        self._deliveries = copy.deepcopy(new_deliveries)
        self._vaccine_producers = copy.deepcopy(new_vaccine_producers)

    def scrapeHistory(self):
        # first of all, scrape the deliveries
        self.scrapeDeliveries()
        # initialize old data
        with open("src/settings/urls.json", "r") as f:
            payloads = ujson.load(f)
        # load variation territories data
        json_response = None
        for p in payloads:
            if p["name"] == "somministrazioni-vaccini-summary-latest":
                response = requests.get(p["url"]).text
                json_response = ujson.loads(response)
                break

        areas_list = sorted(list(set(x["area"] for x in json_response["data"])))
        timestamps_list = sorted(list(set(x["data_somministrazione"] for x in json_response["data"])))
        new_history = []

        for t in range(1, len(timestamps_list)):
            # skip first and last (current) day
            current_day = [x for x in json_response["data"] if x["data_somministrazione"] == timestamps_list[t]]
            current_deliveries = [x for x in self._deliveries if x["data_consegna"] == timestamps_list[t]]

            current_day_time = datetime.strptime(timestamps_list[t][:-5], "%Y-%m-%dT%H:%M:%S")
            script_timestamp = current_day_time.strftime("%Y-%m-%d")

            new_history_day = {}
            new_history_day["timestamp"] = script_timestamp
            new_history_day["assoluti"] = []
            new_history_day["variazioni"] = []

            for a in range(len(areas_list)):
                # calculate absolute
                territory = [x for x in current_day if x["area"] == areas_list[a]]

                if len(territory) > 0:
                    territory = territory[0]
                else:
                    territory = {}

                # init new dict
                new_variation = {}
                # load data from file
                territory_data = self.returnTerritoryData(areas_list[a])
                # start filling new dict
                new_variation["codice_territorio"] = territory_data["codice"]
                new_variation["nome_territorio"] = territory_data["nome"]
                new_variation["nome_territorio_corto"] = territory_data["nome_corto"]

                new_variation["nuovi_vaccinati"] = territory.get("prima_dose", 0) + territory.get("seconda_dose", 0)
                new_variation["nuove_prime_dosi"] = territory.get("prima_dose", 0)
                new_variation["nuove_seconde_dosi"] = territory.get("seconda_dose", 0)
                new_variation["nuovi_sesso"] = {
                    "uomini": territory.get("sesso_maschile", 0),
                    "donne": territory.get("sesso_femminile", 0)
                }
                new_variation["nuovi_categoria"] = {
                    "categoria_operatori_sanitari_sociosanitari": territory.get("categoria_operatori_sanitari_sociosanitari", 0),
                    "personale_non_sanitario": territory.get("categoria_personale_non_sanitario", 0),
                    "categoria_ospiti_rsa": territory.get("categoria_ospiti_rsa", 0),
                    "over_80": territory.get("categoria_over80", 0)
                }

                total_new_delivered = 0
                if len(current_deliveries) > 0:
                    territory_delivery = [x for x in current_deliveries[0]["variazioni"] if x["area"] == areas_list[a]][:-1]
                    if len(territory_delivery) > 0:
                        for delivery in territory_delivery:
                            total_new_delivered += delivery["nuove_dosi_consegnate"]
                new_variation["nuove_dosi_consegnate"] = total_new_delivered

                new_absolute = {}
                new_absolute["codice_territorio"] = territory_data["codice"]
                new_absolute["nome_territorio"] = territory_data["nome"]
                new_absolute["nome_territorio_corto"] = territory_data["nome_corto"]

                if t > 0:
                    # compute total
                    old_days = [x for x in json_response["data"] if x["area"] == areas_list[a] and current_day_time > datetime.strptime(x["data_somministrazione"][:-5], "%Y-%m-%dT%H:%M:%S")]
                    # append today (if found)
                    old_days.append(territory)
                    # sum all data and discard the useless one
                    total = Counter()
                    for day in old_days:
                        total.update(day)

                    new_absolute["totale_vaccinati"] = total.get("prima_dose", 0) + total.get("seconda_dose", 0)
                    new_absolute["percentuale_vaccinati"] = new_absolute["totale_vaccinati"] / territory_data["popolazione"] * 100
                    new_absolute["percentuale_vaccinati_formattato"] = f'{new_absolute["percentuale_vaccinati"]:.2f}%'

                    new_absolute["prime_dosi"] = total.get("prima_dose", 0)
                    new_absolute["seconde_dosi"] = total.get("seconda_dose", 0)
                    new_absolute["sesso"] = {
                        "uomini": total.get("sesso_maschile", 0),
                        "donne": total.get("sesso_femminile", 0)
                    }
                    new_absolute["categoria"] = {
                        "operatori_sanitari_sociosanitari": total.get("categoria_operatori_sanitari_sociosanitari", 0),
                        "personale_non_sanitario": total.get("categoria_personale_non_sanitario", 0),
                        "ospiti_rsa": total.get("categoria_ospiti_rsa", 0),
                        "over_80": total.get("categoria_over80", 0)
                    }

                    old_deliveries = [x for x in self._deliveries if current_day_time > datetime.strptime(x["data_consegna"][:-5], "%Y-%m-%dT%H:%M:%S")]
                    old_deliveries = [x for sublist in old_deliveries for x in sublist["variazioni"]]
                    old_territory_deliveries = [x for x in old_deliveries if x["area"] == areas_list[a]]

                    total_delivered = 0
                    if len(old_territory_deliveries) > 0:
                        for delivery in old_territory_deliveries:
                            total_delivered += delivery["nuove_dosi_consegnate"]
                    new_absolute["totale_dosi_consegnate"] = total_delivered


                new_history_day["variazioni"].append(new_variation)
                new_history_day["assoluti"].append(new_absolute)
            new_history.append(new_history_day)

        self._history = copy.deepcopy(new_history)

    def scrapeData(self):
        # initialize dictionaries
        # load payload and url
        with open("src/settings/urls.json", "r") as f:
            payloads = ujson.load(f)

        # load today
        today_timestamp = datetime.now().strftime("%Y-%m-%d")
        # load yesterday
        yesterday_time = datetime.now().replace(hour=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_timestamp = yesterday_time.strftime("%Y-%m-%d")
        yesterday_data = [x for x in self._history if x["timestamp"] == yesterday_timestamp][0]

        today_deliveries = [x for x in self._deliveries if x["timestamp"] == today_timestamp]
        if len(today_deliveries) > 0:
            today_deliveries = [x for x in y for y in today_deliveries]
        else:
            today_deliveries = []

        self._data["timestamp"] = datetime.now().isoformat()
        self._data["timestamp"] = datetime.now().strftime("%Y-%m-%d ore %H:%M")
        self._italy["ultimo_aggiornamento"] = datetime.now().strftime("%Y-%m-%d ore %H:%M")

        new_data = {
            "assoluti": [],
            "variazioni": [],
            "categorie": [],
            "sesso": [],
            "fasce_eta": [],
            "somministrazioni": []
            }

        new_italy_absolute = {
            "codice_territorio": "00",
            "nome_territorio": "Italia",
            "nome_territorio_corto": "Italia",
        }

        new_italy_variation = copy.deepcopy(new_italy_absolute)

        # load absolute territories data
        json_response = None
        for p in payloads:
            if p["name"] == "vaccini-summary-lastest":
                response = requests.get(p["url"]).text
                json_response = ujson.loads(response)
                break

        for territory in json_response["data"]:
            # init new dict
            new_absolute = {}
            # load data from file
            territory_data = self.returnTerritoryData(territory["area"])
            # start filling new dict
            new_absolute["codice_territorio"] = territory_data["codice"]
            new_absolute["nome_territorio"] = territory_data["nome"]
            new_absolute["nome_territorio_corto"] = territory_data["nome_corto"]
            new_absolute["totale_dosi_consegnate"] = territory["dosi_consegnate"]
            new_absolute["totale_vaccinati"] = territory["dosi_somministrate"]
            # calculations
            new_absolute["percentuale_dosi_utilizzate"] = new_absolute["totale_vaccinati"] / new_absolute["totale_dosi_consegnate"] * 100
            new_absolute["percentuale_popolazione_vaccinata"] = new_absolute["totale_vaccinati"] / territory_data["popolazione"] * 100
            # format numbers
            new_absolute["totale_dosi_consegnate_formattato"] = f'{territory["dosi_consegnate"]:n}'
            new_absolute["totale_vaccinati_formattato"] = f'{territory["dosi_somministrate"]:n}'
            new_absolute["percentuale_dosi_utilizzate_formattato"] = f'{new_absolute["percentuale_dosi_utilizzate"]:.2f}%'
            new_absolute["percentuale_popolazione_vaccinata_formattato"] = f'{new_absolute["percentuale_popolazione_vaccinata"]:.2f}%'

            # update italy
            new_italy_absolute["totale_dosi_consegnate"] = new_italy_absolute.get("totale_dosi_consegnate", 0) + new_absolute["totale_dosi_consegnate"]
            new_italy_absolute["totale_vaccinati"] = new_italy_absolute.get("totale_vaccinati", 0) + new_absolute["totale_vaccinati"]
            # add dict to data
            new_data["assoluti"].append(new_absolute)

            # calculate variations
            yesterday_absolute = [x for x in yesterday_data["assoluti"] if x["codice_territorio"] == territory_data["codice"]][0]

            new_variation = {}
            new_variation["codice_territorio"] = territory_data["codice"]
            new_variation["nome_territorio"] = territory_data["nome"]
            new_variation["nome_territorio_corto"] = territory_data["nome_corto"]

            new_variation["nuovi_vaccinati"] = new_absolute["totale_vaccinati"] - yesterday_absolute["totale_vaccinati"]
            new_variation["nuovi_vaccinati_formattato"] = f'{new_variation["nuovi_vaccinati"]:n}'
            new_variation["percentuale_nuovi_vaccinati"] = new_variation["nuovi_vaccinati"] / yesterday_absolute["totale_vaccinati"] * 100
            new_variation["percentuale_nuovi_vaccinati_formattato"] = f'{new_variation["percentuale_nuovi_vaccinati"]:.2f}%'

            # should be tied to self._deliveries, not self._history
            # BUT there isn't always data for yesterday deliveries
            territory_delivery = [x for x in today_deliveries if x["area"] == territory["area"]]
            if len(territory_delivery) == 0:
                territory_delivery = {}
            else:
                territory_delivery = territory_delivery[0]

            new_variation["nuove_dosi_consegnate"] = territory_delivery.get("nuove_dosi_consegnate", 0)
            new_variation["nuove_dosi_consegnate_formattato"] = f'{new_variation["nuove_dosi_consegnate"]:n}'
            new_variation["percentuale_nuove_dosi_consegnate"] = new_variation["nuove_dosi_consegnate"] / yesterday_absolute["totale_dosi_consegnate"] * 100
            new_variation["percentuale_nuove_dosi_consegnate_formattato"] = f'{new_variation["percentuale_nuove_dosi_consegnate"]:.2f}%'

            # update italy
            new_italy_variation["nuovi_vaccinati"] = new_italy_variation.get("nuovi_vaccinati", 0) + new_variation["nuovi_vaccinati"]
            new_italy_variation["nuove_dosi_consegnate"] = new_italy_variation.get("nuove_dosi_consegnate", 0) + new_variation["nuove_dosi_consegnate"]
            # add dict to data
            new_data["variazioni"].append(new_variation)


        # compute italy
        italy_data = self.returnTerritoryData("ITA")
        new_italy_absolute["totale_dosi_consegnate_formattato"] = f'{new_italy_absolute["totale_dosi_consegnate"]:n}'
        new_italy_absolute["totale_vaccinati_formattato"] = f'{new_italy_absolute["totale_vaccinati"]:n}'
        new_italy_absolute["percentuale_dosi_utilizzate"] = new_italy_absolute["totale_vaccinati"] / new_italy_absolute["totale_dosi_consegnate"] * 100
        new_italy_absolute["percentuale_popolazione_vaccinata"] = new_italy_absolute["totale_vaccinati"] / italy_data["popolazione"] * 100
        new_italy_absolute["percentuale_dosi_utilizzate_formattato"] = f'{new_italy_absolute["percentuale_dosi_utilizzate"]:.2f}%'
        new_italy_absolute["percentuale_popolazione_vaccinata_formattato"] = f'{new_italy_absolute["percentuale_popolazione_vaccinata"]:.2f}%'
        new_italy_variation["nuovi_vaccinati_formattato"] = f'{new_italy_variation["nuovi_vaccinati"]:n}'
        new_italy_variation["nuove_dosi_consegnate_formattato"] =  f'{new_italy_variation["nuove_dosi_consegnate"]:n}'

        self._italy.update(new_italy_absolute)
        self._italy.update(new_italy_variation)

        # load categories and age ranges data
        json_response = None
        for p in payloads:
            if p["name"] == "anagrafica-vaccini":
                response = requests.get(p["url"]).text
                json_response = ujson.loads(response)
                break

        yesterday_absolute = [x for x in yesterday_data["assoluti"] if x["codice_territorio"] == "00"][0]

        categories_list = [x for x in json_response["data"][0] if "categoria" in x]
        categories = []
        count = 0
        for c in categories_list:
            new_dict = {
                "id": count,
                "nome_categoria": c,
                "nome_categoria_pulito": c.replace("categoria_", "").replace("over80", "over_80"),
                "nome_categoria_formattato": c.replace("categoria_", "").replace("over80", "over_80").replace("_", " "),
                "totale_vaccinati": 0,
                "totale_vaccinati_formattato": "0"
            }
            categories.append(new_dict)
            count += 1

        genders = [{"nome_categoria": "uomini", "totale_vaccinati": 0}, {"nome_categoria": "donne", "totale_vaccinati": 0}]
        subministrations = [{"nome_categoria": "prima_dose", "totale_vaccinati": 0}, {"nome_categoria": "seconda_dose", "totale_vaccinati": 0}]

        for age in json_response["data"]:
            age_range = {}
            age_range["nome_categoria"] = age["fascia_anagrafica"]
            age_range["totale_vaccinati"] = age["totale"]
            age_range["totale_vaccinati_formattato"] = f'{age["totale"]:n}'
            age_range["prima_dose"] = age["prima_dose"]
            age_range["sprima_dose_formattato"] = f'{age["prima_dose"]:n}'
            age_range["seconda_dose"] = age["seconda_dose"]
            age_range["seconda_dose_formattato"] = f'{age["seconda_dose"]:n}'
            # add variation

            new_data["fasce_eta"].append(age_range)

            for category in categories:
                for category_name in categories_list:
                    if category["nome_categoria"] == category_name:
                        category["totale_vaccinati"] += age[category_name]
                        break

            for gender in genders:
                if gender["nome_categoria"] == "uomini":
                    gender["totale_vaccinati"] += age["sesso_maschile"]
                elif gender["nome_categoria"] == "donne":
                    gender["totale_vaccinati"] += age["sesso_femminile"]

            for subministration in subministrations:
                subministration["nome_categoria_formattato"] = subministration["nome_categoria"].replace("_", " ")
                if subministration["nome_categoria"] == "prima_dose":
                    subministration["totale_vaccinati"] += age["prima_dose"]
                elif subministration["nome_categoria"] == "seconda_dose":
                    subministration["totale_vaccinati"] += age["seconda_dose"]

        for category in categories:
            category["totale_vaccinati_formattato"] = f'{category["totale_vaccinati"]:n}'
            category["nuovi_vaccinati"] = category["totale_vaccinati"] - yesterday_absolute["categoria"][category["nome_categoria_pulito"]]
            category["nuovi_vaccinati_formattato"] = f'{category["nuovi_vaccinati"]:n}'
            category["nuovi_vaccinati_percentuale"] = category["nuovi_vaccinati"] / yesterday_absolute["categoria"][category["nome_categoria_pulito"]] * 100
            category["nuovi_vaccinati_percentuale_formattato"] = f'{category["nuovi_vaccinati_percentuale"]:.2f}%'
            new_data["categorie"].append(category)

        for gender in genders:
            gender["totale_vaccinati_formattato"] = f'{gender["totale_vaccinati"]:n}'
            gender["nuovi_vaccinati"] = gender["totale_vaccinati"] - yesterday_absolute["sesso"][gender["nome_categoria"]]
            gender["nuovi_vaccinati_formattato"] = f'{gender["nuovi_vaccinati"]:n}'
            gender["nuovi_vaccinati_percentuale"] = gender["nuovi_vaccinati"] / yesterday_absolute["sesso"][gender["nome_categoria"]] * 100
            gender["nuovi_vaccinati_percentuale_formattato"] = f'{gender["nuovi_vaccinati_percentuale"]:.2f}%'
            new_data["sesso"].append(gender)

        for subministration in subministrations:
            subministration["totale_vaccinati_formattato"] = f'{subministration["totale_vaccinati"]:n}'
            new_data["somministrazioni"].append(subministration)

        self._italy["somministrazioni"] = {
            "prima_dose": subministrations[0]["totale_vaccinati"],
            "prima_dose_formattato": subministrations[0]["totale_vaccinati_formattato"],
            "seconda_dose": subministrations[1]["totale_vaccinati"],
            "seconda_dose_formattato": subministrations[1]["totale_vaccinati_formattato"]
        }

        self._data = copy.deepcopy(new_data)

    def scrapeColors(self):
        timestamp = datetime.now().isoformat()
        new_territories_colors = {
            "timestamp": timestamp,
            "territori": []
        }

        # initialize old data
        with open("src/settings/urls.json", "r") as f:
            payloads = ujson.load(f)
        # load variation territories data
        soup = None
        for p in payloads:
            if p["name"] == "colore-territori":
                response = requests.get(p["url"]).text
                soup = BeautifulSoup(response, 'html.parser')
                break

        classes = ["redText", "orangeText", "yellowText"]
        count = 0
        for c in classes:
            territories = soup.body.find("td", class_=c).p.text.strip().replace("\t", "").split("\n")
            for t in territories:
                new_territories_colors["territori"].append({
                    "territorio": t,
                    "codice": int(self.returnTerritoryCode(t)),
                    "colore": count,
                })

        self._territories_color = copy.deepcopy(new_territories_colors)

    def territoryHistory(self, territory_name):
        self.loadData(history=True)
        territory_history = []

        for day in self._history:
            new_dict = {
                "assoluti": None,
                "variazioni": None,
            }

            for key in new_dict:
                for territory in day[key]:
                    if territory["nome_territorio"] == territory_name:
                        new_dict[key] = territory
                        break
            new_dict["timestamp"] = day["timestamp"]

            territory_history.append(new_dict)

        return territory_history

    def scrapeAll(self):
        self.scrapeHistory()
        self.scrapeData()
        self.scrapeColors()
        self.saveData()

    def printJson(self, data, indent=2, exit=True):
        print(ujson.dumps(data, indent=indent))
        if exit:
            quit()

    def backup(self):
        logging.info("Started backup process")
        # now push all to to github
        # repo folder is parent
        subprocess.run(["git", "pull"], check=True)
        logging.info("Repo pulled")
        try:
            subprocess.run(["git", "commit", "-am", '"updated data"'], check=True)
            logging.info("Commit created")
            subprocess.run(["git", "push"], check=True)
            logging.info("Repo pushed")
        except Exception as e:
            logging.error("Cannot commit or push. Repo is probably already "
                          f"on par with the tree. Error {e}")

    @property
    def italy(self):
        self.loadData(italy=True)
        return self._italy

    @property
    def territories_list(self):
        return self._territories_list

    @property
    def absolute_territories(self):
        self.loadData(today=True)
        return self._data["assoluti"]

    @property
    def variation_territories(self):
        self.loadData(today=True)
        return self._data["variazioni"]


    @property
    def categories(self):
        self.loadData(today=True)
        return self._data["categorie"]


    @property
    def genders(self):
        self.loadData(today=True)
        return self._data["sesso"]

    @property
    def age_ranges(self):
        self.loadData(today=True)
        return self._data["fasce_eta"]

    @property
    def history(self):
        self.loadData(history=True)
        return self._history

    @property
    def territories_color(self):
        self.loadData(colors=True)
        return self._territories_color

    @property
    def vaccine_producers(self):
        self.loadData(producers=True)
        return self._vaccine_producers

    @property
    def subministrations(self):
        self.loadData(today=True)
        return self._data["somministrazioni"]


if __name__ == "__main__":
    s = Scraper()
    s.scrapeAll()
    s.saveData()
