# !/usr/bin/env python
import os
import subprocess
import typer

from models import Role, User
from config import Config
from utils.dep import redis_conn, redis_q, db
from rq import Worker, Connection
from main import create_app

manager = typer.Typer()


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')


@app.cli.command("shell_context")
def make_shell_context():
    return dict(app=app, User=User, Role=Role)





@manager.command()
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def create_tables():
    db.create_all()


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command()
def create_tables():
    with app.app_context():
        db.create_all()


@manager.command()
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    with app.app_context():
        db.drop_all()
        db.configure_mappers()
        db.create_all()
        db.session.commit()


@manager.command()
def runserver():
    app.run()


@manager.command()
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command()
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()




def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    with app.app_context():
        Role.insert_roles()
        admin_query = Role.query.filter_by(name='Administrator').first()
        if admin_query:
            if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
                user = User(
                    first_name='John',
                    last_name='Doe',
                    username='admin',
                    role=admin_query,
                    area_code=Config.ADMIN_AREA_CODE,
                    password=Config.ADMIN_PASSWORD,
                    confirmed=True,
                    email=Config.ADMIN_EMAIL)
                db.session.add(user)
                db.session.commit()
                print('Added administrator {}'.format(user.full_name))
            else:
                raise Exception('Object already exists')


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


@manager.command()
def run_worker():
    """Initializes a slim rq task queue."""
    with Connection(redis_conn):
        worker = Worker(redis_q)
        worker.work()


if __name__ == '__main__':
    manager()







