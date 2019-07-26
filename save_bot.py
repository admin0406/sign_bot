# *--conding:utf-8--*
import telebot
from config import API_TOKEN
from data_comming import *

bot = telebot.TeleBot(API_TOKEN)


def get_username(message):
    if message.from_user.username:
        return message.from_user.username
    else:
        return ''


def get_nickname(message):
    frist_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if frist_name and last_name and frist_name != last_name:
        username = frist_name + last_name
    else:
        username = frist_name
    return username


# 存储数据库
@bot.message_handler(func=lambda message: True)
def save_message_to_sql(message):
    try:
        save_text_to_sql(nick_name=get_nickname(message), chat_id=message.from_user.id, new_chat_member='0',
                         left_chat_member='0', text=message.text, other='0')
    except:
        pass


# 文件类型
@bot.message_handler(content_types=['audio', 'document', 'gif', 'photo', 'sticker', 'video', 'voice',
                                    'game', 'video_note'])
def send_file_message(message):
    try:
        save_text_to_sql(nick_name=get_nickname(message), chat_id=message.from_user.id, other='1')
    except:
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
