import time
import os
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")
DBHOST = os.getenv("DBHOST")
DBPORT = os.getenv("DBPORT")
DBNAME = os.getenv("DBNAME")


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///albums.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
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


@app.route('/albums', method=['GET'])
def get_albums():
    return{
        "data": albums.query.all(),
        "message":"success"
    }

@app.route('/albums', method=['POST'])
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
    app.run(debug=True, host='0.0.0.0',port='8000')