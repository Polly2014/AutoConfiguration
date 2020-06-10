# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory, render_template
from plugins import License
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class LicenseInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sn = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    license = db.Column(db.String(80), unique=False, nullable=False)
    time_regist = db.Column(db.Date, nullable=False,
                            default=datetime.datetime.now)

    def __repr__(self):
        return '<SN: {}>'.format(self.sn)


license = License('26716201@qq.com')


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == 'GET':
        sn = request.args.get('sn')
        username = request.args.get('username')
        email = request.args.get('email')
    data = {'license': license.make_lincense(sn)}
    if len(LicenseInfo.query.filter_by(sn=sn).all()) > 0:
        data['message'] = 'SN number Exist!'
        print('SN number Exist!')
    else:
        li = (sn=sn, username=username,
              email=email, license=data['license'])
        db.session.add(li)
        db.session.commit()
        print('[{}] License Info Insert to DB Success'.format(sn))
    return jsonify(data)


@app.route('/download/<filename>', methods=['POST', 'GET'])
def download_data(filename):
    if request.method == 'GET':
        if os.path.isfile(os.path.join('downloads', filename)):
            print("Finde")
            return send_from_directory('downloads', filename, as_attachment=True)
        else:
            print("Not Exist")
    else:
        print("Not GET Method")


@app.route('/paperdata2020')
def paperdata():
    return app.send_static_file('html/uaalink.html')


@app.route('/')
def index():
    return app.send_static_file('html/uaalink.html')


if __name__ == '__main__':
    # app.debug = True  # 设置调试模式，生产模式的时候要关掉debug
    if not os.path.exists('./database.db'):
        db.create_all()
    app.run(host='0.0.0.0', port=80, debug=False)
