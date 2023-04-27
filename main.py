from argparse import ArgumentParser

import telebot

from src.commands import Commands


def main():
    parser = ArgumentParser()
    parser.add_argument('token', type=str, metavar='<token for bot>')
    args = parser.parse_args()

    bot = telebot.TeleBot(args.token, parse_mode=None)
    comm = Commands(bot)
    # comm.load_from_db()

    bot.register_message_handler(comm.add_lesson, commands=['add_lesson'])
    bot.register_message_handler(comm.add_word, commands=['add_word'])
    bot.register_message_handler(comm.list_lesson, commands=['list_lesson'])
    bot.register_message_handler(comm.start_lesson, commands=['start_lesson'])
    bot.register_message_handler(comm.text_command, content_types=['text'])
    # bot.register_message_handler(planer.update_plan, commands=['result', 'add', 'delete', 'comment', 'order', 'fail'])
    # bot.register_message_handler(planer.authentication_user, commands=['saveme'])
    # bot.register_message_handler(planer.set_name, commands=['name'])

    bot.infinity_polling()


if __name__ == '__main__':
    main()
