def uebersetzung_content(soup):
    table = soup.find(
        "table",
        class_="uetabelle__table",
        title="Übersetzungen in andere Sprachen"
    )

    translations = {
        "Übersetzung Portugiesisch": [],
        "Übersetzung Englisch": []
    }

    if table is None:
        return {key: "" for key in translations}

    languages = {
        "Portugiesisch": ("pt", "Übersetzung Portugiesisch"),
        "Englisch": ("en", "Übersetzung Englisch")
    }

    for item in table.find_all("li"):
        for language, (lang_code, field) in languages.items():
            if item.find("a", title=language) is None:
                continue

            for span in item.find_all("span", lang=lang_code):
                link = span.find("a")

                if link is not None:
                    word = link.get_text(" ", strip=True)

                    if word and word not in translations[field]:
                        translations[field].append(word)

    return {
        field: ", ".join(words)
        for field, words in translations.items()
    }