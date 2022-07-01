from tgbot.filters.settings_buttons import ListOfButtons

start_exit = ListOfButtons(text=['Начать день!'],
                           callback=['exit'],
                           align=[1]).inline_keyboard

start_close = ListOfButtons(text=['Закончить день!'],
                            callback=['close'],
                            align=[1]).inline_keyboard
