from os import getenv
from threading import Event as ThreadEvent

from flask import Flask
from flask import redirect, url_for

from routes.dashboard import bp as dashboard_bp
from routes.user import bp as user_bp
from dotenv import load_dotenv

from flask_login import LoginManager

from flask_migrate import Migrate

from models.connection import db
from models.user import User

import click

load_dotenv()


app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

app.config['SQLALCHEMY_DATABASE_URI'] = getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
if getenv("SECRET_KEY") == None:
    print("SECRET_KEY variable is not set.")
    exit()
else:
    app.config['SECRET_KEY'] = getenv("SECRET_KEY")
    # app.config['JWT_SECRET_KEY'] = getenv("SECRET_KEY")


# jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user

db.init_app(app)
migrate = Migrate(app, db)

@app.cli.command("create_user")
@click.option('--username', prompt='Username', required=True)
@click.option('--password', prompt='User password', required=True)
def create_user(username, password):
    from models.user import User

    user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
    if (user == None):
        new_user = User()
        new_user.username = username
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
    else:
        print("User already exist")

@app.cli.command("delete_user")
@click.option('--username', prompt='Username', required=True)
def delete_user(username):
    user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
    if (user != None):
        db.session.delete(user)
        db.session.commit()
    else:
        print("User don't exist")


@app.route("/")
def web_root():
    return redirect(url_for("dashboard.dashboard"))

if __name__ == "__main__":
    app.run(app)