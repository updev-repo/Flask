from apps import create_app
from apps.api.routes import api
from apps.auth.routes import auth
from apps.account.routes import account
from flask_login import LoginManager

from config.login import login_manager

if __name__ == "__main__":
    app = create_app()

    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(account)

    login_manager.init_app(app)

    app.run(debug=True, port=8000)
