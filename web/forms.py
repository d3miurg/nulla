from wtforms import Form
from wtforms import TextAreaField
from wtforms import StringField

class MessageForm(Form):
	message = TextAreaField('Сообщение')
	user = StringField('Имя')