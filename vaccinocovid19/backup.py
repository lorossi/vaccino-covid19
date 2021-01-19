from scraper import Scraper
import logging


if __name__ == "__main__":
    logfile = "backup.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="w")

    s = Scraper()
    s.backup()
