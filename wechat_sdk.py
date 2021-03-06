# coding:UTF-8


"""
微信公众号相关操作封装
@author: yubang
@version: 1.0
2016年02月11日
"""


from xml.dom.minidom import Document
import requests
import json
import urllib
import time


request_timeout = 10


def __fetch_url(url, is_get=True, post_data=None):
    """
    发送一个GET请求
    :param url: 要请求的url
    :param is_get: 是否是GET请求
    :param post_data: POST数据
    :return: 数据, 状态码（0为正确处理数据，-1为微信服务器无法响应，-2为无法处理微信服务器返回的数据）
    """
    try:
        if is_get:
            r = requests.get(url, timeout=request_timeout)
        else:
            r = requests.post(url, json.dumps(post_data, ensure_ascii=False), timeout=request_timeout)
    except Exception:
        return None, 0

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


def set_template_industry(access_token, industry_id1, industry_id2):
    """
    设置所属行业
    行业代码请看：http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html#.E8.AE.BE.E7.BD.AE.E6.89.80.E5.B1.9E.E8.A1.8C.E4.B8.9A
    :param access_token: 微信access_token
    :param industry_id1: 行业代码1
    :param industry_id2: 行业代码2
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/template/api_set_industry?access_token=%s' % access_token
    result = __get_data_use_api(target_url, False, {"industry_id1": industry_id1, "industry_id2": industry_id2})
    return result


def get_template_id(access_token, template_id_short):
    """
    获取模板id
    :param access_token: 微信access_token
    :param template_id_short:模板库中模板的编号
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/template/api_add_template?access_token=%s' % access_token
    result = __get_data_use_api(target_url, False, {"template_id_short": template_id_short})
    return result


def send_template_message(access_token, template_id, template_data, targer_open_id, target_url):
    """
    发送模版消息
    :param access_token: 微信access_token
    :param template_id: 模板id
    :param template_data: 模板数据
    :param targer_open_id: 目标用户open_id
    :param target_url: 模板消息跳转的url
    :return:
    """
    api_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
    result = __get_data_use_api(api_url, False, {
        "touser": targer_open_id,
        "template_id": template_id,
        "url": target_url,
        "data": template_data
    })
    return result


def get_all_templates(access_token):
    """
    获取所有设置的模板
    :param access_token: 微信access_token
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token=%s' % access_token
    result = __get_data_use_api(target_url)
    return result


def send_text_message(access_token,  target_open_id, text):
    """
    发送文本消息
    :param access_token: 微信access_token
    :param target_open_id: 目标用户open_id
    :param text: 需要发送的文本内容
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % access_token
    result = __get_data_use_api(target_url, False, {"touser": target_open_id, "text": {"content": text.encode("UTF-8")}, "msgtype": 'text'})
    return result


def send_media_message(access_token, target_open_id, media_id, media_type):
    """
    发送媒体信息
    :param access_token: 微信access_token
    :param target_open_id: 目标用户open_id
    :param media_id: 媒体id
    :param media_type: 媒体类型，image，voice
    :return:
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % access_token
    result = __get_data_use_api(target_url, False, {"touser": target_open_id, media_type: {"media_id": media_id}, "msgtype": media_type})
    return result


def update_media(access_token, media_type, media_name, media_data):
    """
    上传临时媒体素材
    :param access_token: 微信access_token
    :param media_type: 媒体类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
    :param media_data: 媒体数据
    :param media_name: 媒体名字
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s' % (access_token, media_type)
    try:
        r = requests.post(target_url, files={"media": (media_name, media_data)}, timeout=request_timeout)
        if r.status_code == 200:
            try:
                data = json.loads(r.text)
                code = 0
            except Exception:
                data = r.text
                code = -2
        else:
            code = -1
            data = None
    except Exception:
        code = -1
        data = None

    result = __handle_get_data(data, code)
    return result


def create_menu(access_token, menu_data):
    """
    创建菜单
    :param access_token: 微信access_token
    :param menu_data: 菜单数据
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
    result = __get_data_use_api(target_url, False, {"button": menu_data})
    return result


def get_menu(access_token):
    """
    查询菜单
    :param access_token: 微信access_token
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s' % access_token
    return __get_data_use_api(target_url)


def delete_menu(access_token):
    """
    删除菜单
    :param access_token: 微信access_token
    """
    target_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s' % access_token
    return __get_data_use_api(target_url)


# def send_text_message(access_token, source_wechat, target_open_id, text):
#     """
#     发送文本消息
#     :param access_token: 微信access_token
#     :param source_wechat: 微信号
#     :param target_open_id: 目标用户open_id
#     :param text: 需要发送的文本内容
#     :return:
#     """
#     doc = Document()
#     root = doc.createElement("xml")
#
#     attr = doc.createElement("ToUserName")
#     attr.appendChild(doc.createTextNode(target_open_id))
#     root.appendChild(attr)
#
#     attr = doc.createElement("FromUserName")
#     attr.appendChild(doc.createTextNode(source_wechat))
#     root.appendChild(attr)
#
#     attr = doc.createElement("CreateTime")
#     attr.appendChild(doc.createTextNode(str(int(time.time()))))
#     root.appendChild(attr)
#
#     attr = doc.createElement("MsgType")
#     attr.appendChild(doc.createTextNode('text'))
#     root.appendChild(attr)
#
#     attr = doc.createElement("Content")
#     attr.appendChild(doc.createTextNode(text))
#     root.appendChild(attr)
#
#     print root.toprettyxml()


class WechatApi(object):
    """
    微信服务器API接口封装类
    """
    def init(self, text):
        pass
