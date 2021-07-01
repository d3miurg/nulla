from wtforms import Form
from wtforms import FileField

class style(Form):
	stylesheet = FileField('Файл стилей')
