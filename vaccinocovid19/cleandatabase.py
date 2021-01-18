from scraper import Scraper
import requests
from pathlib import Path


def download(output_path="src/output/"):
    Path(output_path).mkdir(parents=True, exist_ok=True)

    url = "https://raw.githubusercontent.com/lorossi/vaccino-covid19/master/vaccinocovid19/src/output/vaccini.json"
    r = requests.get(url, allow_redirects=True)
    with open(output_path + "vaccini.json", "w") as f:
        f.write(r.text)

    url = "https://raw.githubusercontent.com/lorossi/vaccino-covid19/master/vaccinocovid19/src/output/storico-vaccini.json"
    r = requests.get(url, allow_redirects=True)
    with open(output_path + "storico-vaccini.json", "w") as f:
        f.write(r.text)

if __name__ == "__main__":
    download()

    s = Scraper()
    s.scrapeData()
    s.scrapeHistory()
    s.scrapeTerritoriesColor()
    s.saveData()
