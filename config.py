# *--conding:utf-8--*
import os
API_TOKEN = '837140525:AAERnzRfG9-Th1kz-3dsYaQ40cMXb5c8crQ'
AUTO_PATH = os.path.abspath(os.path.join(os.getcwd(),'../Auto_Test/'))

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
    # 新闻
    'news_list': 'http://www.mxnzp.com/api/news/list?typeId=525&page=1',
    # 请求新闻
    'news_details': 'http://www.mxnzp.com/api/news/details',
    # 天气
    'weather_url': 'http://www.mxnzp.com/api/weather/current/深圳市'
}

# 测试用例结果路径
TEST_CASE = {'case_result_file_path':os.path.join(AUTO_PATH,'report'),
             'case_result_file_name': 'api_report.html'
             }

CHECK_ORDER = {'log_path': os.path.join(AUTO_PATH,'..'),
               'log_name': '拉取注单.log'}

# 写入参数的文件路径
ENV_FILE_PATH = os.path.join(AUTO_PATH,'env_file')
