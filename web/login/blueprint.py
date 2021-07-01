from flask import Blueprint
from flask import render_template
from models import user
from flask import make_response
from flask import request
from flask import redirect
from .forms import checkUser

login = Blueprint('login', __name__, template_folder = 'templates')

@login.route('/')
def index():
	form = checkUser()
	msg = ''

	login = request.args.get('login', '')
	password = request.args.get('password')

	users = user.query.all()
	
	if login == '':
		return render_template('login.html', err = msg, form = form)
	for i in users:
		if i.login == login:
			if i.password == password:
				res = make_response(redirect('/'))
				res.set_cookie('user', login)
				return res

			else:
				msg = 'Неверный пароль'
				break

		else:
			msg = 'Данного пользователя не существует'
			break

	return render_template('login.html', err = msg, form = form)