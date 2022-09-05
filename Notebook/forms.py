import re

from passlib.handlers.sha2_crypt import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_wtf import FlaskForm
from mysql_util import MysqlUtil


# Register Form Class
class LoginForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=2, max=25, message='长度在4-25个字符之间')
        ]
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, max=20, message='长度在6-20个字符之间'),
        ]
    )

    def validate_username(self, field):
        username = field.data
        pattern = re.compile("^[\u4e00-\u9fa5a-zA-Z0-9]{4,25}$")
        error = ""
        if not pattern.match(username):
            error = "用户名格式不对，请输入4-25位中文，大小写字母，下划线的用户名"
        sql = "SELECT * FROM users  WHERE username = '%s'" % (field.data)  # 根据用户名查找user表中记录
        db = MysqlUtil()  # 实例化数据库操作类
        result = db.fetchone(sql)  # 获取一条记录
        if not result:
            error = "用户未注册，请注册"
        if error:
            raise ValidationError(error)

    def validate_password(self, field):
        password = field.data
        pattern = re.compile("^[a-zA-Z]\w{5,19}$")
        if not pattern.match(password):
            raise ValidationError("密码格式错误，正确格式为：以字母开头，长度在6~20之间，只能包含字符、数字和下划线")

    def Valid_user(self, username, password):
        sql = "SELECT * FROM users  WHERE username = '%s'" % (username)  # 根据用户名查找user表中记录
        db = MysqlUtil()  # 实例化数据库操作类
        result = db.fetchone(sql)  # 获取一条记录
        password_database = result['password']  # 用户填写的密码
        return sha256_crypt.verify(password, password_database)


class RegisterForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(min=2, max=25, message='长度在4-25个字符之间')
        ]
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, max=20, message='长度在6-20个字符之间'),
        ]
    )
    confirm = PasswordField(
        '确认密码',
        validators=[
            DataRequired(message='请输入相同密码'),
            Length(min=6, max=20, message='长度在6-20个字符之间'),
        ]
    )
    email = StringField(
        '邮箱地址',
        validators=[
            DataRequired(message="请输入邮箱，必填"),
            Email()
        ]
    )

    def validate_username(self, field):
        username = field.data
        pattern = re.compile("^[\u4e00-\u9fa5a-zA-Z0-9]{4,25}$")
        error = ""
        if not pattern.match(username):
            error = "用户名格式不对，请输入4-25位中文，大小写字母，下划线的用户名"
        sql = "SELECT * FROM users  WHERE username = '%s'" % (field.data)  # 根据用户名查找user表中记录
        db = MysqlUtil()  # 实例化数据库操作类
        result = db.fetchone(sql)  # 获取一条记录
        if result:
            error = "用户已注册，请登录"
        if error:
            raise ValidationError(error)

    def validate_password(self, field):
        password = field.data
        pattern = re.compile("^[a-zA-Z]\w{5,19}$")
        if not pattern.match(password):
            raise ValidationError("密码格式错误，正确格式为：以字母开头，长度在6~20之间，只能包含字符、数字和下划线")

    def validate_confirm(self, field):
        password = field.data
        pattern = re.compile("^[a-zA-Z]\w{5,19}$")
        if not pattern.match(password):
            raise ValidationError("密码格式错误，正确格式为：以字母开头，长度在6~20之间，只能包含字符、数字和下划线")


    def Valid_register(self, username, password_candidate, password_confirm, email):
        print(password_confirm,password_candidate)
        if password_candidate != password_confirm:
            return False
        else:
            return True


# Article Form Class
class ArticleForm(Form):
    title = StringField(
        '标题',
        validators=[
            DataRequired(message='长度在2-30个字符'),
            Length(min=2, max=30)
        ]
    )
    content = TextAreaField(
        '内容',
        validators=[
            DataRequired(message='长度不少于5个字符'),
            Length(min=5)
        ]
    )
