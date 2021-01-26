from aqt.qt import *
from aqt import mw
from aqt.utils import showInfo, askUser, showWarning
from .lingq import authenticate, get_active_languages, get_cards
from PyQt5.QtWidgets import QDesktopWidget
from .model import get_lingq_model
from .config import (
    get_selected_languages,
    update_selected_languages,
    update_credentials,
    toggle_on_startup,
    get_on_startup,
)
from .const import LANGUAGE_CODES


def lingq_addon_main(is_logged_in):
    # Create a dialog window
    dialog = QDialog(mw)
    # Set window title
    dialog.setWindowTitle("Auto Sync LingQ")
    # Set window type to modal
    dialog.setWindowModality(Qt.WindowModal)

    # center dialog
    qtRect = dialog.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qtRect.moveCenter(cp)
    dialog.move(qtRect.topLeft())

    # Create a VBox layout - Each new widget is added vertically
    vbox = QVBoxLayout()
    vbox.setAlignment(Qt.AlignCenter)
    vbox.setContentsMargins(30, 30, 30, 100)

    # Create modal text
    modal_text = QLabel(
        """
    <p>This plugin will make Anki notes and cards from the words you've learned in 
    LingQ. As you learn more words on LingQ across your active languages, new words will automatically be added to your existing decks.</p>
    
    <hr>
    """
    )

    modal_text.setStyleSheet("min-width: 600; padding: 20")
    modal_text.setWordWrap(True)
    vbox.addWidget(modal_text)

    vbox.addSpacing(20)

    grid_layout = QGridLayout()
    grid_layout.setAlignment(Qt.AlignCenter)

    # Create login button
    login_btn = QPushButton("Login")

    # Create Select Languages Button
    select_lang_btn = QPushButton("Select Languages")

    if is_logged_in:
        # Disable login button
        login_btn.setEnabled(False)
        login_btn.setStyleSheet("width: 150; height: 30; font-size: 20px;")

        # Add info label
        label = QLabel(_("You're already logged in"))
        label.setStyleSheet("color: green; font-style: italic;")
        grid_layout.addWidget(label, 0, 1)

        # Enable select language button
        select_lang_btn.setEnabled(True)
        select_lang_btn.setStyleSheet(
            "width: 150; height: 30; background-color: #0099FF; color: #ffffff; font-style: bold"
        )

        # Add info label
        label2 = QLabel(_("Choose which languages to import"))
        label2.setStyleSheet("color: blue")
        grid_layout.addWidget(label2, 1, 1)
    else:
        # Enable login button
        login_btn.setEnabled(True)
        login_btn.setStyleSheet(
            "width: 150; height: 30; font-size: 20px; background-color: #0099FF; color: #ffffff; font-style: bold"
        )

        # Add info label
        label = QLabel(_("Please login"))
        label.setStyleSheet("color: blue;")
        grid_layout.addWidget(label, 0, 1)

        # Disable select language button
        select_lang_btn.setEnabled(False)
        select_lang_btn.setStyleSheet("width: 150; height: 30;")

        # Add info label
        label2 = QLabel(_("You must login before selecting languages to import"))
        label2.setStyleSheet("color: grey; font-style: italic;")
        grid_layout.addWidget(label, 1, 1)

    grid_layout.addWidget(login_btn, 0, 0)
    grid_layout.addWidget(select_lang_btn, 1, 0)

    # Add button to layout
    vbox.addLayout(grid_layout)

    # Add checkbox to set run on startup
    on_startup_box = QCheckBox("Run on startup?")
    on_startup_box.setChecked(get_on_startup())
    on_startup_box.stateChanged.connect(toggle_on_startup)
    vbox.addSpacing(40)
    vbox.addWidget(on_startup_box)

    def login_attempt():
        token = lingq_login()
        if token:
            dialog.close()
            lingq_addon_main(True)
        else:
            dialog.close()
            lingq_addon_main(False)

    def import_attempt():
        sync_info = lingq_select_languages()
        if sync_info:
            dialog.close()
            mw.reset()
            showInfo(sync_info)
            return
        else:
            mw.reset()
            return

    advice_text = QLabel(
        """<p>Each deck is generated with a Text-To-Speech preset added which can be used with the AwesomeTTS plugin.
    For AwesomeTTS to work you will need to save a preset for each language deck, presets should be named "lingq-LANGUAGECODE" 
    <br>e.g. To get AwesomeTTS working on an imported Spanish deck, go to manage presets in the AwesomeTTS addon settings and save a spanish voice
    preset with the name: lingq-es 
    <br><br><em>Note: You can see the language code for each language in the Select Languages pane.</em>
    <br><br><em><strong>Additional Note: setting Auto Sync LingQ to run on startup may cause startup delay</strong></em>
    """
    )
    advice_text.setWordWrap(True)
    advice_text.setStyleSheet("font-size: 15px; color: #505050")

    vbox.addWidget(advice_text)
    # Set dialog layout
    dialog.setLayout(vbox)
    login_btn.clicked.connect(login_attempt)
    select_lang_btn.clicked.connect(import_attempt)

    dialog.show()


def lingq_login():
    # Create a dialog window
    dialog = QDialog(mw)
    # Set window title
    dialog.setWindowTitle("Sync LingQ Login")
    # Set window type to modal
    dialog.setWindowModality(Qt.WindowModal)

    # Create a VBox layout - Each new widget is added vertically
    vbox = QVBoxLayout()
    vbox.setContentsMargins(30, 30, 30, 30)

    # Create modal text
    modal_text = QLabel(
        """
    <p>Please enter your <strong>LingQ</strong> username and password.</p>
    """
    )

    # Allow links to be open in browser from modal text
    modal_text.setOpenExternalLinks(True)
    # Configure modal text properties
    modal_text.setWordWrap(True)
    # Add modal text to vertical layout
    vbox.addWidget(modal_text)

    # Add some empty space before next item
    vbox.addSpacing(20)

    # Create a grid layout (user details and input will be 2x2 grid)
    grid_layout = QGridLayout()

    # Create label for username and add to grid
    user_label = QLabel(_("LingQ Username:"))
    grid_layout.addWidget(user_label, 0, 0)

    # Create a one-line user input field and add to grid
    user_input = QLineEdit()
    grid_layout.addWidget(user_input, 0, 1)

    # Create label for password input and add to grid
    password_label = QLabel(_("LingQ Password:"))
    grid_layout.addWidget(password_label, 1, 0)

    # Create a one-line password input field and add to grid
    password_input = QLineEdit()
    password_input.setEchoMode(QLineEdit.Password)  # Converts input to protected text
    grid_layout.addWidget(password_input, 1, 1)

    # Add user details grid to vertical layout
    vbox.addLayout(grid_layout)

    # Add confirmation button
    bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    bb.button(QDialogButtonBox.Ok).setAutoDefault(True)
    bb.accepted.connect(dialog.accept)
    bb.rejected.connect(dialog.reject)
    vbox.addWidget(bb)

    dialog.setLayout(vbox)
    dialog.show()

    # Resume execution after confirmation pressed
    accepted = dialog.exec_()
    u = user_input.text()
    p = password_input.text()
    if not accepted or not u or not p:
        return

    update_credentials(u, p)

    token = authenticate()
    if not token:
        showWarning(
            "Login Failed. Please check your username and password then try again."
        )
        lingq_login()

    return token


def lingq_select_languages():
    # Create a dialog window
    dialog = QDialog(mw)
    dialog.setWindowTitle("Select LingQ Language Decks")
    # Set window type to modal
    dialog.setWindowModality(Qt.WindowModal)

    # Create a VBox layout - Each new widget is added vertically
    vbox = QVBoxLayout()
    vbox.setContentsMargins(30, 30, 30, 30)

    # Create modal text
    modal_text = QLabel(
        """Below is a list of languages which you are studying on LingQ.<br><br>Please select the languages which you would like synced.
    """
    )

    # Allow links to be open in browser from modal text
    modal_text.setOpenExternalLinks(True)
    # Configure modal text properties
    modal_text.setWordWrap(True)
    # Add modal text to vertical layout
    vbox.addWidget(modal_text)

    # Add some empty space before next item
    vbox.addSpacing(20)

    # Create a model that will act as list of checkboxes
    model = QStandardItemModel()

    # Get all of the user's active languages in LingQ
    user_languages = get_active_languages()

    # Take note of any languages user has selected in previous session
    selected_languages = get_selected_languages()

    if user_languages:  # Check that languages were returned successfully
        # Create a list of checkbox items for each language supported by LingQ
        for language in user_languages:
            lang_item = QStandardItem(language + " " + LANGUAGE_CODES[language])
            lang_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

            # If the language was already selected previously set its state to checked
            if language in selected_languages:
                lang_item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
            else:
                lang_item.setData(QVariant(Qt.Unchecked), Qt.CheckStateRole)

            # Add language checkbox to list
            model.appendRow(lang_item)

    else:  # If no languages returned abort plugin
        warning = "Uh oh! There seems to have been a problem getting your list of active languages from LingQ 😮<br>"
        warning += "<hr><br>"
        warning += "If you're seeing this, you can send a friendly email to <b style=\"color:#013220\">ciarancurran.dev@gmail.com</b> (Ciaran) and he'll see what he can do :)"
        showWarning(warning)
        return

    view = QListView()
    view.setModel(model)
    vbox.addWidget(view)

    # Create and add confirm or cancel buttons to bottom of dialog
    bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    bb.button(QDialogButtonBox.Ok).setAutoDefault(True)
    bb.accepted.connect(dialog.accept)
    bb.rejected.connect(dialog.reject)
    vbox.addWidget(bb)

    dialog.setLayout(vbox)
    dialog.show()
    accepted = dialog.exec_()

    if not accepted:
        return

    # Get chosen languages after confirmation button is pressed
    selected_languages = []

    for i in range(0, model.rowCount()):
        lang_item = model.item(i)
        if lang_item.checkState():
            selected_languages.append(lang_item.text().split(" ")[0])

    # Add selected languages to config
    update_selected_languages(selected_languages)

    # Sync cards
    sync_info = lingq_sync_cards()

    return sync_info


def lingq_sync_cards():
    # String to gather info about the import so it can be shown to user
    sync_info = "LingQ import:\n\n"

    for language in get_selected_languages():
        deck_name = "LingQ " + language
        deck_id = mw.col.decks.id_for_name(deck_name)

        # If deck does not already exist create new one
        if not deck_id:
            # creates new deck
            deck_id = mw.col.decks.id(deck_name)

        # Get model associated with deck name, if none exists create one
        model = get_lingq_model(mw, deck_id, language)

        if not model:
            showWarning("Could not find or create LingQ Sync note type.")
            return

        # I don't quite understand ANKI, but for some reason commenting out the next line seems to work when I think it shouldn't 🤷‍♂️  ️
        # mw.col.decks.select(deck_id)

        # Get all cards for language
        cards_import = get_cards(language)

        # Get all notes in deck
        note_ids = mw.col.models.nids(model)
        note_words = [mw.col.getNote(note_id)["Front"] for note_id in note_ids]

        cards_to_add = []

        # Check if there are any new notes
        for card in cards_import:
            if not any(note_word == card["term"] for note_word in note_words):
                cards_to_add.append(card)

        count = 0
        # For each new word create a note for that deck
        for card in cards_to_add:
            note = mw.col.newNote()

            note["Front"] = card["term"]
            note["Back"] = card["hints"][0]["text"]

            mw.col.addNote(note)
            count += 1

        sync_info += "{} {} cards added\n".format(count, language)

    return sync_info
