from tgbot.filters.settings_buttons import ListOfButtons

accept_keyboard = ListOfButtons(text=['Принять', 'Отказать'],
                                callback=['accept', 'cancel'],
                                align=[2]).inline_keyboard
