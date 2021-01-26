import requests as http
from aqt.addons import ConfigEditor
from aqt import mw
from aqt.qt import *
from aqt.utils import showWarning
from .config import get_credentials
from .const import LANGUAGE_CODES

# If user is authenticated return authorization token otherwise return None
def authenticate():
    # Get username and password if they exist
    username, password = get_credentials()

    if username and password:
        authenticate_url = "https://www.lingq.com/api/api-token-auth/"
        response = http.post(
            authenticate_url,
            data={"username": username, "password": password},
        )

        if response.status_code == http.codes.ok:
            return response.json()["token"]
    return


def get_cards(language):
    token = authenticate()

    if token:
        # Retrieve language code for the language with given title
        language_code = LANGUAGE_CODES[language]

        cards_url = "https://www.lingq.com/api/v2/{}/cards/?page_size=100".format(
            language_code
        )
        response = http.get(
            cards_url, headers={"Authorization": "Token {}".format(token)}
        ).json()

        cards = []

        # Iterate over paginated response until all cards collected
        while True:
            # collect page of cards
            cards.extend(response["results"])

            if not response["next"]:
                break

            cards_url = response["next"]
            # get next page of cards
            response = http.get(
                cards_url, headers={"Authorization": "Token {}".format(token)}
            ).json()

        return cards

    showWarning("Failed to load cards")


def get_active_languages():
    token = authenticate()

    if token:
        active_lang_url = "https://www.lingq.com/api/v2/contexts"

        response = http.get(
            active_lang_url, headers={"Authorization": "Token {}".format(token)}
        )

        languages = []
        for context in response.json()["results"]:
            languages.append(context["language"]["title"])

        return languages

    showWarning("Failed to get active languages")
