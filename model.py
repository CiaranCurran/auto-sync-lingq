from aqt.utils import askUser, showInfo
from .const import LANGUAGE_CODES

_field_names = ["Front", "Back"]


def create_model(mw, did, language):
    mm = mw.col.models
    m = mm.new(mw.col.decks.get(did)["name"] + " Model")

    for field_name in _field_names:
        fm = mm.newField(_(field_name))
        mm.addField(m, fm)

    t = mm.newTemplate("Card 1")
    t["qfmt"] = "<tts preset='lingq-%s'>{{ Front }}</tts>" % LANGUAGE_CODES[language]
    t["afmt"] = "{{ Front }}<br><hr><br>{{ Back }}"

    m["did"] = did
    mm.addTemplate(m, t)

    mm.add(m)
    mw.col.models.save(m)
    return m


def get_lingq_model(mw, did, language):
    # Get name of deck
    deck_name = mw.col.decks.get(did)["name"]

    # Model name is in format "DECK_NAME Model" e.g "LingQ Japanese Model"
    mid = mw.col.models.id_for_name("%s Model" % deck_name)
    m = mw.col.models.get(mid)

    if not m:
        # TODO find a non-blocking alternative
        # showInfo("LingQ Sync note type not found. Creating...")
        m = create_model(mw, did, language)

    # Add new fields if they don't exist yet
    fields_to_add = [
        field_name
        for field_name in _field_names
        if field_name not in mw.col.models.fieldNames(m)
    ]

    if fields_to_add:
        showInfo(
            """
        <p>The LingQ Sync plugin has recently been upgraded to include the following attributes: {}</p>
        <p>This change will require a full-sync of your card database to your Anki-Web account.</p>
        """.format(
                ", ".join(fields_to_add)
            )
        )
        for field_name in fields_to_add:
            pass
            fm = mw.col.models.newField(_(field_name))
            mw.col.models.addField(m, fm)
            mw.col.models.save(m)

    return m