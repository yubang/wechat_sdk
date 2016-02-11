# coding:UTF-8

from flask import Flask
import wechat_sdk


app = Flask(__name__)
access_token = 'dE_-_LLGsrJmpVVQ87c3GSGIqjG72f4_7sKojYbaN9aHHLoRw_AWBRSBI3wcncf10KniPYJu_O6HyDE_cy1xcinrWmfbNvgq4o2jcIDfVZXXdvO-bGREFpDBDAcqQ6weIEHcAGAVRU'


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


@app.route('/set_template_industry')
def set_template_industry():
    print wechat_sdk.set_template_industry(access_token, 1, 5)
    return "ok"


@app.route('/get_template_id')
def get_template_id():
    print wechat_sdk.get_template_id(access_token, 'TM00001')
    return 'ok'


@app.route('/send_template_message')
def send_template_message():
    print wechat_sdk.send_template_message(access_token, '8rdEgQKL-N4tlvcvAbevA1c2QC8q7AaVhojI6xw5_18', {}, 'o4CfkwG89Xw0S79gXYDxBQ8qvg5c', 'http://www.baidu.com')
    return "ok"


@app.route('/get_all_templates')
def get_all_templates():
    print wechat_sdk.get_all_templates(access_token)
    return 'ok'


@app.route('/send_text_message')
def send_text_message():
    print wechat_sdk.send_text_message(access_token,  'o4CfkwG89Xw0S79gXYDxBQ8qvg5c', u'测试内容！')
    return 'ok'


@app.route('/send_media_message')
def send_media_message():
    print wechat_sdk.send_media_message(access_token, 'o4CfkwG89Xw0S79gXYDxBQ8qvg5c', 'OJ-mMeBQ4rxVCB1-jEBKUaUA9L-bh4rNPhqxGXDwzIHPvmm3HzBhQzcqzCHIAEGP', 'image')
    return 'ok'


@app.route('/update_media')
def update_media():
    with open('C:/Users/yubang/Desktop/1.jpg', 'rb') as fp:
        print wechat_sdk.update_media(access_token, 'image', '1.jpg', fp.read())
    return "ok"


@app.route('/create_menu')
def create_menu():
    print wechat_sdk.create_menu(access_token, [{ "type":"view",
               "name":"搜索",
               "url":"http://www.soso.com/"}])
    return "ok"


@app.route('/get_menu')
def get_menu():
    print wechat_sdk.get_menu(access_token)
    return "ok"


@app.route('/delete_menu')
def delete_menu():
    print wechat_sdk.delete_menu(access_token)
    return "ok"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
