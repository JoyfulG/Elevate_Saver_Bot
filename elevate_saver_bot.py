import telebot

import config

bot = telebot.TeleBot(config.tg_bot_token)


def send_message(message):
    bot.send_message(config.tg_user_id, message)
