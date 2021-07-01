from flask import Blueprint
from flask import render_template
from flask import request 
from flask import redirect
from models import group_
from .forms import addGroup
from app import db
from models import user

groupCreate = Blueprint('groupCreate', __name__, template_folder = 'templates')

@groupCreate.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == 'POST':
		name = request.form['name']

		try:
			mesg = group_(name = name, users = '', slug = '')
			db.session.add(mesg)
			db.session.commit()
			return redirect('/')

		except:
			print('error')

	form = addGroup()

	return render_template('groupCreate.html', form = form)