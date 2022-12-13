import logging

# system log
file = logging.FileHandler(filename='./logs/operation_log.log', mode='a', encoding='utf-8')
fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
file.setFormatter(fmt)

# 定义日志
logger1 = logging.Logger(name='operation log')
logger1.addHandler(file)
# logger1.removeHandler(file)

# 写日志
# logger1.error(msg='这里是msg111')
# logger1.log(msg='这里是msg222', level=50)

