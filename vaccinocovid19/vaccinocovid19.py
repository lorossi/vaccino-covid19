import logging
from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

from scraper import Scraper
from colorsofitaly import ColorsOfItaly


# Objects
s = Scraper()
c = ColorsOfItaly()
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['TEMPLATES_AUTO_RELOAD'] = True


def main():
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="w")

    # scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(scrape_data, trigger="cron", minute="*/15")
    scheduler.add_job(scrape_colors, trigger="cron", minute="0", hour="*")
    # run app
    logging.info("App started!")


def scrape_data():
    try:
        s.scrapeHistory()
        s.scrapeData()
        s.saveData(history=True, data=True)
        logging.info("History and data scraped")
    except Exception as e:
        logging.error(f"Error while scraping history and data. Error {e}")


def scrape_colors():
    try:
        s.scrapeColors()
        s.saveData(colors=True)
        logging.info("Colors scraped")
    except Exception as e:
        logging.error(f"Error while scraping colors. Error {e}")


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


@app.route("/get/storico_vaccini/<nome_territorio>", methods=["GET"])
def get_storico_territorio(nome_territorio):
    return jsonify(s.territoryHistory(nome_territorio))


@app.route("/get/colore_territori", methods=["GET"])
def get_colore_territori():
    return jsonify(s.territories_color)


@app.route("/get/colore_territori_slim", methods=["GET"])
def get_colore_territori_slim():
    return jsonify(s.territories_color_slim)


@app.route("/get/colore_territori_rgb", methods=["GET"])
def get_colore_territori_rgb():
    return jsonify(s.territories_color_rgb)


@app.route("/get/colore_territori_slim_dummy", methods=["GET"])
def get_colore_territori_slim_dummy():
    return jsonify(s.territories_color_dummy)


@app.route("/get/mappa_colore_territori", methods=["GET"])
def get_mappa_colore_territori():
    return jsonify(s.territories_color_map)


@app.route("/get/mappa_percentuale_territori", methods=["GET"])
def get_mappa_percentuale_territori():
    return jsonify(s.territories_percentage_map)


@app.route("/get/produttori_vaccini", methods=["GET"])
def get_produttori_vaccini():
    return jsonify(s.vaccine_producers)


@app.route("/get/somministrazioni", methods=["GET"])
def get_somministrazioni():
    return jsonify(s.subministrations)


@app.route("/get/ota_update", methods=["GET"])
def get_ota_version():
    return jsonify(c.ota_infos)


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
    app.run()
