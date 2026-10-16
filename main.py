# ==================================================
import csv
from wiktionary import get_page, get_word_class
from substantiv import substantiv_content
from verb import verb_content
from adjektiv import adjektiv_content
from andere import andere_content
from uebersetzung import uebersetzung_content

# ==================================================
# Takes class of word and section html and returns the dictionary
def process_word(word, word_class, section):
    if word_class == "Substantiv":
        return substantiv_content(section)

    if word_class == "Verb":
        return verb_content(word, section)

    if word_class == "Adjektiv":
        return adjektiv_content(section)

    return andere_content(word, word_class, section)


# =================================================
# Prepare content for CSV export
def prepare_list(items):
    if items is None:
        return ""
    return "<br>".join(items)


def prepare_for_csv(content):
    csv_content = {
        "Front": content["Front"],
        "Aussprache": content["Aussprache"],
        "Bedeutungen": prepare_list(content["Bedeutungen"]),
        "Sinnverwandte Wörter": prepare_list(content["Sinnverwandte Wörter"]),
        "Synonyme": prepare_list(content["Synonyme"]),
        "Beispiele": prepare_list(content["Beispiele"]),
        "Gegenwörter": prepare_list(content["Gegenwörter"]),
        "Herkunft": prepare_list(content["Herkunft"]),
        "Übersetzung Portugiesisch": content.get("Übersetzung Portugiesisch", ""),
        "Übersetzung Englisch": content.get("Übersetzung Englisch", "")
    }
    
    # ------------------------------------------
    # Substantiv-specific fields
    if content["Front"] == "Substantiv":
        csv_content["Substantiv"] = content["Substantiv"]
        csv_content["Substantiv Plural"] = content["Substantiv Plural"]
        csv_content["Aussprache Plural"] = content["Aussprache Plural"]

    # ------------------------------------------
    # Verb-specific fields
    elif content["Front"] == "Verb":
        csv_content["Verb"] = content["Verb"]
        csv_content["Perfekt"] = content["Perfekt"]
        csv_content["Perfekt Aussprache"] = content["Perfekt Aussprache"]
        csv_content["Präteritum"] = content["Präteritum"]
        csv_content["Präteritum Aussprache"] = content["Präteritum Aussprache"]
        csv_content["3. Singular"] = content["3. Singular"]
        csv_content["3. Singular Aussprache"] = content["3. Singular Aussprache"]

    # ------------------------------------------
    # Adjektiv-specific fields
    elif content["Front"] == "Adjektiv":
        csv_content["Adjektiv"] = content["Adjektiv"]
        csv_content["Komparativ"] = content["Komparativ"]
        csv_content["Komparativ Aussprache"] = content["Komparativ Aussprache"]
        csv_content["Superlativ"] = content["Superlativ"]
        csv_content["Superlativ Aussprache"] = content["Superlativ Aussprache"]

    # ------------------------------------------
    # Andere-specific fields
    else:
        csv_content["Andere"] = content["Andere"]
    return csv_content


# =================================================
# CSV Export
FIELDS = [
    "Front",
    "Substantiv",
    "Verb",
    "Adjektiv",
    "Andere",
    "Aussprache",
    "Substantiv Plural",
    "Aussprache Plural",
    "Perfekt",
    "Perfekt Aussprache",
    "Präteritum",
    "Präteritum Aussprache",
    "3. Singular",
    "3. Singular Aussprache",
    "Komparativ",
    "Komparativ Aussprache",
    "Superlativ",
    "Superlativ Aussprache",
    "Bedeutungen",
    "Sinnverwandte Wörter",
    "Synonyme",
    "Beispiele",
    "Gegenwörter",
    "Übersetzung Portugiesisch",
    "Übersetzung Englisch",
    "Herkunft"
]

def save_to_csv(words, filename="anki_deutsch.csv"):
    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )
        writer.writeheader()

        for word in words:
            soup = get_page(word)
            if soup is None:
                continue

            word_class, section = get_word_class(soup)
            content = process_word(
                word,
                word_class,
                section
            )
            content.update(uebersetzung_content(soup))

            if content is None:
                continue

            csv_content = prepare_for_csv(content)
            row = {
                field: ""
                for field in FIELDS
            }
            row["Front"] = word
            for field, value in csv_content.items():
                row[field] = value

            writer.writerow(row)


with open("Wörter.txt", "r", encoding="utf-8") as file:
    words = [
        line.strip()
        for line in file
        if line.strip()
    ]

words = list( dict.fromkeys(words) )

save_to_csv(words)