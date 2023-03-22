from config import conf
import logging


class Logger:
    def __init__(self,
                 log_file,
                 level=logging.DEBUG,
                 extra_info=""):
        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(level)
        self.extra_info = extra_info
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s: %(message)s')

        file_log = logging.FileHandler(log_file, encoding='utf-8')
        file_log.setFormatter(formatter)
        self.logger.addHandler(file_log)

    def debug(self, message):
        if self.extra_info != "":
            message = self.extra_info + "" + message
        self.logger.debug(message)

    def info(self, message):
        if self.extra_info != "":
            message = self.extra_info + "" + message
        self.logger.info(message)

    def warning(self, message):
        if self.extra_info != "":
            message = self.extra_info + "" + message
        self.logger.warn(message)

    def error(self, message):
        if self.extra_info != "":
            message = self.extra_info + "" + message
        self.logger.error(message)


log = Logger(log_file=conf.log_file, level=logging.DEBUG, extra_info=f"[{conf.account} & {conf.user_email}]")