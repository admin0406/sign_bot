# *--conding:utf-8--*
import os
API_TOKEN = '837140525:AAERnzRfG9-Th1kz-3dsYaQ40cMXb5c8crQ'
AUTO_PATH = os.path.abspath(os.path.join(os.getcwd(),'../Auto_Test/'))
black_path = 'black_list'
admin_path = 'admin_list'

# 测试用例路径
WORK_PATH = os.path.join(AUTO_PATH,'main')
# 日志配置

LOG = {
    'file_name': 'telegram_bot.log',
    'backup': 5,
    'console_level': 'INFO',
    'file_level': 'DEBUG',
    'pattern': ''
}

# 三方api接入
URL = {
    # 笑话
    'joke_url': 'http://www.mxnzp.com/api/jokes/list/random',
    # 笑话大全（备用）
    'joke_url1':'https://api.jisuapi.com/xiaohua/text?pagenum=1&pagesize=1&sort=rand&appkey=c716da946813f180',
    # 新闻
    'news_list': 'http://www.mxnzp.com/api/news/list?typeId=525&page=1',
    # 请求新闻
    'news_details': 'http://www.mxnzp.com/api/news/details',
    # 天气
    'weather_url': 'http://www.mxnzp.com/api/weather/current/深圳市',
    # 手机号查询
    'phone_url':'http://api.guaqb.cn/api.php?sj=手机号',
    # 苹果手机序列号查询
    'iphone_key':'http://api.guaqb.cn/api.php?ios=序列号(如dnrpkbwbg5md)',
    # 身份证查询
    'id_card_search':'http://api.guaqb.cn/music/id/card.php?id= 15或18位身份证号',
    # 汇率
    'exchange':'https://api.jisuapi.com/exchange/convert?appkey=c716da946813f180&from=CNY&to=php&amount=10',

}

# 测试用例结果路径
TEST_CASE = {'case_result_file_path':os.path.join(AUTO_PATH,'report'),
             'case_result_file_name': 'api_report.html'
             }

CHECK_ORDER = {'log_path': os.path.join(AUTO_PATH,'..'),
               'log_name': '拉取注单.log'}

# 写入参数的文件路径
ENV_FILE_PATH = os.path.join(AUTO_PATH,'env_file')
