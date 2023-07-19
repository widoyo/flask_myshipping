from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse
import sqlite3
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_peewee.db import Database
import flask_wtf as fw
import wtforms as wt
from flask_wtf import FlaskForm
from app.models import db_wrapper, User

login_manager = LoginManager()

SECRET_KEY = 'hello'
DATABASE = {
    'name': 'myshipping.db',
    'engine': 'peewee.SqliteDatabase'
    }

class LoginForm(fw.FlaskForm):
    username = wt.StringField('Username', validators=[wt.validators.DataRequired()])
    password = wt.PasswordField('Password', validators=[wt.validators.DataRequired()])
    remember_me = wt.BooleanField('Remember Me')
    submit = wt.SubmitField('Sign In')
   
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(user_id)
    except:
        return None


def create_app():
    app = Flask(__name__)

    app.config.from_object(__name__)
    login_manager.init_app(app)
    db_wrapper.init_app(app)
    
    from .user import bp as bp_user
    from .shipment import bp as bp_shipment
    
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_shipment)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('homepage'))
        form = LoginForm()
        if form.validate_on_submit():
            try:
                user = User.get(User.username==form.username.data)
            except User.DoesNotExist:
                flash('Invalid username or password')
                return redirect(url_for('login'))
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = '/'
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/')    
        
    @app.route('/')
    def homepage():
        return render_template('index.html')
    
    return app

