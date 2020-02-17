# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify
from plugins import License

app = Flask(__name__)

license = License('irj32oinj0af08hf0wajfoieajf')


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == 'GET':
        sn = request.args.get('sn')
        username = request.args.get('username')
        email = request.args.get('email')
    data = {'license': license.make_lincense(sn)}
    return jsonify(data)


if __name__ == '__main__':
    # app.debug = True  # 设置调试模式，生产模式的时候要关掉debug
    app.run(host='0.0.0.0', port='80', debug=True)
