import os
import logging
import subprocess
from scraper import Scraper
from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler


# Objects
s = Scraper()
app = Flask(__name__)
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

def main():
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="w")

    # scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(scrape_data, trigger="cron", minute="*/15")
    scheduler.add_job(push_to_github, trigger="cron", minute="35", hour="17")
    scheduler.add_job(scrape_history, trigger="cron", minute="5", hour="0")
    scheduler.add_job(scrape_colors, trigger="cron", minute="10", hour="0")
    s.loadData()
    # run app
    logging.info("App started!")


def scrape_data():
    s.scrapeData()
    s.saveData()


def scrape_history():
    s.scrapeHistory()
    s.saveData()


def scrape_colors():
    s.scrapeTerritoriesColor()
    s.saveData()


def push_to_github():
    subprocess.run(["sh", "backup.sh"])


# error 500 page
@app.errorhandler(Exception)
def error_500(e):
    logging.error("error 500: %s", e)
    return render_template("error.html", errorcode=500,
                           errordescription="internal server error"), 500


# index
@app.route("/")
@app.route("/homepage")
def index():
    return render_template("index.html", last_updated=s.last_updated,
                           territories_list=s.territories_list, italy=s.italy,
                           territory_colors=s.territory_colors)


@app.route("/get/italia", methods=["GET"])
def get_italia():
    return jsonify(s.italy)


@app.route("/get/territori", methods=["GET"])
def get_territori():
    return jsonify(s.absolute_territories)


@app.route("/get/variazioni", methods=["GET"])
def get_variazioni():
    return jsonify(s.variation_territories)


@app.route("/get/categorie", methods=["GET"])
def get_categorie():
    return jsonify(s.categories)


@app.route("/get/sessi", methods=["GET"])
def get_sessi():
    return jsonify(s.genders)


@app.route("/get/fasce_eta", methods=["GET"])
def get_fasce_eta():
    return jsonify(s.age_ranges)


@app.route("/get/storico_vaccini", methods=["GET"])
def get_storico_vaccini():
    return jsonify(s.history)


@app.route("/get/colore_territori", methods=["GET"])
def get_colore_territori():
    return jsonify(s.territory_colors)


# error 404 page
@app.errorhandler(404)
def error_400(e):
    logging.error("error 404: %s", e)
    return render_template("error.html", errorcode=404,
                           errordescription="page not found"), 404


main()

if __name__ == "__main__":
    app.run()
