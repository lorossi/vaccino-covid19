# Made by Lorenzo Rossi
# https://www.lorenzoros.si - https://github.com/lorossi
# it's a little bit of a mess, but i'm working on it


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
        # set locale for number formatting
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        self.log = log
        self.verbose = verbose
        self._urls = {}
        # initialize private variables
        self._last_updated = None
        self._data = {}
        self._italy = {}
        self._history = {}
        self._deliveries = {}
        self._territories_color = {}
        self._vaccine_producers = {}
        self._geojson_colors = {}
        self._geojeson_percentages = {}
        self._territories_data = {}

        # start logging
        if self.log:
            logfile = "logging.log"
            logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                                level=logging.INFO, filename=logfile,
                                filemode="w")
        # if necessary, tell user we are logging
        if self.verbose:
            if self.log:
                (f"Logging in {logfile}")
            else:
                ("No logging in file.")

        # now load settigns
        self.loadSettings()

    def loadSettings(self):
        # open settings file
        with open("src/settings/settings.json") as f:
            settings = ujson.loads(f.read())

        # load output paths and output filenames from file
        self.output_path = settings["output_path"]
        self.history_filename = settings["history_filename"]
        self.today_filename = settings["today_filename"]
        self.italy_filename = settings["italy_filename"]
        self.colors_filename = settings["colors_filename"]
        self.colors_geojson_filename = settings["colors_geojson_filename"]
        self.vaccinations_geojeson_filename = settings["vaccinations_geojeson_filename"]

        # open urls file
        with open("src/settings/urls.json") as f:
            self._urls = ujson.loads(f.read())

        # load territories list to be passed to dropdown selector
        self._territories_list = []
        if not self._territories_data:
            with open("src/settings/territories-data.json", "r") as f:
                self._territories_data = ujson.load(f)
                # italy will be on top
                for territory in self._territories_data:
                    self._territories_list.append(territory["nome"])

    def saveData(self):
        # create output folders
        logging.info("Creating folders")
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        logging.info("Saving to file")

        if self._data:
            with open(self.output_path + self.today_filename, "w") as f:
                ujson.dump(self._data, f, indent=2, sort_keys=True)
            logging.info(f"Today file saved. Path: {self.today_filename}")

            with open(self.output_path + self.italy_filename, "w") as f:
                ujson.dump(self._italy, f, indent=2, sort_keys=True)
            logging.info(f"Italy file saved. Path: {self.italy_filename}")

            with open(self.output_path + self.vaccinations_geojeson_filename, "w") as f:
                ujson.dump(self._geojeson_percentages, f)
            logging.info(f"Geojson vaccinations file saved. Path: {self.vaccinations_geojeson_filename}")

        if self._history:
            with open(self.output_path + self.history_filename, "w") as f:
                f.write(ujson.dumps(self._history, indent=2, sort_keys=True))
            logging.info(f"History file saved. Path: {self.history_filename}")

        if self._territories_color:
            with open(self.output_path + self.colors_filename, "w") as f:
                # convert dict to json (will be read by js)
                f.write(ujson.dumps(self._territories_color, indent=2, sort_keys=True))
            logging.info(f"Color file saved. Path: {self.colors_filename}")

            with open(self.output_path + self.colors_geojson_filename, "w") as f:
                # convert dict to json (will be read by js)
                f.write(ujson.dumps(self._geojson_colors, f))
            logging.info(f"Geojson colors file saved. Path: {self.colors_geojson_filename}")

    # load data from json files
    def loadData(self, all=False, today=False, history=False, italy=False,
                 colors=False, colors_geojson=False, percentage_geojson=False):
        # each variable is related to a particular file, so we don't load
        # everything if we only need one variable

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

        if colors_geojson or all:
            try:
                with open(self.output_path + self.colors_geojson_filename, "r") as f:
                    self._geojson_colors = ujson.load(f)
            except Exception as e:
                logging.error(f"Cannot read geojson file. error {e}")
                self._geojson_colors = {}

        if percentage_geojson or all:
            try:
                with open(self.output_path + self.vaccinations_geojeson_filename, "r") as f:
                    self._geojeson_percentages = ujson.load(f)
            except Exception as e:
                logging.error(f"Cannot read geojson file. error {e}")
                self._geojeson_percentages = {}

    # returns data related to a territory (population, territory code, etc)
    # according to its "AREA" as given by json source
    def returnTerritoryData(self, area):
        # load territories population
        if not self._territories_data:
            with open("src/settings/territories-data.json", "r") as f:
                self._territories_data = ujson.load(f)

        for territory in self._territories_data:
            if territory["area"] == area:
                return territory

    # returns data related to a territory (population, territory code, etc)
    # according to its ISTAT territory code
    def returnTerritoryCode(self, name):
        if not self._territories_data:
            with open("src/settings/territories-data.json", "r") as f:
                self._territories_data = ujson.load(f)

        for territory in self._territories_data:
            if territory["nome"] == name or territory.get("nome_alternativo", None) == name:
                return territory["codice"]

    # laod history for one particular territory
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

    # load the deliveries file and get all the useful information
    def scrapeDeliveries(self):
        logging.info("Loading deliveries")

        # load variation territories data
        response = requests.get(self._urls["consegne-vaccini"]).text
        json_response = ujson.loads(response)

        logging.info("Scraping deliveries")
        # initialize dict
        new_vaccine_producers = {
            "produttori": []
        }
        new_vaccine_producers["timestamp"] = datetime.now().isoformat()
        # load list of unique vaccine brands
        brands = list(set(x["fornitore"] for x in json_response["data"]))
        # populate dict
        for brand in brands:
            new_vaccine_producers["produttori"].append({
                "nome_produttore": brand,
                "totale_dosi_consegnate": 0
            })

        # load total number of deliveries
        for delivery in json_response["data"]:
            for producer in new_vaccine_producers["produttori"]:
                if producer["nome_produttore"] == delivery["fornitore"]:
                    producer["totale_dosi_consegnate"] += delivery["numero_dosi"]
                    break

        # load last deliveries
        for producer in new_vaccine_producers["produttori"]:
            # initialize producer if not found
            producer["nuove_dosi_consegnate"] = 0
            # reverse list
            for delivery in json_response["data"][::-1]:
                if producer["nome_produttore"] == delivery["fornitore"]:
                    if datetime.fromisoformat(delivery["data_consegna"][:-1]).date == datetime.now().date:
                        producer["nuove_dosi_consegnate"] = delivery["numero_dosi"]
                        break

        # format the values
        for producer in new_vaccine_producers["produttori"]:
            producer["totale_dosi_consegnate_formattato"] = f'{producer["totale_dosi_consegnate"]:n}'
            producer["nuove_dosi_consegnate_formattato"] = f'{producer["nuove_dosi_consegnate"]:n}'
            producer["nuove_dosi_percentuale"] = producer["nuove_dosi_consegnate"] / producer["totale_dosi_consegnate"] * 100
            producer["nuove_dosi_percentuale_formattato"] = f'{locale.format_string("%.2f", producer["nuove_dosi_percentuale"])}'

        # load list of uninque areas
        areas_list = sorted(list(set(x["area"] for x in json_response["data"])))
        # load list of uninque timestamps list
        timestamps_list = sorted(list(set(x["data_consegna"] for x in json_response["data"])))
        new_deliveries = []

        # iterate through each timestamp
        for t in range(len(timestamps_list)):
            # skip first and last (current) day
            current_day = [x for x in json_response["data"] if x["data_consegna"] == timestamps_list[t]]
            current_day_time = datetime.strptime(timestamps_list[t][:-5], "%Y-%m-%dT%H:%M:%S")
            script_timestamp = current_day_time.strftime("%Y-%m-%d")

            # initialize and populate dict
            new_delivery_day = {
                "timestamp": script_timestamp,
                "data_consegna": timestamps_list[t],
                "variazioni": []
            }

            total_delivered = 0
            # iterate throught each area
            for a in range(len(areas_list)):
                # calculate total number of delivered doses
                territories = [x for x in current_day if x["area"] == areas_list[a]]

                if len(territories) > 0:
                    # initialize and populate dict
                    new_variation = {
                        "area": areas_list[a],
                        "nuove_dosi_consegnate": 0
                    }
                    # update total number of deliveries today
                    for territory in territories:
                        new_variation["nuove_dosi_consegnate"] += territory["numero_dosi"]
                    # update total number of all time deliveries
                    total_delivered += new_variation["nuove_dosi_consegnate"]
                # append to the dict
                new_delivery_day["variazioni"].append(new_variation)
            # data for italy is the sum of all deliveries
            new_delivery_day["variazioni"].append({"area": "ITA", "nuove_dosi_consegnate": total_delivered})
            new_deliveries.append(new_delivery_day)

        # finally copy the generated dicts inside the private variables
        self._deliveries = copy.deepcopy(new_deliveries)
        self._vaccine_producers = copy.deepcopy(new_vaccine_producers)

    def scrapeHistory(self):
        # first of all, scrape the deliveries if needed
        if not self._deliveries:
            self.scrapeDeliveries()

        response = requests.get(self._urls["somministrazioni-vaccini-summary-latest"]).text
        json_response = ujson.loads(response)

        logging.info("Scraping history")
        # load list of uninque areas
        areas_list = sorted(list(set(x["area"] for x in json_response["data"])))
        # load list of uninque timestamps list
        timestamps_list = sorted(list(set(x["data_somministrazione"] for x in json_response["data"])))
        new_history = []

        # iterate through all the timestamps skipping the first day
        for t in range(1, len(timestamps_list) - 1):
            # load all the data relatie to this day
            current_day = [x for x in json_response["data"] if x["data_somministrazione"] == timestamps_list[t]]
            # load all the deliveries relative to this day
            current_deliveries = [x for x in self._deliveries if x["data_consegna"] == timestamps_list[t]]
            # load timestamp relative to this day
            # will be used later in charts
            current_day_time = datetime.strptime(timestamps_list[t][:-5], "%Y-%m-%dT%H:%M:%S")
            script_timestamp = current_day_time.strftime("%Y-%m-%d")

            # initialize and populate dict
            new_history_day = {
                "timestamp": script_timestamp,
                "assoluti": [],
                "variazioni": []
            }

            # data for italy is NOT PROVIDED ANYMORE
            # so all we have to do is treat it differently
            italy_absolute = {
                "codice_territorio": "00",
                "nome_territorio": "Italia",
                "nome_territorio_corto": "Italia"
            }
            italy_variation = copy.deepcopy(italy_absolute)

            # iterate through all the territories (areas)
            for a in range(len(areas_list)):
                # calculate absolute
                territory = [x for x in current_day if x["area"] == areas_list[a]]
                # keep only the first one
                if len(territory) > 0:
                    territory = territory[0]
                else:
                    territory = {}

                # load data from file
                territory_data = self.returnTerritoryData(areas_list[a])

                # init new dict
                new_variation = {}
                # start filling new dict
                new_variation["codice_territorio"] = territory_data["codice"]
                new_variation["nome_territorio"] = territory_data["nome"]
                new_variation["nome_territorio_corto"] = territory_data["nome_corto"]
                # calculate variation
                new_variation["nuovi_vaccinati"] = territory.get("prima_dose", 0) + territory.get("seconda_dose", 0)
                new_variation["nuove_prime_dosi"] = territory.get("prima_dose", 0)
                new_variation["nuove_seconde_dosi"] = territory.get("seconda_dose", 0)
                # calculate variation by gender
                new_variation["nuovi_sesso"] = {
                    "uomini": territory.get("sesso_maschile", 0),
                    "donne": territory.get("sesso_femminile", 0)
                }
                # calculate variation by category
                new_variation["nuovi_categoria"] = {
                    "categoria_operatori_sanitari_sociosanitari": territory.get("categoria_operatori_sanitari_sociosanitari", 0),
                    "personale_non_sanitario": territory.get("categoria_personale_non_sanitario", 0),
                    "categoria_ospiti_rsa": territory.get("categoria_ospiti_rsa", 0),
                    "over_80": territory.get("categoria_over80", 0)
                }

                # calculate the number of new delivered doses
                total_new_delivered = 0
                if len(current_deliveries) > 0:
                    territory_delivery = [x for x in current_deliveries[0]["variazioni"] if x["area"] == areas_list[a]][:-1]
                    if len(territory_delivery) > 0:
                        for delivery in territory_delivery:
                            total_new_delivered += delivery["nuove_dosi_consegnate"]
                new_variation["nuove_dosi_consegnate"] = total_new_delivered

                # now update all data for italy
                italy_variation["nuovi_vaccinati"] = italy_variation.get("nuovi_vaccinati", 0) + new_variation["nuovi_vaccinati"]
                italy_variation["nuove_prime_dosi"] = italy_variation.get("nuove_prime_dosi", 0) + new_variation["nuove_prime_dosi"]
                italy_variation["nuove_seconde_dosi"] = italy_variation.get("nuove_seconde_dosi", 0) + new_variation["nuove_seconde_dosi"]
                italy_variation["nuove_dosi_consegnate"] = italy_variation.get("nuove_dosi_consegnate", 0) + new_variation["nuove_dosi_consegnate"]

                # now update dicts inside the italy dict
                if "nuovi_sesso" in italy_variation:
                    for key, value in new_variation["nuovi_sesso"].items():
                        italy_variation["nuovi_sesso"][key] += value
                else:
                    italy_variation["nuovi_sesso"] = copy.deepcopy(new_variation["nuovi_sesso"])

                if "nuovi_categoria" in italy_variation:
                    for key, value in new_variation["nuovi_categoria"].items():
                        italy_variation["nuovi_categoria"][key] += value
                else:
                    italy_variation["nuovi_categoria"] = copy.deepcopy(new_variation["nuovi_categoria"])

                # init new dict
                new_absolute = {}
                # start filling new dict
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
                    # the percentage of vaccinated people is related to the
                    # population that has received the FIRST DOSE ONLY
                    new_absolute["percentuale_vaccinati"] = total.get("prima_dose", 0) / territory_data["popolazione"] * 100
                    new_absolute["percentuale_vaccinati_formattato"] = f'{locale.format_string("%.2f", new_absolute["percentuale_vaccinati"])}%'

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

                    # load old deliveries and flatten list in order to calculate
                    # the total number of deliveries relative to one day
                    old_deliveries = [x for x in self._deliveries if current_day_time > datetime.strptime(x["data_consegna"][:-5], "%Y-%m-%dT%H:%M:%S")]
                    old_deliveries = [x for sublist in old_deliveries for x in sublist["variazioni"]]
                    old_territory_deliveries = [x for x in old_deliveries if x["area"] == areas_list[a]]
                    # loop throught all the deliveries to calculate the total
                    total_delivered = 0
                    if len(old_territory_deliveries) > 0:
                        for delivery in old_territory_deliveries:
                            total_delivered += delivery["nuove_dosi_consegnate"]
                    new_absolute["totale_dosi_consegnate"] = total_delivered

                    # now update all data for italy
                    italy_absolute["totale_vaccinati"] = italy_absolute.get("totale_vaccinati", 0) + new_absolute["totale_vaccinati"]
                    italy_absolute["prime_dosi"] = italy_absolute.get("prime_dosi", 0) + new_absolute["prime_dosi"]
                    italy_absolute["seconde_dosi"] = italy_absolute.get("seconde_dosi", 0) + new_absolute["seconde_dosi"]
                    italy_absolute["totale_dosi_consegnate"] = italy_absolute.get("totale_dosi_consegnate", 0) + new_absolute["totale_dosi_consegnate"]

                    # now update dicts inside the italy dict
                    if "sesso" in italy_absolute:
                        for key, value in new_absolute["sesso"].items():
                            italy_absolute["sesso"][key] += value
                    else:
                        italy_absolute["sesso"] = copy.deepcopy(new_absolute["sesso"])

                    if "categoria" in italy_absolute:
                        for key, value in new_absolute["categoria"].items():
                            italy_absolute["categoria"][key] += value
                    else:
                        italy_absolute["categoria"] = copy.deepcopy(new_absolute["categoria"])

                # finally append the dicts to the history list
                new_history_day["variazioni"].append(new_variation)
                new_history_day["assoluti"].append(new_absolute)

            territory_data = self.returnTerritoryData("ITA")
            italy_absolute["percentuale_vaccinati"] = italy_absolute.get("prime_dosi", 0) / territory_data["popolazione"] * 100
            italy_absolute["percentuale_vaccinati_formattato"] = f'{locale.format_string("%.2f", italy_absolute["percentuale_vaccinati"])}%'

            new_history_day["variazioni"].append(italy_variation)
            new_history_day["assoluti"].append(italy_absolute)

            new_history.append(new_history_day)

        # copy the new variable inside the private variable
        self._history = copy.deepcopy(new_history)

    def scrapeData(self):
        # initialize dictionaries
        # load today
        today_timestamp = datetime.now().strftime("%Y-%m-%d")
        # load yesterday
        yesterday_time = datetime.now().replace(hour=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_timestamp = yesterday_time.strftime("%Y-%m-%d")
        yesterday_data = [x for x in self._history if x["timestamp"] == yesterday_timestamp]
        if len(yesterday_data) > 0:
            yesterday_data = yesterday_data[0]
        else:
            yesterday_data = None

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
            "somministrazioni": [],
            "produttori_vaccini": self._vaccine_producers["produttori"]
            }

        new_italy_absolute = {
            "codice_territorio": "00",
            "nome_territorio": "Italia",
            "nome_territorio_corto": "Italia",
        }

        new_italy_variation = copy.deepcopy(new_italy_absolute)

        logging.info("Loading data")
        # load absolute territories data
        response = requests.get(self._urls["vaccini-summary-latest"]).text
        json_response = ujson.loads(response)

        logging.info("Scraping data")
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
            # the percentage of vaccinated people is related to the
            # population that has received the FIRST DOSE ONLY
            # in order to calculate that, we subract the number of second
            # doses from the precedent day to the number of total doses today
            # it is not 100% accurate but will work
            if yesterday_data:
                for yesterday_territory in yesterday_data["assoluti"]:
                    if yesterday_territory["codice_territorio"] == new_absolute["codice_territorio"]:
                        new_absolute["percentuale_popolazione_vaccinata"] = (new_absolute["totale_vaccinati"] - yesterday_territory["seconde_dosi"]) / territory_data["popolazione"] * 100
            else:
                new_absolute["percentuale_popolazione_vaccinata"] = 0

                # fallback
                last_day = datetime.now().replace(hour=0, second=0, microsecond=0) - timedelta(days=1)
                for i in range(len(self._history)):
                    last_day -= timedelta(days=1)
                    last_timestamp = last_day.strftime("%Y-%m-%d")
                    last_data = [x for x in self._history if x["timestamp"] == last_timestamp]
                    if len(last_data) > 0:
                        last_data = last_data[0]
                        break
                # ugly af
                if last_data:
                    for last_territory in last_data["assoluti"]:
                        if last_territory["codice_territorio"] == new_absolute["codice_territorio"]:
                            new_absolute["percentuale_popolazione_vaccinata"] = (new_absolute["totale_vaccinati"] - last_territory["seconde_dosi"]) / territory_data["popolazione"] * 100

            # format numbers
            new_absolute["totale_dosi_consegnate_formattato"] = f'{territory["dosi_consegnate"]:n}'
            new_absolute["totale_vaccinati_formattato"] = f'{territory["dosi_somministrate"]:n}'
            new_absolute["percentuale_dosi_utilizzate_formattato"] = f'{locale.format_string("%.2f", new_absolute["percentuale_dosi_utilizzate"])}%'
            new_absolute["percentuale_popolazione_vaccinata_formattato"] = f'{locale.format_string("%.2f", new_absolute["percentuale_popolazione_vaccinata"])}%'

            # update italy
            new_italy_absolute["totale_dosi_consegnate"] = new_italy_absolute.get("totale_dosi_consegnate", 0) + new_absolute["totale_dosi_consegnate"]
            new_italy_absolute["totale_vaccinati"] = new_italy_absolute.get("totale_vaccinati", 0) + new_absolute["totale_vaccinati"]
            # add dict to data
            new_data["assoluti"].append(new_absolute)

            new_variation = {}
            new_variation["codice_territorio"] = territory_data["codice"]
            new_variation["nome_territorio"] = territory_data["nome"]
            new_variation["nome_territorio_corto"] = territory_data["nome_corto"]

            # calculate variations
            if yesterday_data:
                yesterday_absolute = [x for x in yesterday_data["assoluti"] if x["codice_territorio"] == territory_data["codice"]][0]
                new_variation["nuovi_vaccinati"] = new_absolute["totale_vaccinati"] - yesterday_absolute["totale_vaccinati"]
                new_variation["percentuale_nuovi_vaccinati"] = new_variation["nuovi_vaccinati"] / yesterday_absolute["totale_vaccinati"] * 100
            else:
                yesterday_absolute = None
                new_variation["nuovi_vaccinati"] = 0
                new_variation["percentuale_nuovi_vaccinati"] = 0

            new_variation["nuovi_vaccinati_formattato"] = f'{new_variation["nuovi_vaccinati"]:n}'
            new_variation["percentuale_nuovi_vaccinati_formattato"] = f'{locale.format_string("%.2f", new_variation["percentuale_nuovi_vaccinati"])}%'

            # should be tied to self._deliveries, not self._history
            # BUT there isn't always data for yesterday deliveries
            territory_delivery = [x for x in today_deliveries if x["area"] == territory["area"]]
            if len(territory_delivery) == 0:
                territory_delivery = {}
            else:
                territory_delivery = territory_delivery[0]

            new_variation["nuove_dosi_consegnate"] = territory_delivery.get("nuove_dosi_consegnate", 0)
            new_variation["nuove_dosi_consegnate_formattato"] = f'{new_variation["nuove_dosi_consegnate"]:n}'
            if yesterday_absolute:
                new_variation["percentuale_nuove_dosi_consegnate"] = new_variation["nuove_dosi_consegnate"] / yesterday_absolute["totale_dosi_consegnate"] * 100
            else:
                new_variation["percentuale_nuove_dosi_consegnate"] = 0
            new_variation["percentuale_nuove_dosi_consegnate_formattato"] = f'{locale.format_string("%.2f", new_variation["percentuale_nuove_dosi_consegnate"])}%'

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
        new_italy_absolute["percentuale_dosi_utilizzate_formattato"] = f'{locale.format_string("%.2f", new_italy_absolute["percentuale_dosi_utilizzate"])}%'
        new_italy_absolute["percentuale_popolazione_vaccinata_formattato"] = f'{locale.format_string("%.2f", new_italy_absolute["percentuale_popolazione_vaccinata"])}%'
        new_italy_variation["nuovi_vaccinati_formattato"] = f'{new_italy_variation["nuovi_vaccinati"]:n}'
        new_italy_variation["nuove_dosi_consegnate_formattato"] =  f'{new_italy_variation["nuove_dosi_consegnate"]:n}'

        self._italy.update(new_italy_absolute)
        self._italy.update(new_italy_variation)

        # load categories and age ranges data
        response = requests.get(self._urls["anagrafica-vaccini"]).text
        json_response = ujson.loads(response)
        # load data for yesterday
        if yesterday_data:
            yesterday_absolute = [x for x in yesterday_data["assoluti"] if x["codice_territorio"] == "00"]
            if len(yesterday_absolute) > 0:
                yesterday_absolute = yesterday_absolute[0]
            else:
                yesterday_absolute = None
        else:
            yesterday_absolute = None

        # load all unique categories
        categories_list = [x for x in json_response["data"][0] if "categoria" in x]
        categories = []
        count = 0
        # append to the list the newly created categories
        for c in categories_list:
            new_dict = {
                "id": count,
                "nome_categoria": c,
                "nome_categoria_pulito": c.replace("categoria_", "").replace("over80", "over_80"), # this is needed later
                "nome_categoria_formattato": c.replace("categoria_", "").replace("over80", "over_80").replace("_", " "), # this is needed for the chart
                "totale_vaccinati": 0,
                "totale_vaccinati_formattato": "0"
            }
            categories.append(new_dict)
            count += 1

        # initialize genders and subministrations dicts
        genders = [{"nome_categoria": "uomini", "totale_vaccinati": 0}, {"nome_categoria": "donne", "totale_vaccinati": 0}]
        subministrations = [{"nome_categoria": "prima_dose", "totale_vaccinati": 0}, {"nome_categoria": "seconda_dose", "totale_vaccinati": 0}]

        # now load ages
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

            # data for category and genders is packed inside the ages
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

        # now calculate new vaccinated and format everything
        for category in categories:
            category["totale_vaccinati_formattato"] = f'{category["totale_vaccinati"]:n}'
            if yesterday_absolute:
                category["nuovi_vaccinati"] = category["totale_vaccinati"] - yesterday_absolute["categoria"][category["nome_categoria_pulito"]]
                category["nuovi_vaccinati_percentuale"] = category["nuovi_vaccinati"] / yesterday_absolute["categoria"][category["nome_categoria_pulito"]] * 100
            else:
                category["nuovi_vaccinati"] = 0
                category["nuovi_vaccinati_percentuale"] = 0

            category["nuovi_vaccinati_formattato"] = f'{category["nuovi_vaccinati"]:n}'
            category["nuovi_vaccinati_percentuale_formattato"] = f'{locale.format_string("%.2f", category["nuovi_vaccinati_percentuale"])}%'
            new_data["categorie"].append(category)

        for gender in genders:
            gender["totale_vaccinati_formattato"] = f'{gender["totale_vaccinati"]:n}'
            if yesterday_absolute:
                gender["nuovi_vaccinati"] = gender["totale_vaccinati"] - yesterday_absolute["sesso"][gender["nome_categoria"]]
                gender["nuovi_vaccinati_percentuale"] = gender["nuovi_vaccinati"] / yesterday_absolute["sesso"][gender["nome_categoria"]] * 100
            else:
                gender["nuovi_vaccinati"] = 0
                gender["nuovi_vaccinati_percentuale"] = 0

            gender["nuovi_vaccinati_formattato"] = f'{gender["nuovi_vaccinati"]:n}'
            gender["nuovi_vaccinati_percentuale_formattato"] = f'{locale.format_string("%.2f", gender["nuovi_vaccinati_percentuale"])}%'
            new_data["sesso"].append(gender)

        for subministration in subministrations:
            subministration["totale_vaccinati_formattato"] = f'{subministration["totale_vaccinati"]:n}'
            new_data["somministrazioni"].append(subministration)

        # update data about italy
        self._italy["somministrazioni"] = {
            "prima_dose": subministrations[0]["totale_vaccinati"],
            "prima_dose_formattato": subministrations[0]["totale_vaccinati_formattato"],
            "seconda_dose": subministrations[1]["totale_vaccinati"],
            "seconda_dose_formattato": subministrations[1]["totale_vaccinati_formattato"]
        }

        self._data = copy.deepcopy(new_data)

        # now create the new geoJson file
        with open("src/settings/regioni.geojson", "r") as f:
            geojson_data = ujson.load(f)

        for feature in geojson_data["features"]:
            for a in new_data["assoluti"]:
                if feature["properties"]["codice_regione"] == a["codice_territorio"]:
                    feature["properties"]["percentuale_popolazione_vaccinata"] = a["percentuale_popolazione_vaccinata"]
                    feature["properties"]["percentuale_popolazione_vaccinata_formattato"] = a["percentuale_popolazione_vaccinata_formattato"]
                    feature["properties"]["tinta"] = a["percentuale_popolazione_vaccinata"] / 100 * 120
                    break

        self._geojeson_percentages = copy.deepcopy(geojson_data)

    def scrapeColors(self):
        new_territories_colors = {
            "timestamp": datetime.now().isoformat(),
            "ultimo_aggiornamento": datetime.now().strftime("%Y-%m-%d ore %H:%M"),
            "territori": []
        }

        logging.info("Loading colors")
        # initialize old data
        response = requests.get(self._urls["colore-territori"]).text
        soup = BeautifulSoup(response, 'html.parser')

        # small settings dict
        # now data is loaded dynamically (BUT ONLY THE REGIONS COLORS, NOT THE
        # REGION LIST!) by a DUMB SCRIPT WITH A CLEAR DESCRIPTIVE NAME
        # MINISTERO, IF YOU WANTED TO KEEP THIS SECRET, YOU COULD HAVE FOUND
        # A BETTER WAY TO DO SO!
        colors = {
            "document.write(areaRossa)": {
                "nome": "Rossa",
                "rgb": "#dd222a"
            },
            "document.write(areaArancione)": {
                "nome": "Arancione",
                "rgb": "#e78314"
            },
            "document.write(areaGialla)": {
                "nome": "Gialla",
                "rgb": "#f8c300"
            },
            "document.write(areaBianca)": {
                "nome": "Bianca",
                "rgb": "#f7f7f7"
            }
        }

        logging.info("Scraping colors")
        # save geoJson related to territories color
        count = 0
        for c in colors:
            # find the element and get its text
            territories = soup.body.find(text=lambda t: c in t).next.get_text(strip=True, separator="\n")

            for t in territories.split("\n"):
                # sometimes the line is empty
                if not t:
                    continue

                # replace the acronym
                t = t.replace("PA", "P.A.")
                # create the new dict
                new_territories_colors["territori"].append({
                    "territorio": t,
                    "codice_territorio": self.returnTerritoryCode(t),
                    "colore": colors[c]["nome"],
                    "colore_rgb": colors[c]["rgb"],
                    "codice_colore": count
                })

            count += 1

        with open("src/settings/regioni.geojson", "r") as f:
            geojson_data = ujson.load(f)

        # save geoJson related to vaccination color
        for feature in geojson_data["features"]:
            for t in new_territories_colors["territori"]:
                if feature["properties"]["codice_regione"] == t["codice_territorio"]:
                    feature["properties"]["colore"] = t["colore"]
                    feature["properties"]["colore_rgb"] = t["colore_rgb"]
                    break

        # finally, copy inside the private variables
        self._territories_color = copy.deepcopy(new_territories_colors)
        self._geojson_colors = copy.deepcopy(geojson_data)

    def scrapeAll(self):
        self.scrapeHistory()
        self.scrapeData()
        self.scrapeColors()

    def printJson(self, data, indent=2, exit=True):
        print(ujson.dumps(data, indent=indent))
        if exit:
            quit()

    def backup(self):
        logging.info("Started backup process")
        # now push all to to github
        # repo folder is parent
        subprocess.run(["git", "pull"])
        logging.info("Repo pulled")
        try:
            subprocess.run(["git", "add", "-A"])
            subprocess.run(["git", "commit", "-m", "updated data"])
            logging.info("Commit created")
            subprocess.run(["git", "push"])
            logging.info("Repo pushed")
        except Exception as e:
            logging.error("Cannot commit or push. Repo is probably already "
                          f"on par with the tree. Error {e}")

    # getter methods
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
    def territories_color_map(self):
        self.loadData(colors_geojson=True)
        return self._geojson_colors

    @property
    def territories_percentage_map(self):
        self.loadData(percentage_geojson=True)
        return self._geojeson_percentages

    @property
    def vaccine_producers(self):
        self.loadData(today=True)
        return self._data["produttori_vaccini"]

    @property
    def subministrations(self):
        self.loadData(today=True)
        return self._data["somministrazioni"]


if __name__ == "__main__":
    s = Scraper()
    started = datetime.now()
    s.scrapeAll()
    s.saveData()
    elapsed = (datetime.now() - started).total_seconds()
    logging.info(f"It took {elapsed} seconds")
