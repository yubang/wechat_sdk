# coding:UTF-8


"""
微信公众号相关操作封装
"""


import requests
import json
import urllib


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
        r = requests.post(url, json.dumps(post_data), timeout=request_timeout)

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
        if 'errcode' in result['content'] and result['content']['errcode'] != 0:
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


def get_short_url(access_token, source_url):
    """
    将一条长链接转成短链接
    :param access_token: 微信access_token
    :param source_url: 源网址
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/shorturl?access_token=%s' % access_token
    result = __get_data_use_api(target_url, False, {"action": 'long2short', 'long_url': source_url})
    return result


def create_short_ticket(access_token, expire_seconds=2592000, scene_id=0):
    """
    创建临时二维码
    :param access_token: 微信access_token
    :param expire_seconds: 二维码过期时间
    :param scene_id: 场景值ID
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % access_token
    result = __get_data_use_api(target_url, False, {"expire_seconds": expire_seconds, "action_info": {"scene": {"scene_id": scene_id}}, "action_name": 'QR_SCENE'})
    return result


def create_long_ticket(access_token, scene_id=0, scene_str=None):
    """
    创建永久二维码
    注意场景id只能选择一种
    :param access_token: 微信access_token
    :param scene_id: 场景值ID
    :param scene_str: 场景值ID（字符串）
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % access_token
    if scene_str:
        result = __get_data_use_api(target_url, False, {"action_info": {"scene": {"scene_str": scene_str}}, "action_name": 'QR_LIMIT_STR_SCENE'})
    else:
        result = __get_data_use_api(target_url, False, {"action_info": {"scene": {"scene_id": scene_id}}, "action_name": 'QR_LIMIT_SCENE'})

    return result


def get_ticket_url(ticket):
    """
    获取二维码地址，注意该接口只返回一个url
    :param ticket: 微信二维码ticket
    :return:
    """
    url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s' % urllib.quote(ticket)
    return url
