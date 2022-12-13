import unittest
from app import app
from models import QuestionModel,UserModel
import time
from flask_sqlalchemy import SQLAlchemy

db = None
class TestLogin(unittest.TestCase):

    def setUp(self):
        """在执行具体的测试方法前，先被调用"""

        # 激活测试标志
        app.testing = True
        user = 'root'
        password = '111111'
        database = 'test_qa'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)
        # 测试 数据库的修改
        db = SQLAlchemy()
        db.init_app(app)


        # 设置用来测试的数据库，避免使用正式数据库实例[覆盖原来项目中的数据库配置]

        # 设置数据库，测试之前需要创建好 create database testdb charset=utf8;
        # database = 'testdb'
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)
        # database = 'qa'

        # self.app = app

        # 创建数据库的所有模型表：Author、Book模型表
        # db.create_all()

    def tearDown(self):
        # 测试结束操作，删除数据库
        with app.app_context():
            db.session.remove()
        # db.drop_all()

    # 测试代码
    def test_append_data(self):
        au = UserModel(username='test',email = "1611503455@qq.com",password="111111")
        # question = QuestionModel(title="nihao",content="nihao",author=g.user,city=city,geolocation=geo)
        with app.app_context():
            db.session.add(au)
            db.session.commit()
            author =UserModel.query.filter_by(username='test').first()
        # book = Book.query.filter_by(info='python_book').first()
        # 断言数据存在
            self.assertIsNotNone(author)
        # self.assertIsNotNone(book)

        # 休眠10秒，可以到数据库中查询表进行确认
        time.sleep(10)


if __name__ == '__main__':
    unittest.main()

# import unittest
# from app import User, db, app
#
# class DataBaseTeset(unittest.TestCase):
#     """测试用户的数据库操作"""
#
#     def setUp(self):
#         app.testing = True
#         #    SQLALCHEMY_DATABASE_URI = "mysql://root:@127.0.0.1:3306/test"
#         # 测试 数据库的修改
#         app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1:3306/test"
#
#     def test_add_user(self):
#         user = User(**{
#             "name": "姓名4",
#             "email": '邮箱4'
#         })
#         db.session.add(user)
#         db.session.commit()
#
#         res = User.query.filter_by(name="姓名1").first()
#         self.assertIsNotNone(res)
#
#     def tearDown(self):
#         """在所有的测试执行后 执行，通过用来进行清理操作"""
#         db.session.remove()#删除数据，和连接状态
#         # db.drop_all() 删除数据库表，慎用