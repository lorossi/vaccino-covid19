from scraper import Scraper
from datetime import datetime
from string import printable


def red(text):
    return "\x1b[1m\x1b[31m" + str(text) + "\x1b[0m"


def green(text):
    return "\x1b[1m\x1b[32m" + str(text) + "\x1b[0m"


def yellow(text):
    return "\x1b[1m\x1b[33m" + str(text) + "\x1b[0m"


def white(text):
    return "\x1b[1m\x1b[37m" + str(text) + "\x1b[0m"

# Return real (printable) length of string


def rLen(text):
    return len("".join((filter(lambda x: x in printable, text))))


def main():
    failed = False
    width = 100
    result = "done"

    print(yellow("Starting tests."))
    incipit = "Instantiating scraper... "
    print(incipit, end="", flush=True)
    try:
        started = datetime.now()
        s = Scraper()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))
        return

    # test methods
    total = 0
    passed = 0
    print("")
    print(yellow("Starting methods test."))

    incipit = "Scraping history... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.scrapeHistory()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Scraping data... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.scrapeData()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Scraping colors... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.scrapeColors()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Saving data... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        s.saveData()
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

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

    incipit = "Getting italy... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.italy
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting territories list... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_list
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting absolute territories... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.absolute_territories
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting variation territories... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.variation_territories
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting categories... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.categories
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting genders... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.genders
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting age ranges... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.age_ranges
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting history... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.history
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting territories color... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting territories color slim... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_slim
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting territories color rgb... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_rgb
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting territories color dummy... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_dummy
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting territories color map... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_color_map
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting territories percentage map... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.territories_percentage_map
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting vaccine producers... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.vaccine_producers
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
    except Exception as e:
        print("error", red(e), red("x"))

    incipit = "Getting subministrations... "
    print(incipit, end="", flush=True)
    try:
        total += 1
        started = datetime.now()
        _ = s.subministrations
        elapsed = round((datetime.now() - started).microseconds / 1000, 2)
        passed += 1
        info = f"{green('✓')} [{green(elapsed)}{green('ms')}]"
        spacing = (width - rLen(incipit) -
                   rLen(result) - rLen(info))
        print(result, spacing * " ", info, sep="")
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
