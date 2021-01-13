from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify
import logging
import scraper
import json


# GLOBAL VARIABLES
data = []
history = []
app = Flask(__name__)

# error 500 page
@app.errorhandler(Exception)
def error_500(e):
    logging.error("error 500: %s", e)
    return render_template("error.html", errorcode=500,
                           errordescription="internal server error"), 500


def main():
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="w")
    # scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_data, trigger="cron", minute="*/15")
    scheduler.start()
    load_data()
    # run app
    logging.info("App started!")


def load_settings(path="src/settings/settings.json"):
    with open(path, "r") as f:
        return json.load(f)


def scrape_data():
    global data, history
    scraper.setup(log=True, verbose=False)
    data = scraper.scrape_data()
    history = scraper.scrape_history(data)
    scraper.save_data(data, history)


def load_data():
    global data, history
    data, history = scraper.load_data()


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
    return_dict = {
        "territori": data[0]["lista_territori"]
    }
    return jsonify(return_dict)


@app.route("/get/italy", methods=["GET"])
def get_italy():
    return_dict = {}

    for a in data[0]["assoluti"]:
        if a["nome_territorio"] == "Italia":
            return_dict.update(a)
            break

    for v in data[0]["variazioni"]:
        if v["nome_territorio"] == "Italia":
            return_dict.update(v)
            break

    return jsonify(return_dict)


@app.route("/get/territori", methods=["GET"])
def get_territori():
    territori = data[0]["assoluti"]
    return_list = [t for t in territori if t["nome_territorio"] != "Italia"]
    return jsonify(return_list)


@app.route("/get/variazioni", methods=["GET"])
def get_variazioni():
    variazioni = data[0]["variazioni"]
    return_list = [v for v in variazioni if v["nome_territorio"] != "Italia"]
    return jsonify(return_list)


@app.route("/get/categorie", methods=["GET"])
def get_categorie():
    categorie = data[0]["categorie"]
    return jsonify(categorie)


@app.route("/get/sessi", methods=["GET"])
def get_sessi():
    sesso = data[0]["sesso"]
    return jsonify(sesso)


@app.route("/get/fasce_eta", methods=["GET"])
def get_fasce_eta():
    sesso = data[0]["fasce_eta"]
    return jsonify(sesso)


@app.route("/get/storico_vaccini", methods=["GET"])
def get_storico_vaccini():
    return jsonify(history[1:])


# error 404 page
@app.errorhandler(404)
def error_400(e):
    logging.error("error 404: %s", e)
    return render_template("error.html", errorcode=404,
                           errordescription="page not found"), 404


@app.before_first_request
def run_once():
    main()


if __name__ == "__main__":
    main()
