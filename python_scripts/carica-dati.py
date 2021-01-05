import requests
import json
from datetime import datetime
import logging
from pathlib import Path
import os
import subprocess


def main():
    json_filename = "vaccini.json"
    js_filename = "vaccini.js"
    output_path = "output/"
    assets_path = "../docs/assets/"

    popolazione_italia = 60317000
    data = {"territori": []}
    italia = {"nome_territorio": "Italia"}

    data["script_timestamp"] = datetime.now().isoformat()
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # current working directory
    cwd = os.getcwd() + "/"

    logging.info("Loading settings")

    with open("settings/headers.json") as f:
        headers = json.load(f)

    with open("settings/payloads.json", "r") as f:
        payload = json.load(f)

    with open("settings/codici_regione.json", "r") as f:
        codici = json.load(f)

    logging.info("Requesting data")
    response = requests.post(payload["url"], headers=headers,
                             data=payload["totale_vaccini"]).text

    json_response = json.loads(response)
    logging.info("Data requested")

    logging.info("Loading old data")
    try:
        print(json_filename)
        with open(json_filename, "r") as f:
            old_data = json.load(f)
            old_data.sort(key=lambda x: datetime.fromisoformat(x['script_timestamp']), reverse=False)
            today = datetime.now().day
            for x in range(len(old_data)):
                old_timestamp = datetime.fromisoformat(old_data[x]['script_timestamp'])
                if today != old_timestamp.day:
                    last_data = old_data[x]

    except Exception as e:
        last_data = None
        logging.info(f"No previous record. Unable to calculate variation. Error: {e}")

    logging.info("Scraping data")
    data["last_data_update"] = json_response["results"][0]["result"]["data"]["timestamp"]
    for territorio in json_response["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]:
        nome_territorio = territorio["C"][0].replace("P.A.", "").replace("-", " ").strip().upper()
        codice_territorio = None

        for c in codici:
            if codici[c] == nome_territorio:
                codice_territorio = c
                break

        new_data = {
            "nome_territorio": territorio["C"][0],
            "codice_territorio": codice_territorio,
            "totale_dosi_consegnate": territorio["C"][3],
            "totale_vaccinati": territorio["C"][1],
            "percentuale_popolazione_vaccinata": territorio["C"][2]
        }

        last_territorio = None
        if last_data is not None:
            for old_territorio in last_data["territori"]:
                if old_territorio["nome_territorio"] == new_data["nome_territorio"]:
                    last_territorio = territorio["C"]

        if last_territorio is not None:
            new_data["nuove_dosi_consegnate"] = new_data["totale_dosi_consegnate"] - last_territorio[3]
            new_data["nuovi_vaccinati"] = new_data["totale_vaccinati"] - last_territorio[1]
        data["territori"].append(new_data)

        if "totale_dosi_consegnate" not in italia:
            italia["totale_dosi_consegnate"] = territorio["C"][3]
            italia["totale_vaccinati"] = territorio["C"][1]
        else:
            italia["totale_dosi_consegnate"] += territorio["C"][3]
            italia["totale_vaccinati"] += territorio["C"][1]

    italia["percentuale_popolazione_vaccinata"] = italia["totale_vaccinati"] / popolazione_italia * 100

    last_italia = None
    if last_data is not None:
        for territorio in last_data["territori"]:
            if territorio["nome_territorio"] == "Italia":
                last_italia = territorio

    if last_italia is not None:
        italia["nuove_dosi_consegnate"] = italia["totale_dosi_consegnate"] - last_italia["totale_dosi_consegnate"]
        italia["nuovi_vaccinati"] = italia["totale_vaccinati"] - last_italia["totale_vaccinati"]

    data["territori"].append(italia)
    logging.info("Data scraped")

    logging.info("Creating folders")
    Path(output_path).mkdir(parents=True, exist_ok=True)
    Path(assets_path).mkdir(parents=True, exist_ok=True)

    logging.info("Saving to file")
    try:
        with open(output_path + json_filename, "r") as f:
            old_data = json.load(f)
            old_data.append(data)
            old_data.sort(key=lambda x: datetime.fromisoformat(x['script_timestamp']), reverse=True)
    except Exception as e:
        logging.error(f"Error while opening dest file. Error: {e}")
        logging.error("Creating new file.")
        old_data = [data]

    with open(output_path + json_filename, "w") as f:
        json.dump(old_data, f, indent=3)
    logging.info(f"Json file saved. Path: {cwd}{json_filename}")

    with open(output_path + js_filename, "w") as f:
        js_string = "let vaccini = "
        # convert dict to json (will be read by js)
        js_string += json.dumps(data, indent=4)
        js_string += ";"
        f.write(js_string)
    logging.info(f"JS file saved. Path: {cwd}{js_filename}")

    with open(assets_path + js_filename, "w") as f:
        js_string = "let vaccini = "
        # convert dict to json (will be read by js)
        js_string += json.dumps(data, indent=4)
        js_string += ";"
        f.write(js_string)

    return
    logging.info("Pushing to GitHub")
    subprocess.run("git pull".split(" "))
    subprocess.run(["git", "add", cwd + output_path + json_filename])
    subprocess.run(["git", "add", cwd + output_path + js_filename])
    subprocess.run(["git", "add", cwd + assets_path + js_filename])
    subprocess.run(["git", "pull"])
    subprocess.run(["git", "commit", "-m", "\"updated data\""])
    subprocess.run(["git", "push"])
    logging.info("Pushed to GitHub")


if __name__ == "__main__":
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="a")
    print(f"Logging in {logfile}")

    logging.info("Script started")
    main()
    logging.info("Script ended")
