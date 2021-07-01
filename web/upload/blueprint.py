from flask import Blueprint, render_template, request
from flask import redirect
from models import File
from forms import Upload_form
from werkzeug.utils import secure_filename
from app import db
from app import app

import os

upload = Blueprint('upload', __name__, template_folder = 'templates')

@upload.route('/', methods = ['POST', 'GET'])
def uploadFile():
	if request.method == 'POST':
		
		file = request.files['file']
		fileExtention = file.filename.split('.')
		secured_name = secure_filename(file.filename)

		print(file.filename, secured_name)

		fileBase = File(name = secured_name, extention = fileExtention[-1])

		try:
			db.session.add(fileBase)
			db.session.commit()

		except:
			return 'Upload error'

		file.save(os.path.join(app.config['UPLOAD_FOLDER'], secured_name))

		return redirect('/')

	form = Upload_form()
	return render_template('upload.html', form = form)