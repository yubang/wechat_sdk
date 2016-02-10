# coding:UTF-8


"""
微信公众号相关操作封装
"""


import requests
import json


request_timeout = 10


def __fetch_url(url, is_get=True, post_data=None):
    """
    发送一个GET请求
    :param url: 要请求的url
    :param is_get: 是否是GET请求
    :param post_data: POST数据
    :return: 数据, 状态码（0为正确处理数据，-1为微信服务器无法响应，-2为无法处理微信服务器返回的数据）
    """
    if is_get:
        r = requests.get(url, timeout=request_timeout)
    else:
        r = requests.post(url, post_data, timeout=request_timeout)

    if r.status_code == 200:
        try:
            obj = json.loads(r.text)
            return obj, 0
        except Exception:
            return r.text, -2
    else:
        return None, -1


def __handle_get_data(data, code):
    """
    处理请求服务器之后的返回数据
    :param data: 经处理成字典的数据
    :param code: 状态码
    :return:
    """
    result = {"code": code, "msg": u"ok", "content": data}

    if code == -1:
        result['msg'] = u'微信服务器无法响应'
    elif code == -2:
        result['msg'] = u'无法处理微信服务器返回的数据'
    else:
        if 'errcode' in result['content']:
            result['code'] = result['content']['errcode']
            if 'errmsg' in result['content']:
                result['msg'] = result['content']['errmsg']
            else:
                result['msg'] = u'未知错误！'

    return result


def __get_data_use_api(target_url, is_get=True, post_data=None):
    """
    调用微信API接口
    :param target_url: 要请求的url
    :param is_get: 是否是GET请求
    :param post_data:
    :return: POST数据
    """
    data, code = __fetch_url(target_url, is_get, post_data)

    # 处理数据
    result = __handle_get_data(data, code)

    return result


def get_access_token(appid, secret):
    """
    获取微信access_token，该凭证是微信所有接口所需要的
    该接口不提供缓存功能，由于该接口调用次数有限，请自己缓存
    :param appid: 公众号appid
    :param secret: 公众号secret
    :return:
    """
    # 请求服务器
    target_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, secret)
    result = __get_data_use_api(target_url)
    return result


def get_wechat_server_ip(access_token):
    """
    获取微信服务器ip
    :param access_token: 微信access_token
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s' % access_token
    result = __get_data_use_api(target_url)
    return result
