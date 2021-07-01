from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField

class checkUser(Form):
	login = StringField('Имя')
	password = PasswordField('Пароль')