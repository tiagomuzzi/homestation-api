import time
import os
from flask import Flask, flash, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///albums.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
a =\
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=os.getenv("DBUSER"),
        passwd=os.getenv("DBPASS"),
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
        db=os.getenv("DBNAME"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'

db = SQLAlchemy(app)


class albums(db.Model):
    id = db.Column('album_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)

    def __init__(self, name, author, year):
        self.name = name
        self.author = author
        self.year = year
        


def database_initialization_sequence():
    db.create_all()
    test_rec = albums(
            'John Doe',
            'Los Angeles',
            '123 Foobar Ave')

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()

@app.route('/')
def home():
    return 'Flask with docker!'

@app.route('/albums', methods=['GET'])
def get_albums():
    app.logger.info('im here')
    return{
        "data": albums.query.all(),
        "message":"success"
    }

@app.route('/albums', methods=['POST'])
def new_album():
    album = albums(
            request.form['name'],
            request.form['author'],
            request.form['year'])

    db.session.add(album)
    db.session.commit()
    flash('Record was succesfully added')
    return {"message":"success"}


if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0',port=8000)