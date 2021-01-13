import scraper
import cleandatabase
import json


def main():
    try:
        cleandatabase.clean()
        print("databse cleaned")
    except Exception as e:
        print("database already clean")

    scraper.setup()
    data = scraper.scrape_data()
    history = scraper.scrape_history(data)
    scraper.save_data(data, history)
    print("data scraped")
    print("now start flask")


if __name__ == "__main__":
    main()
