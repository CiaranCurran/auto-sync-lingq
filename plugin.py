from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, askUser, showWarning
from aqt.addons import ConfigEditor
from aqt.gui_hooks import profile_did_open
from .lingq import authenticate
from .dialog import lingq_addon_main, lingq_sync_cards
from .const import ADDON
from .config import get_credentials, get_on_startup

# in order to pass "mw" to "ConfigEditor" as parent widget
mw.mgr = mw.addonManager

# Runs sync on statup of anki
def run_sync():
    username, password = get_credentials()

    is_logged_in = False
    # Check if there are existing credentials
    if username and password:
        # Check if credentials are valid
        auth_token = authenticate()
        if auth_token:
            is_logged_in = True

    if is_logged_in:
        sync_info = lingq_sync_cards()
        mw.reset()
        showInfo(sync_info)
    else:
        showInfo(
            "You need to login before you can import. Go to addon config to login."
        )

    return


# Runs when the addon config button is pressed
def config_action():

    username, password = get_credentials()

    is_logged_in = False
    # Check if there are existing credentials
    if username and password:
        # Check if credentials are valid
        auth_token = authenticate()
        if auth_token:
            is_logged_in = True

    # show main addon dialog window
    lingq_addon_main(is_logged_in)

    return


# Check if the user has selected to run sync on startup
if get_on_startup():
    profile_did_open.append(run_sync)

# Enable a config action to be called for the addon
mw.addonManager.setConfigAction(ADDON, config_action)