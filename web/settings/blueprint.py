from flask import Blueprint
from flask import render_template
from .forms import style
from flask import request
from flask import url_for
import os
from models import user
from flask import redirect
from app import db

settings = Blueprint('settings', __name__, template_folder = 'templates')

@settings.route('/', methods = ['POST', 'GET'])
def index():
	name = request.cookies.get('user')
	if name:
		form = style()

		if request.method == 'GET':
			for i in user.query.all():
				if i.login == name:
					if i.custom_style == 'yes':
						return render_template('settings.html', form = form, core = 'upload/{}/core.css'.format(name), menu = 'upload/{}/menu.css'.format(name))

			return render_template('settings.html', form = form, core = 'css/core.css', menu = 'css/menu.css')

		if request.method == 'POST':
			file = request.files['stylesheet']
			path = 'static/upload/{}'.format(name)

			try:
				file.save(dst = '{}/{}'.format(path, file.filename))

			except FileNotFoundError as e:
				os.mkdir(path)
				usr = user.query.all()
				for i in user.query.all():
					if i.login == name:
						i.custom_style = 'yes'
						print (i)
						db.session.add(i)
						db.session.commit()
				file.save(dst = '{}/{}'.format(path, file.filename))

			return render_template('settings.html', form = form, core = 'upload/{}/core.css'.format(name), menu = 'upload/{}/menu.css'.format(name))

	return redirect('/verify')