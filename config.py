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