import scraper
import cleandatabase
import json

# IMPORTANT
# run this before starting the server
# this script is useful to "clean" the "database" and to allow the migration
# to the new flask based website.
# the fields inside the json file have changed so we need to convert all the
# old gathered data. This needs to be done only once, before starting the
# server for the first time

def main():
    cleandatabase.download()
    try:
        cleandatabase.clean()
        print("database cleaned")
    except Exception as e:
        print("database already clean")

    scraper.setup(log=False, verbose=False)
    data = scraper.scrape_data()
    history = scraper.scrape_history(data)
    scraper.save_data(data, history)
    print("data scraped")
    print("now start flask")


if __name__ == "__main__":
    main()
