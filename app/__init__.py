import os
from flask import Flask

# create and configure the app
def create_app(test_config=None):
    # creates a Flask instance
    app = Flask(__name__, instance_relative_config=True)
    
    # default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)
    app.add_url_rule('/', endpoint='index')

    from . import userView
    app.register_blueprint(userView.bp)

    from . import modifyUser
    app.register_blueprint(modifyUser.bp)

    from . import proyectView
    app.register_blueprint(proyectView.bp)

    from . import modifyProyect
    app.register_blueprint(modifyProyect.bp)

    from . import logger
    app.register_blueprint(logger.bp)

    from . import clientView
    app.register_blueprint(clientView.bp)

    from . import department
    app.register_blueprint(department.bp)

    from . import metricsView
    app.register_blueprint(metricsView.bp)
    
    return app