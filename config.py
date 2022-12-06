# database config information
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'qa'
USERNAME = 'root'
PASSWORD = '111111'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "sdfsadfskrwerfj1233453345"

# config of emial
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "386018442@qq.com"
MAIL_PASSWORD = "zjkrfexeplecbggi"
MAIL_DEFAULT_SENDER = "386018442@qq.com"

# config of log
from logging.config import dictConfig

dictConfig({
        "version": 1,
        "disable_existing_loggers": False,  # 不覆盖默认配置
        "formatters": {  # 日志输出样式
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",  # 控制台输出
                "level": "DEBUG",
                "formatter": "default",
            },
            "log_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "default",   # 日志输出样式对应formatters
                "filename": "./logs/flask.log",  # 指定log文件目录
                "maxBytes": 20*1024*1024,   # 文件最大20M
                "backupCount": 10,          # 最多10个文件
                "encoding": "utf8",         # 文件编码
            },

        },
        "root": {
            "level": "DEBUG",  # # handler中的level会覆盖掉这里的level
            "handlers": ["console", "log_file"],
        },
    }
)
