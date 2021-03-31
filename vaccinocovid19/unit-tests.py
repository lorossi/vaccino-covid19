from scraper import Scraper
from colorsofitaly import ColorsOfItaly
from time import time
from string import printable


def red(text):
    return f"\x1b[1m\x1b[31m{text}\x1b[0m"


def green(text):
    return f"\x1b[1m\x1b[32m{text}\x1b[0m"


def yellow(text):
    return f"\x1b[1m\x1b[33m{text}\x1b[0m"


def white(text):
    return f"\x1b[1m\x1b[37m{text}\x1b[0m"

# Return real (printable) length of string


def rLen(text):
    return len("".join(s for s in text if s in printable))


def main():
    failed = False
    width = 50
    result = "done"

    print(yellow("Starting tests."))
    incipit = "Instantiating scraper... "
    print(incipit, end="", flush=True)
    try:
        started = time()
        s = Scraper()
        elapsed = round((time() - started) * 1000, 2)
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")
        return

    incipit = "Instantiating colors of italy... "
    print(incipit, end="", flush=True)
    try:
        started = time()
        c = ColorsOfItaly()
        elapsed = round((time() - started) * 1000, 2)
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")
        return

    # test methods
    total = 0
    passed = 0
    print()
    print(yellow("Starting methods test."))

    incipit = "Scraping history... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        s.scrapeHistory()
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Scraping data... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        s.scrapeData()
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Scraping colors... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        s.scrapeColors()
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Saving data... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        s.saveData()
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

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
    print()
    print(yellow("Starting properties test."))

    incipit = "Getting italy... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.italy
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting territories list... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.territories_list
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting absolute territories... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.absolute_territories
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting variation territories... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.variation_territories
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting categories... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.categories
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting genders... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.genders
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting age ranges... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.age_ranges
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting history... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.history
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting territories color... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.territories_color
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting territories color slim... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.territories_color_slim
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting territories color rgb... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.territories_color_rgb
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting territories color dummy... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.territories_color_dummy
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting territories color map... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.territories_color_map
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting territories percentage map... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.territories_percentage_map
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting vaccine producers... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.vaccine_producers
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting subministrations... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = s.subministrations
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    incipit = "Getting ota infos... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = time()
        _ = c.ota_infos
        elapsed = round((time() - started) * 1000, 2)
        passed += 1
        info = f"{green('PASS')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        spacing = width - rLen(incipit)
        print(spacing * " ", red("FAIL"), " error: ", red(e), sep="")

    percentage = int(passed/total * 100)
    print(yellow(f"Passed: {passed}/{total}"), end=" ", flush=True)

    if percentage < 100:
        print("[", red(f"{percentage}%"), "]", sep="")
        failed = True
    else:
        print("[", green(f"{percentage}%"), "]", sep="")

    print()

    if failed:
        print(red("TEST FAILED"))
    else:
        print(green("TEST PASSED"))

    print()


if __name__ == '__main__':
    main()
