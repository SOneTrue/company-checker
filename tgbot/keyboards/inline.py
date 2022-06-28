from tgbot.filters.settings_buttons import ListOfButtons

start_exit = ListOfButtons(text=['Начать раб. день'],
                           callback=['exit'],
                           align=[1]).inline_keyboard

start_close = ListOfButtons(text=['Закончить раб. день'],
                            callback=['close'],
                            align=[1]).inline_keyboard

answer_q1 = ListOfButtons(text=['Верно', 'Комментарий'],
                          callback=['good_1', 'comment_1'],
                          align=[2]).inline_keyboard

answer_q2 = ListOfButtons(text=['Верно', 'Комментарий'],
                          callback=['good_2', 'comment_2'],
                          align=[2]).inline_keyboard
