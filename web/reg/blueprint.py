from flask import Blueprint, render_template
from models import user
from app import db
from flask import request
from flask import make_response
from flask import redirect
from .forms import newUser

reg = Blueprint('reg', __name__, template_folder = 'templates')

@reg.route('/', methods = ['POST', 'GET'])
def index():

	form = newUser()

	if request.method == 'POST':
		login = request.form['login']
		password = request.form['password']

		if login == '':
			return render_template('reg.html', err = 'Введите имя пользователя', form = form)

		elif password == '':
			return render_template('reg.html', err = 'Введите пароль', form = form)

		else:
			try:
				usr = user(login = login, password = password, customStyle = 0x00)
				print(usr)
				db.session.add(usr)
				db.session.commit()

			except:
				return render_template('reg.html', err = 'Ошибка сервера', form = form)

			res = make_response(redirect('/'))
			res.set_cookie('user', login)
			return res

	return render_template('reg.html', form = form)
