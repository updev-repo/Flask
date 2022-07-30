from app import app
from flask import jsonify, request, Blueprint
from database import Posts, Users, db
from flask_restful import Resource, Api

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(app)


@api_bp.route('/users', methods = ['GET', 'POST'])
def user_list():
    queryset = Users.query.all()
    user_data = []
    if (request.method == 'GET'):
        for obj in queryset:
            data = {
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                }

            user_data.append(data)       
        return jsonify({'data': user_data})


@api_bp.route('/posts', methods = ['GET', 'POST'])
def get_posts():
    queryset = Posts.query.all()
    posts_data = []
    if (request.method == 'GET'):
        for obj in queryset:
            data = {
                'id': obj.id,
                'title': obj.title,
                'body': obj.body,
                'time': obj.time.strftime("%b %d %Y, %I:%M %p")
            }
            posts_data.append(data)       
        return jsonify({'data': posts_data})




def run():
    api.add_resource()