from flask import Flask, render_template, g
import sqlite3


DATABASE = 'myshipping.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    app = create_app()
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
        
def create_app():
    app = Flask(__name__)

    @app.route('/')
    def homepage():
        return render_template('index.html')
    
    @app.teardown_appcontext
    def close_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return app

