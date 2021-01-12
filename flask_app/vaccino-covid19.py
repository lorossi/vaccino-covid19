from flask import Flask, render_template, request, jsonify, session
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import scraper
import json

# GLOBAL VARIABLES
data = []
history = []


def load_settings(path="src/settings/settings.json"):
    with open(path, "r") as f:
        return json.load(f)


def scrape_data():
    global data, history
    data = scraper.scrape_data()
    history = scraper.load_history(data)


def load_data():
    global data, history
    data, history = scraper.load_data()


app = Flask(__name__)
# index
@app.route("/")
@app.route("/homepage")
def index():
    return render_template("index.html")


@app.route("/get/last_updated", methods=["GET"])
def get_last_updated():
    return_dict = {
        "last_updated": data[0]["last_updated"]
    }
    return jsonify(return_dict)


@app.route("/get/lista_territori", methods=["GET"])
def get_lista_territori():
    territori = []
    for t in data[0]["territori"]:
        # skip italia so we can add it on top
        if t["nome_territorio"] != "Italia":
            territori.append(t["nome_territorio"])

    territori.sort()
    territori.insert(0, "Italia")
    return_dict = {
        "territori": territori
    }
    return jsonify(return_dict)


@app.route("/get/italy", methods=["GET"])
def get_italy():
    for d in data:
        for t in d["territori"]:
            if t["nome_territorio"] == "Italia":
                return jsonify(t)


@app.route("/get/territori", methods=["GET"])
def get_territori():
    territori = data[0]["territori"]
    return_dict = [t for t in territori if t["nome_territorio"] != "Italia"]
    return jsonify(return_dict)


if __name__ == "__main__":
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="a")

    # scheduler setup
    scheduler = BackgroundScheduler()
    # data_job = scheduler.add_job(scrape_data, trigger="cron", minute="*/30")
    load_data()
    scheduler.start()
    # run app
    app.run(debug=True)
    logging.info("App started!")
