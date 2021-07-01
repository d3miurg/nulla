from app    import app
from app import db
from flask  import request
from flask  import render_template
from flask import url_for
from flask import Response
from flask import redirect
from forms import MessageForm
from models import Message

@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'GET':
		form = MessageForm()
		return render_template('main.html', form = form)

	elif request.method == 'POST':
		pass

@app.errorhandler(404)
def page_not_found(e):
	return 'Тут есть только одна страница', 404