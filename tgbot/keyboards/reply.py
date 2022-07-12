from tgbot.filters.settings_buttons import ListOfButtons

start_default = ListOfButtons(text=['Send'],
                              callback=['sender'],
                              align=[1]).reply_keyboard

answer = ListOfButtons(text=['Верно'],
                       callback=['good'],
                       align=[1]).reply_keyboard

answer_day = ListOfButtons(text=['Нет'],
                           callback=['no'],
                           align=[1]).reply_keyboard

number_auto_key = ListOfButtons(text=['562', '459', '176', '481', '293', '793', '044', '771', '522', '858', '949'],
                            callback=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
                            align=[5, 5, 1]).reply_keyboard
