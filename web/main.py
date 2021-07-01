from app import app
import view

#from about.blueprint import about
#from groupCreate.blueprint import groupCreate
#from login.blueprint import login
#from reg.blueprint import reg
#from settings.blueprint import settings

#app.register_blueprint(about, url_prefix = '/about')
#app.register_blueprint(groupCreate, url_prefix = '/new_group')
#app.register_blueprint(login, url_prefix = '/login')
#app.register_blueprint(reg, url_prefix = '/reg')
#app.register_blueprint(settings, url_prefix = '/settings')

if __name__ == '__main__':
	app.run()