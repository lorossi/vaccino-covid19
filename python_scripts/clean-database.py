import json
import os
from datetime import datetime, timedelta


def main():
    cwd = os.getcwd() + "/"
    json_filename = "vaccini.json"
    json_output_filename = "vaccini-cleaned.json"
    output_path = "output/"

    with open(cwd + output_path + json_filename, "r") as f:
        old_data = json.load(f)

    old_data.sort(key=lambda x: datetime.fromisoformat(x['script_timestamp']), reverse=True)

    cleaned_data = []
    first_in_day = None
    last_timestamp = []
    for d in old_data:
        time_obj = datetime.fromisoformat(d["script_timestamp"])

        if not last_timestamp:
            last_timestamp.append(time_obj)
        else:
            if time_obj.date() != last_timestamp[-1].date():
                last_timestamp.append(time_obj)


    for t in last_timestamp:
        for d in old_data:
            if t == datetime.fromisoformat(d["script_timestamp"]):
                cleaned_data.append(d)
                break

    for x in range(len(old_data) - 1, 0, -1):
        for t in old_data[x]["territori"]:
            t["percentuale_dosi_utilizzate"] = t["totale_vaccinati"] / t["totale_dosi_consegnate"] * 100
            for o in old_data[x-1]["territori"]:
                if o["nome_territorio"] == t["nome_territorio"]:
                    t["nuovi_vaccinati"] = o["totale_vaccinati"] - t["totale_vaccinati"]

    with open(cwd + output_path + json_output_filename, "w") as f:
        json.dump(cleaned_data, f, indent=4)


if __name__ == "__main__":
    main()
