# coding:UTF-8

from flask import Flask
import wechat_sdk


app = Flask(__name__)
access_token = '9Em_q4EJOlYyU0l6EeXQzfK_scKjtJfLdo1LT3D97fkE40GRcOkegRVTjyuHnk8KCnDylt5HxbAXPd7O_c2L6iegDday72wIR1vs8-HaNPk_hs79rYISA4nAYRJYEUiOEWNcABAXPG'


@app.route('/get_access_token', methods=['GET'])
def get_access_token():
    print wechat_sdk.get_access_token('', '')
    return "123"


@app.route('/get_ip')
def get_ip():
    print wechat_sdk.get_wechat_server_ip(access_token)
    return "ok"


@app.route('/get_short_url')
def get_short_url():
    print wechat_sdk.get_short_url(access_token, 'https://www.baidu.com')
    return "ok"


@app.route('/create_short_ticket')
def create_short_ticket():
    print wechat_sdk.create_short_ticket(access_token)
    return '123'


@app.route('/create_long_ticket')
def create_long_ticket():
    print wechat_sdk.create_long_ticket(access_token, 1)
    return '123'


@app.route('/get_ticket_url')
def get_ticket_url():
    return wechat_sdk.get_ticket_url('gQEI8ToAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xLzVqc19pdExsNldPUWg5VjNNaGNrAAIEpu_6VgMEAAAAAA==')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
