from scraper import Scraper
from datetime import datetime


def red(text):
    return "\x1b[1m\x1b[31m" + text + "\x1b[0m"


def green(text):
    return "\x1b[1m\x1b[32m" + text + "\x1b[0m"


def yellow(text):
    return "\x1b[1m\x1b[33m" + text + "\x1b[0m"


def white(text):
    return "\x1b[1m\x1b[37m" + text + "\x1b[0m"


def main():
    print(yellow("Starting tests."))
    print("Instantiating scraper...", end=" ", flush=True)
    try:
        started = datetime.now()
        s = Scraper()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        text = f"scraper instantiated [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))
        return

    # test methods
    failed = False
    total = 0
    passed = 0
    print("")
    print(yellow("Starting methods test."))

    print("Scraping history...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.scrapeHistory()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"history scraped [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Scraping data...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.scrapeData()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"data scraped [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))
        return

    print("Scraping colors...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.scrapeColors()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"colors scraped [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))
        return

    print("Saving data...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.saveData(all=True)
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"data saved [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))
        return

    percentage = int(passed/total * 100)
    print(yellow(f"Passed: {passed}/{total}"), end=" ", flush=True)

    if percentage < 100:
        print("[", red(f"{percentage}%"), "]", sep="")
        failed = True
    else:
        print("[", green(f"{percentage}%"), "]", sep="")

    # test getters
    total = 0
    passed = 0
    print("")
    print(yellow("Starting properties test."))

    print("Getting italy...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.italy
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"italy loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting territories list...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_list
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"territories list [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting absolute territories...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.absolute_territories
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"absolute territories loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting variation territories...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.variation_territories
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"variationterritories loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting categories...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.categories
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"categories loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting genders...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.genders
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"genders loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting age ranges...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.age_ranges
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"age ranges loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting history...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.history
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"history loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting territories color...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"territories color loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting territories slim...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_slim
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"territories color slim loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting territories color rgb...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_rgb
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"territories color rgb loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting territories color dummy...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_dummy
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"territories color dummy loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting territories color map...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_map
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"territories color map loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting territories percentage map...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_percentage_map
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"territories percentage map loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting vaccine producers slim...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.vaccine_producers
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"vaccine producersloaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    print("Getting subministrations...", end=" ", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.subministrations
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        text = f"subministrations loaded [{elapsed}ms] {green('✓')}"
        print(text)
    except Exception as e:
        print("error", red(e), red("x"))

    percentage = int(passed/total * 100)
    print(yellow(f"Passed: {passed}/{total}"), end=" ", flush=True)

    if percentage < 100:
        print("[", red(f"{percentage}%"), "]", sep="")
        failed = True
    else:
        print("[", green(f"{percentage}%"), "]", sep="")

    print("")

    if failed:
        print(red("TEST FAILED"))
    else:
        print(green("TEST PASSED"))

    print()


if __name__ == '__main__':
    main()
