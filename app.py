from flask import Flask

from migrate_tools.routes.employee import employees_routes
from migrate_tools.routes.database import database_routes

from migrate_tools.config.base_config import DockerDevelopmentConfig, LocalDevelopmentConfig, TestingConfig
from migrate_tools.mongodb.init_db import db

import os 

# create flask app 
app = Flask(__name__)
app.debug = True

if os.environ.get('FLASK_ENV') == 'docker_development':
    app.config.from_object(DockerDevelopmentConfig)
    app.config["MONGODB_SETTINGS"] = DockerDevelopmentConfig.MONGODB_SETTINGS
   
elif os.environ.get('FLASK_ENV') == 'local_development':
    app.config.from_object(LocalDevelopmentConfig)
    app.config["MONGODB_SETTINGS"] = LocalDevelopmentConfig.MONGODB_SETTINGS

else:
    app.config.from_object(TestingConfig)

db.init_app(app)

# employees routes 
app.register_blueprint(employees_routes, url_prefix='/')

if __name__ == "__main__":
    # run app
    app.run()
