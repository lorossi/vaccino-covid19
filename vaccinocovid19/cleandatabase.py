# IMPORTANT
# run this before starting the server
# this script is useful to "clean" the "database" and to allow the migration
# to the new flask based website.
# the fields inside the json file have changed so we need to convert all the
# old gathered data. This needs to be done only once, before starting the
# server for the first time

import os
import json
from scraper import Scraper
import requests
from datetime import datetime


def download(output_path="src/output/", output_filename="vaccini.json", url="https://raw.githubusercontent.com/lorossi/vaccino-covid19/master/python_scripts/output/vaccini.json"):
    r = requests.get(url, allow_redirects=True)
    with open(output_path + output_filename, "w") as f:
        f.write(r.text)


def clean():
    cwd = os.getcwd() + "/"
    json_filename = "vaccini.json"
    json_output_filename = "vaccini.json"
    output_path = "src/output/"
    settings_path = "src/settings/"

    with open(cwd + output_path + json_filename, "r") as f:
        old_data = json.load(f)

    with open(cwd + settings_path + "popolazione_regione.json") as f:
        territories_population = json.load(f)

    old_data.sort(key=lambda x: datetime.fromisoformat(x['script_timestamp']), reverse=True)

    cleaned_data = []
    first_in_day = None
    last_timestamp = []
    for d in old_data:
        time_obj = datetime.fromisoformat(d["script_timestamp"])

        if not last_timestamp:
            last_timestamp.append(time_obj)
        else:
            if time_obj.date() != last_timestamp[-1].date():
                last_timestamp.append(time_obj)


    for t in last_timestamp:
        for d in old_data:
            if t == datetime.fromisoformat(d["script_timestamp"]):
                cleaned_data.append(d)
                break

    for x in range(len(cleaned_data)):
        new_territories = {
            "assoluti": [],
            "variazioni": []
        }

        for y in range(len(cleaned_data[x]["territori"])):
            territory_name = cleaned_data[x]["territori"][y]["nome_territorio"]
            territory_code = cleaned_data[x]["territori"][y].get("codice_territorio")
            if not territory_code:
                territory_code = "00"
            population = territories_population[territory_code]

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

            new_absolute = {
                "nome_territorio": territory_name,
                "nome_territorio_corto": short_name,
                "codice_territorio": territory_code,
                "totale_vaccinati": cleaned_data[x]["territori"][y]["totale_vaccinati"],
                "percentuale_popolazione_vaccinata": cleaned_data[x]["territori"][y]["totale_vaccinati"] / population * 100,
                "totale_dosi_consegnate": cleaned_data[x]["territori"][y]["totale_dosi_consegnate"],
                "percentuale_dosi_utilizzate": cleaned_data[x]["territori"][y]["totale_vaccinati"] / cleaned_data[x]["territori"][y]["totale_dosi_consegnate"] * 100
            }

            if x < len(old_data) - 1:
                new_variations = {
                    "nome_territorio": territory_name,
                    "nome_territorio_corto": short_name,
                    "codice_territorio": territory_code,
                    "nuovi_vaccinati": cleaned_data[x]["territori"][y]["nuovi_vaccinati"],
                    "percentuale_nuovi_vaccinati": cleaned_data[x]["territori"][y]["nuovi_vaccinati"] / cleaned_data[x+1]["territori"][y]["totale_vaccinati"] * 100,
                    "nuove_dosi_consegnate": cleaned_data[x]["territori"][y]["totale_dosi_consegnate"] - cleaned_data[x+1]["territori"][y]["totale_dosi_consegnate"],
                    "percentuale_nuove_dosi_consegnate": (cleaned_data[x]["territori"][y]["totale_dosi_consegnate"] - cleaned_data[x+1]["territori"][y]["totale_dosi_consegnate"]) / cleaned_data[x+1]["territori"][y]["totale_dosi_consegnate"] * 100
                }

            new_territories["assoluti"].append(new_absolute)

            if new_variations:
                new_territories["variazioni"].append(new_variations)

        for y in range(len(cleaned_data[x]["fasce_eta"])):
            cleaned_data[x]["fasce_eta"][y]["nome_categoria"] = cleaned_data[x]["fasce_eta"][y]["nome_categoria"].replace("<=", "0-")

        cleaned_data[x].update(new_territories)

    for x in range(len(cleaned_data)):
        del cleaned_data[x]["territori"]


    with open(cwd + output_path + json_output_filename, "w") as f:
        json.dump(cleaned_data, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    download()
    s = Scraper()

    try:
        clean()
        print("database cleaned")
    except Exception as e:
        print(f"database already clean. Error {e}")

    s.scrape_data()
    s.scrape_history()
    s.save_data()
    print("data scraped")
    print("now start flask")
