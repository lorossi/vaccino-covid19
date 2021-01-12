import json
import os
from datetime import datetime, timedelta


def main():
    cwd = os.getcwd() + "/"
    json_filename = "vaccini.json"
    json_output_filename = "vaccini-cleaned.json"
    output_path = "src/output/"

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

    for x in range(len(cleaned_data)):
        new_territories = {
            "assoluti": [],
            "variazioni": []
        }

        for y in range(len(cleaned_data[x]["territori"])):
            new_absolute = {
                "nome_territorio": cleaned_data[x]["territori"][y]["nome_territorio"],
                "codice_territorio": cleaned_data[x]["territori"][y].get("codice_territorio", None),
                "totale_vaccinati": cleaned_data[x]["territori"][y]["totale_vaccinati"],
                "percentuale_popolazione_vaccinata": float(cleaned_data[x]["territori"][y]["percentuale_popolazione_vaccinata"]),
                "totale_dosi_consegnate": cleaned_data[x]["territori"][y]["totale_dosi_consegnate"],
                "percentuale_dosi_utilizzate": cleaned_data[x]["territori"][y]["totale_vaccinati"] / cleaned_data[x]["territori"][y]["totale_dosi_consegnate"] * 100
            }

            if x < len(old_data) - 1:
                new_variations = {
                    "nome_territorio": cleaned_data[x]["territori"][y]["nome_territorio"],
                    "codice_territorio": cleaned_data[x]["territori"][y].get("codice_territorio", None),
                    "nuovi_vaccinati": cleaned_data[x]["territori"][y]["nuovi_vaccinati"],
                    "percentuale_nuovi_vaccinati": cleaned_data[x]["territori"][y]["nuovi_vaccinati"] / cleaned_data[x+1]["territori"][y]["totale_vaccinati"] * 100,
                    "nuove_dosi_consegnate": cleaned_data[x]["territori"][y]["totale_dosi_consegnate"] - cleaned_data[x+1]["territori"][y]["totale_dosi_consegnate"],
                    "percentuale_nuove_dosi_consegnate": (cleaned_data[x]["territori"][y]["totale_dosi_consegnate"] - cleaned_data[x+1]["territori"][y]["totale_dosi_consegnate"]) / cleaned_data[x+1]["territori"][y]["totale_dosi_consegnate"] * 100
                }

            new_territories["assoluti"].append(new_absolute)

            if new_variations:
                new_territories["variazioni"].append(new_variations)

        for y in range(len(cleaned_data[x]["fasce_eta"])):
            cleaned_data[x]["fasce_eta"][y]["nome_categoria"] = cleaned_data[x]["fasce_eta"][y]["nome_categoria"].replace("<=", "0-")

        cleaned_data[x].update(new_territories)

    for x in range(len(cleaned_data)):
        del cleaned_data[x]["territori"]



    with open(cwd + output_path + json_output_filename, "w") as f:
        json.dump(cleaned_data, f, indent=2)


if __name__ == "__main__":
    main()
