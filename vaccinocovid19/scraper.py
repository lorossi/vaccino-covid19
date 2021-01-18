# Made by Lorenzo Rossi
# https://www.lorenzoros.si - https://github.com/lorossi

import copy
import ujson
import logging
import requests
import subprocess
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime


class Scraper:
    def __init__(self, log=True, verbose=True):

        self.log = log
        self.verbose = verbose
        self._data = []
        self._new_data = []
        self._history = []
        self._new_history = []
        self._italy = {}
        self._territories = []
        self._today = []
        self._territory_colors = {}
        self._last_updated = None
        self._territories_codes = None

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

        self.json_filename = settings["json_filename"]
        self.output_path = settings["output_path"]
        self.history_filename = settings["history_filename"]
        self.today_filename = settings["today_filename"]
        self.italy_filename = settings["italy_filename"]
        self.colors_filename = settings["colors_filename"]
        self.colors_url = settings["colors_url"]

    def scrapeData(self):
        # initialize dictionaries
        self._new_data = {
            "assoluti": [],
            "variazioni": [],
            "categorie": [],
            "sesso": [],
            "fasce_eta": [],
            "lista_territori": [
                    "Italia"
                ]
            }

        italy_absolute = {
            "nome_territorio": "Italia",
            "nome_territorio_corto": "Italia",
            "codice_territorio": "00"
            }

        italy_variation = copy.deepcopy(italy_absolute)

        # load timestamp that will be put inside the output
        now = datetime.now()
        self._new_data["script_timestamp"] = now.isoformat()
        self._new_data["last_updated"] = now.strftime("%Y-%m-%d ore %H:%M")

        logging.info("Loading settings")
        # load headers
        with open("src/settings/headers.json") as f:
            headers = ujson.load(f)

        # load payload and url
        with open("src/settings/payloads.json", "r") as f:
            payload = ujson.load(f)

        # load territories population
        with open("src/settings/popolazione_regione.json", "r") as f:
            territories_population = ujson.load(f)

        logging.info("Loading old data")
        last_data = None
        try:
            # try to load old data to make a comparision
            with open(self.output_path + self.json_filename, "r") as f:
                old_data = ujson.load(f)
                # sort old data so the newest one is the first
                old_data.sort(key=lambda x:
                              datetime.fromisoformat(x['script_timestamp']),
                              reverse=True)
                # get last midnight
                midnight = datetime.now().replace(hour=0, minute=0, second=0)
                # now start iterating until we find data from yesterday (if any)
                for x in range(len(old_data)):
                    old_timestamp = datetime.fromisoformat(
                                    old_data[x]["script_timestamp"])

                    if midnight > old_timestamp:
                        # found the most recent data for the prior day
                        last_data = old_data[x]
                        logging.info("Loaded data for previous day with timestamp "
                                     f"{old_timestamp}")
                        break

        except Exception as e:
            # no old previuos file has been found
            logging.info("No previous record. Unable to calculate variation. "
                         f"Error: {e}")

        logging.info("Requesting data about territories")
        response = requests.post(payload["url"], headers=headers,
                                 data=payload["totale_vaccini"]).text
        json_response = ujson.loads(response)

        # load data from the response
        last_update = json_response["results"][0]["result"]["data"]["timestamp"]
        self._new_data["last_data_update"] = last_update
        # iterate over each territory
        territories = json_response["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]

        for territory in territories:
            # format territory name to later match the code
            territory_name = territory["C"][0]
            territory_code = self.findTerritoryCode(territory_name)

            # preloading
            # data for percentage of vaccinated people is wrong.
            # oh well, who could have guessed?
            total_vaccinated = territory["C"][1]
            total_population = territories_population[territory_code]
            percent_vaccinated = total_vaccinated / total_population * 100
            total_doses = territory["C"][3]
            percent_used_doses = total_vaccinated / total_doses * 100

            if territory_code == "06":
                short_name = "E.R."
            elif territory_code == "07":
                short_name = "F.V.G"
            elif territory_code == "20":
                short_name = "V. d'Aosta"
            elif territory_code == "03":
                short_name = "Bolzano"
            elif territory_code == "18":
                short_name = "Trento"
            elif territory_code is None:
                short_name = "Italy"
            else:
                short_name = territory_name

            # populate the dict with all the new data
            new_absolute = {
                "nome_territorio": territory_name,
                "nome_territorio_corto": short_name,
                "codice_territorio": territory_code,
                "totale_vaccinati": total_vaccinated,
                "percentuale_popolazione_vaccinata": percent_vaccinated,
                "totale_dosi_consegnate": total_doses,
                "percentuale_dosi_utilizzate": percent_used_doses
            }

            new_variation = None

            # find the absolute data for yesterday
            last_territory = None
            if last_data is not None:
                for old_territory in last_data["assoluti"]:
                    if old_territory["nome_territorio"] == new_absolute["nome_territorio"]:
                        last_territory = old_territory
                        break

            # if found, compare
            if last_territory is not None:
                nuovi_vaccinati = new_absolute["totale_vaccinati"] - last_territory["totale_vaccinati"]
                nuovi_vaccini = new_absolute["totale_dosi_consegnate"] - last_territory["totale_dosi_consegnate"]

                new_variation = {
                    "nome_territorio": new_absolute["nome_territorio"],
                    "nome_territorio_corto": short_name,
                    "codice_territorio": new_absolute["codice_territorio"],
                    "nuovi_vaccinati": nuovi_vaccinati,
                    "percentuale_nuovi_vaccinati": nuovi_vaccinati / last_territory["totale_vaccinati"] * 100,
                    "nuove_dosi_consegnate": nuovi_vaccini,
                    "percentuale_nuove_dosi_consegnate": nuovi_vaccini / last_territory["totale_dosi_consegnate"] * 100
                }

            # finally append data to the dict
            self._new_data["assoluti"].append(new_absolute)
            if new_variation:
                self._new_data["variazioni"].append(new_variation)
            if territory_code:
                self._new_data["lista_territori"].append(territory_name)

            # update total number of doses and vaccinated people
            if "totale_dosi_consegnate" not in italy_absolute:
                italy_absolute["totale_dosi_consegnate"] = territory["C"][3]
                italy_absolute["totale_vaccinati"] = territory["C"][1]
            else:
                italy_absolute["totale_dosi_consegnate"] += territory["C"][3]
                italy_absolute["totale_vaccinati"] += territory["C"][1]

        # calculate the percentage of vaccinated people
        population_percentage = italy_absolute["totale_vaccinati"] / territories_population["00"] * 100
        italy_absolute["percentuale_popolazione_vaccinata"] = population_percentage
        italy_absolute["percentuale_popolazione_vaccinata_formattata"] = format(population_percentage, ".2f")
        used_percentage = italy_absolute["totale_vaccinati"] / italy_absolute["totale_dosi_consegnate"] * 100
        italy_absolute["percentuale_dosi_utilizzate"] = used_percentage
        italy_absolute["percentuale_dosi_utilizzate_formattata"] = format(used_percentage, ".2f")

        # now look for old data about italy as whole
        last_italy = None
        if last_data is not None:
            for territory in last_data["assoluti"]:
                if territory["nome_territorio"] == "Italia":
                    last_italy = territory

        # if found, update the variation
        if last_italy is not None:
            italy_variation["nuove_dosi_consegnate"] = italy_absolute["totale_dosi_consegnate"] - last_italy["totale_dosi_consegnate"]
            italy_variation["nuovi_vaccinati"] = italy_absolute["totale_vaccinati"] - last_italy["totale_vaccinati"]

        # finally, append to dict the data about italy
        self._new_data["assoluti"].append(italy_absolute)
        # only if anything else has been found, update the variation
        if len(self._new_data["variazioni"]) > 0:
            self._new_data["variazioni"].append(italy_variation)
        else:
            del self._new_data["variazioni"]

        # now load categories
        logging.info("Requesting data about categories")
        response = requests.post(payload["url"], headers=headers,
                                 data=payload["categorie"]).text
        json_response = ujson.loads(response)

        categories = json_response["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
        for category in categories:
            category_id = int(category["C"][0][0])
            category_name = category["C"][0][4:]
            total_number = category["C"][1]

            # init the dict with all the new data
            new_data = {
                "id_categoria": category_id,
                "nome_categoria": category_name,
                "totale_vaccinati": total_number,
            }

            # iterate over last data to find the variation
            if last_data is not None:
                for category in last_data["categorie"]:
                    if category["nome_categoria"] == category_name:
                        if "totale_vaccinati" in category:
                            # add variation from yesterday
                            variation = total_number - category["totale_vaccinati"]
                            new_data["nuovi_vaccinati"] = variation
                            new_data["percentuale_nuovi_vaccinati"] = variation / total_number * 100
                            break

            # finally append data to the dict
            self._new_data["categorie"].append(new_data)

        # now load women
        logging.info("Requesting data about women")
        response = requests.post(payload["url"], headers=headers, data=payload["donne"]).text
        json_response = ujson.loads(response)

        women = json_response["results"][0]["result"]["data"]["dsr"]["DS"][0] \
                             ["PH"][0]["DM0"][0]["M0"]

        new_dict = {
            "nome_categoria": "donne",
            "totale_vaccinati": women
        }

        if last_data is not None:
            for gender in last_data["sesso"]:
                if gender["nome_categoria"] == "donne":
                    if "totale_vaccinati" in gender:
                        # calculate variation
                        variation = women - gender["totale_vaccinati"]
                        new_dict["nuovi_vaccinati"] = variation
                        new_dict["percentuale_nuovi_vaccinati"] = variation / women * 100

        # finally append to data
        self._new_data["sesso"].append(new_dict)

        # now load men
        logging.info("Requesting data about men")
        response = requests.post(payload["url"], headers=headers, data=payload["uomini"]).text
        json_response = ujson.loads(response)

        men = json_response["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"] \
                           [0]["DM0"][0]["M0"]
        new_dict = {
            "nome_categoria": "uomini",
            "totale_vaccinati": men
        }

        if last_data is not None:
            for gender in last_data["sesso"]:
                if gender["nome_categoria"] == "uomini":
                    if "totale_vaccinati" in gender:
                        # calculate variation
                        variation = men - gender["totale_vaccinati"]
                        new_dict["nuovi_vaccinati"] = variation
                        new_dict["percentuale_nuovi_vaccinati"] = variation / men * 100

        # finally append to data
        self._new_data["sesso"].append(new_dict)

        # now load age ranges
        logging.info("Requesting data about age ranges")
        response = requests.post(payload["url"], headers=headers,
                                 data=payload["eta"]).text
        json_response = ujson.loads(response)

        for age_range in json_response["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]:
            if len(age_range["C"]) < 2:
                continue
            category_name = age_range["C"][0]
            total_number = age_range["C"][1]

            # init the dict with all the new data
            new_data = {
                "nome_categoria": category_name.replace("<=", "0-"),
                "totale_vaccinati": total_number,
            }

            # iterate over last data to find the variation
            if last_data is not None:
                for age in last_data["fasce_eta"]:
                    if age["nome_categoria"] == category_name:
                        if "totale_vaccinati" in age:
                            variation = total_number - age["totale_vaccinati"]
                            new_data["nuovi_vaccinati"] = variation
                            new_data["percentuale_nuovi_vaccinati"] = variation / total_number * 100
                            break

            # finally append data to the dict
            self._new_data["fasce_eta"].append(new_data)

        try:
            # load old data to update the file
            with open(self.output_path + self.json_filename, "r") as f:
                old_data = ujson.load(f)
                # sort by time so new data is always on top
                old_data.sort(key=lambda x:
                              datetime.fromisoformat(x['script_timestamp']),
                              reverse=True)
        except Exception as e:
            logging.error(f"Error while opening dest file. Error: {e}")
            # no old data has been found.
            # the new data must be encapsulated in a list before dumping it into
            # a json file
            old_data = [self._new_data]

        # loop trhought old data in order to update the dictionary
        found = False
        current_timestamp = datetime.fromisoformat(self._new_data["script_timestamp"])
        for d in old_data:
            old_timestamp = datetime.fromisoformat(d["script_timestamp"])
            if current_timestamp.date() == old_timestamp.date():
                # update dictionary
                found = True
                # this won't work, not running python 3.9 currently :(
                # d |= data
                d.update(self._new_data)
                # log info
                logging.info("Data for today already found with timestamp: "
                             f"{old_timestamp}")
                break

        if not found:
            old_data.append(self._new_data)
            logging.info("No old data found for today. Appending.")
        logging.info("Data scraped")

        self._new_data = old_data
        # save data, territories and italy in separated private lists
        self._data = copy.deepcopy(self._new_data)
        self.filterData()

    def scrapeHistory(self):
        # create a js file with all the data about vaccines
        # midnight for the considered day
        midnight = datetime.now().replace(hour=0, minute=0,
                                          second=0, microsecond=0)
        # last midnight from now
        last_midnight = datetime.now().replace(hour=0, minute=0,
                                               second=0, microsecond=0)
        self._new_history = []

        for d in self._new_data:
            new_data = {}
            timestamp = d["script_timestamp"]
            time_obj = datetime.fromisoformat(timestamp)
            # the data we are looking for is older than last midnght and closest
            # to midnight (rolling)
            since_midnight = (midnight - time_obj).total_seconds()
            since_last_midnight = (last_midnight - time_obj).total_seconds()
            if since_midnight >= 0 and since_last_midnight >= 0:
                new_timestamp = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d")
                new_data["script_timestamp"] = new_timestamp
                new_data["assoluti"] = []
                new_data["variazioni"] = []

                for absolute in d["assoluti"]:
                    new_absolute = {
                        "nome_territorio": absolute["nome_territorio"],
                        "codice_territorio": absolute.get("codice_territorio", "00"),
                        "totale_vaccinati": absolute["totale_vaccinati"],
                        "percentuale_popolazione_vaccinata": absolute["percentuale_popolazione_vaccinata"],
                        "totale_dosi_consegnate": absolute["totale_dosi_consegnate"],
                        "percentuale_dosi_utilizzate": absolute["percentuale_dosi_utilizzate"]
                    }

                    new_data["assoluti"].append(new_absolute)

                if "variazioni" in d:
                    for variation in d["variazioni"]:
                        # some data, including old variation, might not be yet available
                        new_variation = {
                            "nome_territorio": variation["nome_territorio"],
                            "codice_territorio": variation.get("codice_territorio", "00"),
                            "nuovi_vaccinati": variation["nuovi_vaccinati"],
                            "percentuale_nuovi_vaccinati": variation.get("percentuale_nuovi_vaccinati", 0),
                            "nuove_dosi_consegnate": variation.get("nuove_dosi_consegnate", 0),
                            "percentuale_nuove_dosi_consegnate": variation.get("percentuale_nuove_dosi_consegnate", 0)
                        }

                    new_data["variazioni"].append(new_variation)

                self._new_history.append(new_data)
                midnight = time_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        # reverse so the oldest one ore always on top
        self._new_history.reverse()

        if len(self._new_history) > 0:
            self._history = copy.deepcopy(self._new_history)
        else:
            self._history = []

    def scrapeTerritoriesColor(self):
        colors = [
            {
                "color_name": "rossa",
                "color_code": 0
            },
            {
                "color_name": "arancione",
                "color_code": 1
            },
            {
                "color_name": "gialla",
                "color_code": 2
            },
            {
                "color_name": "bianca",
                "color_code": 3
            }
        ]

        to_remove = [":", ";", "."]
        self._territory_colors = {"territori": []}
        html = requests.get(self.colors_url).text
        soup = BeautifulSoup(html, 'html.parser')

        for c in colors:
            # get regions list
            div = soup.body.find(text=f"area {c['color_name']}")
            if not div:
                continue
            regions_text = div.next
            # start editing names
            for r in to_remove:
                regions_text = regions_text.replace(r, "")
            regions_text = regions_text.replace(u'\xa0', " ")  # spazio
            regions_text = regions_text.replace('\u2019', "'")  # apostrofo
            # dumb changes
            regions_text = regions_text.replace("Emilia Romagna", "Emilia-Romagna")
            regions_text = regions_text.replace("Friuli Venezia Giulia", "Friuli-Venezia Giulia")
            # non fanno differenza tra maiuscola e minuscola
            regions_text = regions_text.lower().replace("provincia autonoma di", "P.A.").title()
            regions_list = regions_text.strip().split(", ")
            regions_list.sort()

            for r in regions_list:
                territory_code = self.findTerritoryCode(r)
                new_dict = {
                    "nome_territorio": r,
                    "codice_territorio": int(territory_code),
                    "colore": c["color_name"],
                    "codice_colore": c["color_code"]
                }
                self._territory_colors["territori"].append(new_dict)

        self._territory_colors["script_timestamp"] = datetime.now().isoformat()

    def saveData(self):
        # create output folders
        logging.info("Creating folders")
        Path(self.output_path).mkdir(parents=True, exist_ok=True)

        if self._data:
            logging.info("Saving to file")
            # now finally save the json file
            with open(self.output_path + self.json_filename, "w") as f:
                ujson.dump(self._data, f, indent=2, sort_keys=True)
            logging.info(f"JSON file saved. Path: {self.json_filename}")

            with open(self.output_path + self.today_filename, "w") as f:
                ujson.dump(self._today, f, indent=2, sort_keys=True)
            logging.info(f"Today file saved. Path: {self.json_filename}")

            with open(self.output_path + self.italy_filename, "w") as f:
                ujson.dump(self._italy, f, indent=2, sort_keys=True)
            logging.info(f"Italy file saved. Path: {self.json_filename}")

        if self._history:
            with open(self.output_path + self.history_filename, "w") as f:
                # convert dict to json (will be read by js)
                f.write(ujson.dumps(self._history, indent=2, sort_keys=True))
            logging.info(f"JSON history file saved. Path: {self.history_filename}")


        if self._territory_colors:
            with open(self.output_path + self.colors_filename, "w") as f:
                # convert dict to json (will be read by js)
                f.write(ujson.dumps(self._territory_colors, indent=2, sort_keys=True))
            logging.info(f"JSON history file saved. Path: {self.colors_filename}")

    def loadData(self):
        try:
            with open(self.output_path + self.json_filename, "r") as f:
                self._new_data = ujson.load(f)
        except Exception as e:
            logging.error(f"Cannot read data file. error {e}")
            self._new_data = []

        try:
            with open(self.output_path + self.history_filename, "r") as f:
                self._new_history = ujson.load(f)
        except Exception as e:
            logging.error(f"Cannot read history file. error {e}")
            self._new_history = []

        try:
            with open(self.output_path + self.colors_filename, "r") as f:
                self._new_territory_colors = ujson.load(f)
        except Exception as e:
            logging.error(f"Cannot read colors file. error {e}")
            self._new_territory_colors = []

        self._data = copy.deepcopy(self._new_data)
        self._history = copy.deepcopy(self._new_history)
        self._territory_colors = copy.deepcopy(self._new_territory_colors)

        self.filterData()

    def filterData(self):
        self._today = self._data[0]
        self._last_updated = self._data[0]["last_updated"]

        self._absolute_territories = [t for t in self._data[0]["assoluti"] if t["nome_territorio"] != "Italia"]
        if "assoluti" in self._data[0]:
            self._variation_territories = [v for v in self._data[0]["variazioni"] if v["nome_territorio"] != "Italia"]

        self._italy = {}
        self._italy.update(next(t for t in self._data[0]["assoluti"] if t["nome_territorio"] == "Italia"))
        if "assoluti" in self._data[0]:
            self._italy.update(next(v for v in self._data[0]["variazioni"] if v["nome_territorio"] == "Italia"))

        self._italy["last_updated"] = self._last_updated

    def findTerritoryCode(self, territory_name):
        current_name = territory_name.replace("P.A.", "").replace("-", " ")
        current_name = current_name.strip().upper()
        # load territories ISTAT code
        if not self._territories_codes:
            with open("src/settings/codici_regione.json", "r") as f:
                self._territories_codes = ujson.load(f)

        for code in self._territories_codes:
            if self._territories_codes[code] == current_name:
                return code
        return None

    def pushToGitHub(self):
        # now push all to to github
        logging.info("Pushing to GitHub")
        subprocess.run(["git", "pull"], check=True, shell=True)
        subprocess.run(["git", "add", "-A"], check=True, shell=True)
        subprocess.run(["git", "commit", "-m", '"updated data"'], check=True, shell=True)
        subprocess.run(["git", "push"], check=True, shell=True)
        logging.info("Pushed to GitHub")

    @property
    def last_updated(self):
        with open(self.output_path + self.today_filename, "r") as f:
            self._last_updated = ujson.load(f)["last_updated"]
        return {
            "last_updated": self._last_updated
            }

    @property
    def italy(self):
        with open(self.output_path + self.italy_filename, "r") as f:
            self._italy = ujson.load(f)
            return self._italy

    @property
    def territories_list(self):
        with open(self.output_path + self.today_filename, "r") as f:
            self._today = ujson.load(f)
        return {
                "territori": self._today["lista_territori"]
            }

    @property
    def absolute_territories(self):
        with open(self.output_path + self.today_filename, "r") as f:
            self._absolute_territories = [t for t in ujson.load(f)["assoluti"] if t["nome_territorio"] != "Italia"]
            return self._absolute_territories

    @property
    def variation_territories(self):
        with open(self.output_path + self.today_filename, "r") as f:
            self._variation_territories = [t for t in ujson.load(f)["variazioni"] if t["nome_territorio"] != "Italia"]
            return self._variation_territories

    @property
    def categories(self):
        with open(self.output_path + self.today_filename, "r") as f:
            self._absolute_territories = ujson.load(f)["categorie"]
            return self._absolute_territories

    @property
    def genders(self):
        with open(self.output_path + self.today_filename, "r") as f:
            self._absolute_territories = ujson.load(f)["sesso"]
            return self._absolute_territories

    @property
    def age_ranges(self):
        with open(self.output_path + self.today_filename, "r") as f:
            self._absolute_territories = ujson.load(f)["fasce_eta"]
            return self._absolute_territories

    @property
    def history(self):
        with open(self.output_path + self.history_filename, "r") as f:
            self._history = ujson.load(f)
            return self._history

    @property
    def territory_colors(self):
        with open(self.output_path + self.colors_filename, "r") as f:
            self._territory_colors = ujson.load(f)
            return self._territory_colors


if __name__ == "__main__":
    s = Scraper()
    s.scrapeData()
    s.scrapeHistory()
    s.scrapeTerritoriesColor()
    s.saveData()
    # s.pushToGitHub()
