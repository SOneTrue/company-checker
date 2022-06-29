from tgbot.filters.settings_buttons import ListOfButtons

start_exit = ListOfButtons(text=['Начать раб. день'],
                           callback=['exit'],
                           align=[1]).inline_keyboard

start_close = ListOfButtons(text=['Закончить раб. день'],
                            callback=['close'],
                            align=[1]).inline_keyboard
