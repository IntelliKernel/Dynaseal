import logging
import os
import datetime

# 获取当前文件夹名称
path = os.path.dirname(__file__)

# 创建一个logger
logger = logging.getLogger(path)
logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG

# 创建一个handler，用于写入日志文件, 日志文件名为 时间.log
now = datetime.datetime.now()
log_file = 'logs/' + now.strftime('%Y-%m-%d-%H-%M-%S') + '.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# 再创建一个handler，用于将日志输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(file_handler)
logger.addHandler(console_handler)

if __name__ == '__main__':
    # 记录一条日志
    logger.debug('This is a debug message')
