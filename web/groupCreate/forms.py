from wtforms import Form
from wtforms import TextAreaField

class addGroup(Form):
	name = TextAreaField('Название')