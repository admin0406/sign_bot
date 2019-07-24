from logging.handlers import TimedRotatingFileHandler
import datetime
import logging,os
import config

LOG_PATH = os.path.abspath(os.getcwd())

class Logger(object):
    def __init__(self, logger_name='telegram_bot.log'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        # 引入配置文件log
        c = config.LOG
        # 拼接使用当前时间为日志名
        log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        # 日志文件名
        self.log_file_name = c['file_name'] if c and c['file_name'] else LOG_PATH + '\\' + log_file  # 日志名
        self.backup_count = c['backup'] if c and c['backup'] else 5  # 保留日志数量
        # 日志输出级别
        self.console_output_level = c['console_level'] if c and c['console_level'] else 'WARNING'
        self.file_output_level = c['file_level'] if c and c['file_level'] else 'DEBUG'
        # 日志输出格式
        self.formatter = c['pattern'] if c and c['pattern'] else logging.Formatter(
            '%(asctime)s -- %(name)s -- %(filename)s -- %(lineno)d -- %(levelname)s -- %(message)s')

    def get_logger(self):
        '''在logger添加日志句柄并返回,如果logger已有句柄,则直接返回'''
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志,最多保留self.backup_count 份
            file_handler = TimedRotatingFileHandler(filename=self.log_file_name,
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


# 调用logger即可写入日志
logger = Logger().get_logger()
if __name__ == '__main__':
    log = Logger()
    log.logger.info('dkjfa 急啊卡收费道具')
