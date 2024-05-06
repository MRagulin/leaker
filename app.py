#!/usr/bin/env python
from flask import Flask
from flask import jsonify, json
from flask import render_template
from flask import request
from os import mkdir
from os.path import isdir
from hashlib import md5
from config import Config
from flask_sqlalchemy import SQLAlchemy
from re import match


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(64), unique=True)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True)
    fio = db.Column(db.String(128))
    source = db.Column(db.Integer, db.ForeignKey(Source.id), primary_key=True)


@app.route('/')
def main():
    columns = ['Телефон', 'Email', 'ФИО', 'Источник']
    query = request.args.get('query')
    tmp_data = {}

    if query:
        query = query.strip().lower()
        if '@' in query:
            data = Data.query.filter_by(email=query).join(Source, Source.id == Data.source).add_columns(Data.phone, Data.email, Data.fio, Source.name).first()
        elif match('^\d{,11}$', query):
            data = Data.query.filter_by(phone=query).join(Source, Source.id == Data.source).add_columns(Data.phone, Data.email, Data.fio, Source.name).first()
        else:
            data = Data.query.filter_by(fio=query).join(Source, Source.id == Data.source).add_columns(Data.phone, Data.email, Data.fio, Source.name).first()

        if data is not None and len(data) > 0:
            for idx, el in enumerate(columns):
                tmp_data[columns[idx]] = data[idx + 1]
            tmp_data[columns[-1]] = '<span class="badge bg-primary">{}</span>'.format(tmp_data[columns[-1]])

    return render_template('index.html', data=tmp_data)



@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            return jsonify("{'status: error', 'text': 'No selected file'}")
        if f:
            if not isdir('uploads'):
                mkdir('uploads', mode=0o666, dir_fd=None)
            f.save('uploads/' + md5(f.filename.encode('utf-8')).hexdigest())
    return jsonify("{'status: success'}")


def create_database():
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0')



