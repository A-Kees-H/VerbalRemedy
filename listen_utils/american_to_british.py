import re

def american_to_british(text):
    # Extended American to British spelling dictionary (no words ending in i, z, e)
    am_to_br = {
        "acknowledgment": "acknowledgement",
        "aluminum": "aluminium",
        "ax": "axe",
        "armored": "armoured",
        "balk": "baulk",
        "behavior": "behaviour",
        "catalog": "catalogue",
        "canceled": "cancelled",
        "counselor": "counsellor",
        "defense": "defence",
        "dialog": "dialogue",
        "enroll": "enrol",
        "fulfill": "fulfil",
        "fueling": "fuelling",
        "gray": "grey",
        "honor": "honour",
        "humor": "humour",
        "jewelry": "jewellery",
        "maneuver": "manoeuvre",
        "mold": "mould",
        "offense": "offence",
        "plow": "plough",
        "program": "programme",
        "rumor": "rumour",
        "skeptic": "sceptic",
        "skeptical": "sceptical",
        "specialty": "speciality",
        "theater": "theatre",
        "traveling": "travelling",
        "traveler": "traveller",
        "woolen": "woollen",
        "license": "licence",
        "practice": "practise",
        "catalogs": "catalogues",
        "maneuvers": "manoeuvres",
        "plows": "ploughs",
        "armors": "armours",
        # More words can be added here
    }

    # Precompile regex for splitting words, keeping punctuation
    word_pattern = re.compile(r"\b\w+\b")

    def convert_word(word):
        lower_word = word.lower()
        replacement = None

        # Exact match
        if lower_word in am_to_br:
            replacement = am_to_br[lower_word]
        # Plural match: word + 's' or 'es'
        elif lower_word.endswith('s') and lower_word[:-1] in am_to_br:
            replacement = am_to_br[lower_word[:-1]] + 's'
        elif lower_word.endswith('es') and lower_word[:-2] in am_to_br:
            replacement = am_to_br[lower_word[:-2]] + 'es'

        if replacement:
            # Preserve capitalization
            if word[0].isupper():
                return replacement.capitalize()
            return replacement

        # Handle -ize → -ise and -yze → -yse
        if lower_word.endswith("yze"):
            british_word = re.sub(r"yze$", "yse", lower_word)
        elif lower_word.endswith("ize"):
            british_word = re.sub(r"ize$", "ise", lower_word)
        else:
            british_word = None

        if british_word:
            if word[0].isupper():
                return british_word.capitalize()
            return british_word

        return word

    # Replace each word individually
    converted_text = word_pattern.sub(lambda m: convert_word(m.group()), text)
    return converted_text