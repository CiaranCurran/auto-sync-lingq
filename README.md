
# Auto Sync LingQ
Automatically get the words you've encountered in LingQ synced into Anki 2.1.

## Installing

### Manually

To install manually, download `sync_lingq.ankiaddon` from the [latest release](https://github.com/CiaranCurran/auto-sync-lingq/releases/latest/). You can then use Anki's `Tools` -> `Add-ons` -> `Install from file...` and select the `sync_link.ankiaddon` file to install this plugin.

### From the Anki Add-on Repository

In Anki, select `Tools` -> `Add-ons` -> `Get Add-ons` and then enter the code from the bottom of this addon's [Anki Add-On Repository page](https://ankiweb.net/shared/info/)

## Use

### Auto Sync LingQ

After installing the addon, you can now open the addons manager under the `Tools` -> `Add-ons` and access the main control pane by selecting the addon `Auto Sync LingQ` and then pressing the config button.

If it's your first time using the addon, `Auto Sync LingQ` will ask you to login.

After you've logged in, you can then select the languages you would like to have imported from the list of languages you are learning on LingQ. After you have selected you languages, a deck for each language will be created.

### TTS Support

`Auto Sync LingQ` is designed to work with the [AwesomeTTS Addon](https://ankiweb.net/shared/info/1436550454) see also [their GitHub](https://github.com/AwesomeTTS/awesometts-anki-addon).

The front of each card is wrapped with a `<tts preset=lingq-XX></tts>` tag. Where XX is the language code of the deck's language. See below to find the language code for a given language, or view them in the `Select Languages` pane from the addon's config. 
For TTS to work you will need to save a preset with the correct name using the AwesomeTTS Addon e.g. To get TTS to work for a Japanese deck, save a Japanese TTS voice preset in the AwesomeTTS plugin as `lingq-ja`

### Language Codes

Language | Code
------------ | -------------
Czech | cs
Norwegian | no
Turkish | tr
Finnish | fi
Hebrew | he
Romanian | ro
Dutch | nl
Greek | el
Polish | pl
Esperanto | eo
Latin | la
Danish | da
Ukrainian | uk
Slovak | sk
Malay | ms
Indonesian | id
Chinese (Traditional) | zh-t
Cantonese | hk
Gujarati | gu
Bulgarian | bg
Persian | fa
Belarusian | be
Arabic | ar
Serbian | srp
Croatian | hrv
Hungarian | hu
Catalan | ca
English | en
French | fr
German | de
Spanish | es
Italian | it
Japanese | ja
Korean | ko
Chinese | zh
Portuguese | pt
Russian | ru
Swedish | sv

#
## Etc.

### Improvements
See the [issues](https://github.com/JASchilz/AnkiSyncDuolingo/issues/) for the features I intend to add or fix. Feel free to add any issues you encounter.

### Acknowledgements
Much of this addon was inspired by [Joseph Schilz's](https://github.com/JAShilz/) [AnkiSyncDuolingo](https://github.com/JASchilz/AnkiSyncDuolingo). Without which, it would have taken considerably more effort to understand the anki source code and produce this addon.

### Getting Involved
Feel free to open pull requests or issues. [GitHub](https://github.com/CiaranCurran/auto-sync-lingq) is the canonical location of this project.

Here's the general sequence of events for code contribution:

1. Either:
    * Identify an existing issue in the [issue tracker](https://github.com/CiaranCurran/auto-sync-lingq/issues) and comment that you'd like to try to resolve it.
    * Open an issue in the [issue tracker](https://github.com/CiaranCurran/auto-sync-lingq).
2. Get acknowledgement/concurrence.
3. Submit a pull request to resolve the issue. Include documentation, if appropriate.
