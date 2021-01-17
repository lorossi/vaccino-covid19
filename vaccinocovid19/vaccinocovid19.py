from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify
import logging
from scraper import Scraper


# Objects
s = Scraper()
app = Flask(__name__)


def main():
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="w")

    # scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(scrape_data, trigger="cron", minute="*/15")
    scheduler.add_job(scrape_history, trigger="cron", minute="5", hour="0")
    scheduler.add_job(push_to_github, trigger="cron", minute="55", hour="23")
    s.loadData()
    # run app
    logging.info("App started!")


def scrape_data():
    s.scrapeData()
    s.saveData()


def scrape_history():
    s.scrapeHistory()
    s.saveData()


def push_to_github():
    s.pushToGitHub()
    logging.info("pushed to GitHub")


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
                           territories_list=s.territories_list, italy=s.italy)


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


# error 404 page
@app.errorhandler(404)
def error_400(e):
    logging.error("error 404: %s", e)
    return render_template("error.html", errorcode=404,
                           errordescription="page not found"), 404


main()

if __name__ == "__main__":
    app.run()
