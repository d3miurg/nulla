from flask import Blueprint, render_template, redirect, request
from models import user

news = Blueprint('news', __name__, template_folder = 'templates')

@news.route('/')
def index():
	name = request.cookies.get('user')
	if name:
		for i in user.query.all():
				if i.login == name:
					if i.custom_style == 'yes':
						return render_template('news.html', news = 'upload/{}/news.css'.format(name), menu = 'upload/{}/menu.css'.format(name), core = 'upload/{}/core.css'.format(name))
	
		return render_template('news.html', news = 'css/news.css', menu = 'css/menu.css', core = 'css/core.css')

	else:
		return redirect('/verify/')		