from tgbot.filters.settings_buttons import ListOfButtons

start_default = ListOfButtons(text=['Send'],
                              callback=['sender'],
                              align=[1]).reply_keyboard
