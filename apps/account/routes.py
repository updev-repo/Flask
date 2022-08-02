from flask import Blueprint, render_template
from flask_login import login_required

account = Blueprint("account", __name__, url_prefix="/account", template_folder="./templates")


@account.route("/")
@login_required
def account_page():
    return render_template("account.html")
