from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, askUser, showWarning
from aqt.addons import ConfigEditor
from .const import ADDON

config = mw.addonManager.getConfig(ADDON)
print(config)


def update_selected_languages(selected_languages):
    config = mw.addonManager.getConfig(ADDON)
    config["selected_languages"] = selected_languages
    mw.addonManager.writeConfig(ADDON, config)


def update_credentials(username, password):
    config = mw.addonManager.getConfig(ADDON)
    config["username"] = username
    config["password"] = password
    mw.addonManager.writeConfig(ADDON, config)


def get_credentials():
    config = mw.addonManager.getConfig(ADDON)
    return (config["username"], config["password"])


def get_selected_languages():
    config = mw.addonManager.getConfig(ADDON)
    return config["selected_languages"]


def toggle_on_startup():
    config = mw.addonManager.getConfig(ADDON)
    config["on_startup"] = not config["on_startup"]
    mw.addonManager.writeConfig(ADDON, config)


def get_on_startup():
    config = mw.addonManager.getConfig(ADDON)
    return config["on_startup"]