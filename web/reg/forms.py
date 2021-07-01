from wtforms import Form
from wtforms import StringField

class newUser(Form):
	login = StringField('Имя')
	password = StringField('Пароль')