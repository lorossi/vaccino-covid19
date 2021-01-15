from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify
import logging
from scraper import Scraper


app = Flask(__name__)


def main():
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="w")
    # scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_data, trigger="cron", minute="*/15")
    scheduler.add_job(scrape_history, trigger="cron", minute="5", hour="0")
    scheduler.add_job(push_to_github, trigger="cron", minute="10", hour="0")
    scheduler.start()
    s.load_data()
    # run app
    logging.info("App started!")


def scrape_data():
    s.scrape_data()
    s.save_data()


def scrape_history():
    s.scrape_history()
    s.save_data()


def push_to_github():
    # THIS HAS TO BE CHANGED WHEN DEPLOYED
    return
    s.push_to_GitHub()


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
    return render_template("index.html")


@app.route("/get/last_updated", methods=["GET"])
def get_last_updated():
    return_dict = {
        "last_updated": s.last_updated
    }
    return jsonify(return_dict)


@app.route("/get/lista_territori", methods=["GET"])
def get_lista_territori():
    return_dict = {
        "territori": s.territories_list
    }
    return jsonify(return_dict)


@app.route("/get/italy", methods=["GET"])
def get_italy():
    italy = s.italy
    return jsonify(italy)


@app.route("/get/territori", methods=["GET"])
def get_territori():
    territori = s.absolute_territories
    return jsonify(territori)


@app.route("/get/variazioni", methods=["GET"])
def get_variazioni():
    variazioni = s.variation_territories
    return jsonify(variazioni)


@app.route("/get/categorie", methods=["GET"])
def get_categorie():
    categorie = s.categories
    return jsonify(categorie)


@app.route("/get/sessi", methods=["GET"])
def get_sessi():
    sesso = s.genders
    return jsonify(sesso)


@app.route("/get/fasce_eta", methods=["GET"])
def get_fasce_eta():
    fasce_eta = s.age_ranges
    return jsonify(fasce_eta)


@app.route("/get/storico_vaccini", methods=["GET"])
def get_storico_vaccini():
    return jsonify(s.history)


# error 404 page
@app.errorhandler(404)
def error_400(e):
    logging.error("error 404: %s", e)
    return render_template("error.html", errorcode=404,
                           errordescription="page not found"), 404


# Objects
s = Scraper()
main()


if __name__ == "__main__":
    main()
    app.run()
