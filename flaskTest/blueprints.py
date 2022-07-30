from app import app
from views import post_bp, bp
from endpoints import api_bp, run

app.register_blueprint(bp)
app.register_blueprint(post_bp)
app.register_blueprint(api_bp)
app.add_url_rule('/', endpoint='index')

