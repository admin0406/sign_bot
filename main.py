# *--conding:utf-8--*
import datetime
import sqlite3
import threading
from config import API_TOKEN, URL, ENV_FILE_PATH, CHECK_ORDER, TEST_CASE, WORK_PATH
import telebot
from telebot import types
from logger import Logger
import requests
import time
import join, re
import os

requests.adapters.DEFAULT_RETRIES = 5
r = requests.session()
r.keep_alive = False
bot = telebot.TeleBot(token=API_TOKEN)
logger = Logger().logger

PATH = os.getcwd()


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        callback_button_menu = types.InlineKeyboardButton(text="讲段子", callback_data="讲段子", )
        callback_button_song = types.InlineKeyboardButton(text='天气状况', callback_data='天气状况')
        # callback_button_news = types.InlineKeyboardButton(text='今日新闻', callback_data='今日新闻')
        callback_button_phones = types.InlineKeyboardButton(text='电话簿',
                                                            url='https://www.feituan.ph/index.php?cid=&ccid=9')
        # callback_button_cars = types.InlineKeyboardButton(text='日常修车', url='t.me/openporn')
        keyboard.add(callback_button_menu, callback_button_song, callback_button_phones, )
        msg_id = bot.send_message(message.chat.id, "欢迎使用自助机器人!", reply_markup=keyboard).message_id
        timer = threading.Timer(30, bot.delete_message, (message.chat.id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


# 进群欢迎信息
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def say_welcom(message):
    if message.new_chat_members:
        logger.info(message.new_chat_members)
        names = message.new_chat_members[0]
        msg_id = bot.send_message(message.chat.id, '欢迎 {} 加入群组🌺 کارب عزیز  🌺'.format(names.first_name)).message_id
        timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
        timer.start()


# 天气状况
@bot.callback_query_handler(func=lambda call: call.data == '天气状况')
def callback_menu(call):
    try:
        data = get_weather()
        logger.info(call.from_user)
        logger.info(call.data)
        callback_id = call.message.json['chat']['id']
        msg_id = bot.send_message(callback_id,
                                  "城市{} 温度:{} {} \n风向:{}{} 湿度:{} 时间:{}\n 60秒后自动删除！".format(data['address'],
                                                                                           data['temp'],
                                                                                           data['weather'],
                                                                                           data['windDirection'],
                                                                                           data['windPower'],
                                                                                           data['humidity'],
                                                                                           data[
                                                                                               'reportTime'])).message_id
        timer = threading.Timer(60, bot.delete_message, (callback_id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


# 文件类型
@bot.message_handler(content_types=['audio', 'document', 'gif', 'photo', 'sticker', 'video', 'voice',
                                    'game', 'video_note'])
def send_file_message(message):
    try:
        msg_id = bot.send_message(message.chat.id, '😅不好意思， 霸霸还不会处理文件内容，请多多指教😅😅').message_id
        bot.send_document(message.chat.id, message.document.file_id)
        logger.info(message.chat)
        timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


# 段子笑话
@bot.callback_query_handler(func=lambda call: call.data == '讲段子')
def callback_menu(call):
    try:
        logger.info(call.from_user)
        logger.info(call.data)
        callback_id = call.message.json['chat']['id']
        msg_id = bot.send_message(callback_id, get_joke()).message_id
        timer = threading.Timer(60, bot.delete_message, (callback_id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


# 新闻资讯
@bot.callback_query_handler(func=lambda call: call.data == '今日新闻')
def callback_menu(call):
    try:
        logger.info(call.from_user)
        logger.info(call.data)
        callback_id = call.message.json['chat']['id']
        msg_id = bot.send_message(callback_id,
                                  '今日推荐:{}，\n{}\n{} \n 60秒自动删除！'.format(get_news()['title'], get_news()['source'],
                                                                        get_news()['cover'])).message_id
        timer = threading.Timer(60, bot.delete_message, (callback_id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


# 查看个人信息
@bot.message_handler(commands=['my_id'])
def get_user_info(message):
    try:
        logger.info(message.chat)
        username = message.from_user.first_name if message.from_user.first_name else message.from_user.last_name
        if message.from_user.username:
            msg_id = bot.send_message(message.chat.id,
                                      "亲爱的❤️{}  ❤️你好\n你的 Chat_Id = {}\nUsername是 {} \n  5秒后自动删除！".format(username,
                                                                                                         message.from_user.id,
                                                                                                         message.from_user.username)).message_id
            timer = threading.Timer(5, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
        else:
            msg_id = bot.send_message(message.chat.id,
                                      "亲爱的 {} 你好\n你的 Chat_Id是 = {}\nUsername 还没设置 \n  5秒后自动删除！".format(
                                          message.from_user.first_name,
                                          message.from_user.id)).message_id
            timer = threading.Timer(5, bot.delete_message, (message.chat.id, msg_id))
            timer.start()

    except Exception as e:
        logger.error(e)


# 获取游戏帮助
@bot.message_handler(commands=['game_help'])
def get_help(message):
    try:
        logger.info(message.chat)
        if message.chat.type == 'private':
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id,
                             "/join_lottery - 加入抽奖\n/list_lottery- 查看名单\n/lottery - 抽奖[admin]\n/clear_game_list - 清空名单[admin]\n")
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            msg_id = bot.send_message(message.chat.id,
                                      "/join_lottery - 加入抽奖\n/list_lottery- 查看名单\n/lottery - 抽奖[admin]\n/clear_game_list - 清空名单[admin]\n").message_id
            timer = threading.Timer(30, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 加入抽奖
@bot.message_handler(commands=['join_lottery'])
def join_lottery(message):
    try:
        logger.info(message.chat)
        if message.chat.type == 'private':
            un = message.from_user.username
            r = join.add_in(un)
            bot.reply_to(message, r)
        else:
            un = message.from_user.username
            r = join.add_in(un)
            msg_id = bot.reply_to(message, r).message_id
            timer = threading.Timer(15, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 查看抽奖名单
@bot.message_handler(commands=['list_lottery'])
def send_list(message):
    try:
        logger.info(message.chat)
        if message.chat.type == 'private':
            un = message.from_user.username
            bot.send_chat_action(message.chat.id, 'typing')
            r = join.read_list(un)
            count = -1
            for count, line in enumerate(open("list", 'r')):
                pass
            count += 1
            rr = u'%s \n\n 目前共有%s人参与抽奖哦' % (r, count)
            msg_id = bot.reply_to(message, rr).message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()

        else:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton('戳这里！', url='https://t.me/Bibo_dear_bot')
            markup.add(btn)
            msg_id = bot.send_message(chat_id=message.chat.id, text=u'为了防止刷屏，请在私聊中使用此命令哦～',
                                      reply_markup=markup).message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 抽奖
@bot.message_handler(commands=['lottery'])
def execution_lottery(message):
    try:
        un = message.from_user.username
        logger.info(message.chat)
        f = open('adminlist', 'r')
        l = f.read()
        if l.find('%s' % un) == -1:
            msg_id = bot.reply_to(message, '您没有权限哦').message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
        else:
            code, r = join.get_lottery()
            bot.reply_to(message, r)
    except Exception as e:
        logger.error(e)


# 清空名单
@bot.message_handler(commands=['clear_game_list'])
def del_lottery_list(message):
    try:
        un = message.from_user.username
        logger.info(message.chat)
        f = open('adminlist', 'r')
        l = f.read()
        if message.chat.type == 'private':
            if l.find('%s' % un) == -1:
                bot.reply_to(message, '您没有权限哦')
            else:
                r = join.del_list()
                bot.reply_to(message, r)
        else:
            if l.find('%s' % un) == -1:
                msg_id = bot.reply_to(message, '您没有权限哦').message_id
                timer = threading.Timer(5, bot.delete_message, (message.chat.id, msg_id))
                timer.start()
            else:
                r = join.del_list()
                msg_id = bot.reply_to(message, r).message_id
                timer = threading.Timer(5, bot.delete_message, (message.chat.id, msg_id))
                timer.start()
    except Exception as e:
        logger.error(e)


# 执行测试用例
@bot.message_handler(regexp='execution_case_(.*)_over')
def execution_test_case(message):
    try:
        logger.info(message.chat)
        un = message.from_user.username
        with open('adminlist', 'r')as f:
            l = f.read()
        if un and l.find(un) == 0:
            environment = re.search('execution_case_(.*)_over', message.text).group(1)
            if '_' in environment:
                en = environment.split('_')[0]
                with open(ENV_FILE_PATH, 'a', encoding='utf-8')as f:
                    f.write('|'.join(environment.split('_')))
                    f.write('\r')
            else:
                en = environment
                with open(ENV_FILE_PATH, 'a', encoding='utf-8')as f:
                    f.write(''.join(environment))
                    f.write('\r')
            id = bot.send_message(message.chat.id, '霸霸正在拼命执行{}的所以测试用例，请稍等片刻...😅😅...'.format(en)).message_id
            timer1 = threading.Timer(300, bot.delete_message, (message.chat.id, id))
            timer1.start()
            os.chdir(WORK_PATH)
            os.system('python3 run_api_case.py')
            # 再推送到群里
            time.sleep(10)
            with open('{}/{}'.format(TEST_CASE['case_result_file_path'], TEST_CASE['case_result_file_name']), 'rb')as f:
                msg_id = bot.send_document(message.chat.id, data=f).message_id
            os.chdir(PATH)
            timer = threading.Timer(300, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
        else:
            msg_id = bot.reply_to(message, '您没有权限哦😂').message_id
            timer = threading.Timer(5, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 查看是否漏单
@bot.message_handler(commands=['cat_check_order_log'])
def check_order_log(message):
    try:
        logger.info(message.chat)
        with open('{}/{}'.format(CHECK_ORDER['log_path'], CHECK_ORDER['log_name']), 'rb')as f:
            msg_id = bot.send_document(message.chat.id, data=f).message_id
            timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


def creat_table():
    """创建表"""
    conncet = sqlite3.connect('telegram_user')
    curs = conncet.cursor()
    curs.execute(
        "create table User_sign(id integer PRIMARY KEY AUTOINCREMENT,user_name varchar(255),chat_id int(11),is_sign int (1) default 1,time TIMESTAMP default (datetime('now','localtime')))")

    curs.close()
    conncet.close()


# 插入数据库签到表
def insert_sign(telegram_user_name, chat_id):
    sql = "insert into User_sign(user_name,chat_id) values ('{}','{}');".format(
        telegram_user_name, chat_id)
    conn = sqlite3.connect('telegram_user')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        return cur.rowcount
    except:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# 查询累计签到
def search_signs(chat_id):
    sql = "SELECT COUNT(1) from User_sign WHERE chat_id =='{}';".format(chat_id)
    conn = sqlite3.connect('telegram_user')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchone()[0]
    except:
        pass
    finally:
        cur.close()
        conn.close()


# 查询最后一次签到的时间
def search_last_sign_time(chat_id):
    sql = "SELECT time from User_sign WHERE chat_id ='{}' order by  id desc limit 1;".format(chat_id)
    conn = sqlite3.connect('telegram_user')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchone()[0]
    except:
        pass
    finally:
        cur.close()
        conn.close()


@bot.message_handler(commands=['sign'])
def user_sign(message):
    logger.info(message.chat)
    try:
        username = message.from_user.first_name if message.from_user.first_name else message.from_user.last_name
        chat_id = message.from_user.id
        t = str(datetime.datetime.today()).split(' ')[0]
        t1 = search_last_sign_time(chat_id)
        if t1 and t == str(t1).split(' ')[0]:
            msg_id = bot.reply_to(message, '今日已签到,签到时间为:{} 请明天再来！20秒自毁以启动'.format(t1)).message_id
            timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
        else:
            insert_sign(username, chat_id)
            msg_id = bot.reply_to(message, '亲爱的 {} 恭喜你签到成功! 20秒自毁以启动'.format(username)).message_id
            timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


@bot.message_handler(commands=['mystats'])
def user_status(message):
    try:
        logger.info(message.chat)
        username = message.from_user.first_name if message.from_user.first_name else message.from_user.last_name
        chat_id = message.from_user.id
        num = search_signs(chat_id)
        msg_id = bot.reply_to(message, '{}:您总共签到:{} 次，很棒棒额，请再接再厉，20秒自毁以启动'.format(username, num)).message_id
        timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


def get_news():
    res = r.get(URL['news_list'])
    if res.status_code == 200:
        news_Id = res.json()['data'][0]['newsId']
        news_url = URL['news_details'] + '?newsId=' + news_Id
        res = r.get(news_url)
        return res.json()['data']


def get_joke():
    res = r.get(URL['joke_url'])
    if res.status_code == 200:
        return res.json()['data'][0]['content']


def get_weather():
    res = r.get(URL['weather_url']).json()
    return res['data']


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
