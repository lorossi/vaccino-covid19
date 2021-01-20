import logging
from scraper import Scraper
from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler


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
    scheduler.add_job(scrape_colors, trigger="cron", minute="10", hour="0")
    s.scrapeAll()
    # run app
    logging.info("App started!")


def scrape_data():
    s.scrapeAll()
    s.saveData()

def scrape_colors():
    s.scrapeTerritoriesColor()
    s.saveData()


# index
@app.route("/")
@app.route("/homepage")
def index():
    return render_template("index.html", italy=s.italy,
                           territories_list=s.territories_list)


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


@app.route("/get/sesso", methods=["GET"])
def get_sessi():
    return jsonify(s.genders)


@app.route("/get/fasce_eta", methods=["GET"])
def get_fasce_eta():
    return jsonify(s.age_ranges)


@app.route("/get/storico_vaccini", methods=["GET"])
def get_storico_vaccini():
    return jsonify(s.history)


@app.route("/get/storico_vaccini/<codice_territorio>", methods=["GET"])
def get_storico_territorio(codice_territorio):
    return jsonify(s.territoryHistory(codice_territorio))


@app.route("/get/colore_territori", methods=["GET"])
def get_colore_territori():
    return jsonify(s.territories_color)


@app.route("/get/produttori_vaccini", methods=["GET"])
def get_produttori_vaccini():
    return jsonify(s.vaccine_producers)


@app.route("/get/somministrazioni", methods=["GET"])
def get_somministrazioni():
    return jsonify(s.subministrations)


# error 404 page
@app.errorhandler(404)
def error_400(e):
    logging.error("error 404: %s", e)
    return render_template("error.html", errorcode=404,
                           errordescription="page not found"), 404


# error 500 page
@app.errorhandler(Exception)
def error_500(e):
    logging.error("error 500: %s", e)
    return render_template("error.html", errorcode=500,
                           errordescription="internal server error"), 500


main()

if __name__ == "__main__":
    app.run(debug=True)
