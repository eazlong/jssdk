#!/usr/bin/python
# encoding=utf-8
from flask import Flask, jsonify, request, make_response, Response
from werkzeug.datastructures import Headers
import os, time
from xml.etree import ElementTree as ET
from token_manager import TokenManager
from sign import Sign
# from db import 
from pydub import AudioSegment

import base64
import sys
import time
import json
import hashlib
import urllib2
import uuid


app = Flask(__name__)
token_mngr = TokenManager()
host = 'http://www.xrrjkj.com'

invalid_request="Invalid Request"


@app.route("/jssdk", methods=["POST"])
def config():
    print '********************************'
    ticket = token_mngr.get_ticket()
    print ticket
    print 'token'+token_mngr.get_token()
    sign = Sign( ticket, request.form['url'] )
    return make_response(jsonify(sign.sign()), 200)

def asr( path ):
    requrl = "https://api.xfyun.cn/v1/aiui/v1/iat"
    print 'requrl:{}'.format(requrl)
    #讯飞开放平台注册申请应用的应用ID(APPID)
    x_appid = "5acdb572";
    print 'X-Appid:{}'.format(x_appid)
    cur_time = int(time.time())
    print 'X-CurTime:{}'.format(cur_time)
    x_param = {"auf":"16k","aue":"raw","scene":"main"}
    x_param = json.dumps(x_param)
    xparam_base64 = base64.b64encode(x_param.encode(encoding="utf-8")).decode().strip('\n')
    print 'X-Param:{}'.format(xparam_base64)
    #音频文件
    file_data = open(path, 'rb')
    file_base64 = base64.b64encode(file_data.read())
    file_data.close()
    body_data = "data="+file_base64.decode("utf-8")
    #ApiKey创建应用时自动生成
    api_key = "294be53c0cd04409bc5413fce58afbfe"
    token = api_key + str(cur_time)+ xparam_base64 + body_data
    m = hashlib.md5()
    m.update(token.encode(encoding='utf-8'))
    x_check_sum = m.hexdigest()
    print 'X-CheckSum:{}'.format(x_check_sum)
    headers = {"X-Appid": x_appid,"X-CurTime": cur_time,"X-Param":xparam_base64,"X-CheckSum":x_check_sum,"Content-Type":"application/x-www-form-urlencoded"}
    print "headers : {}".format(headers)
    # req = urllib2.Request(requrl, data=body_data.encode('utf-8'), headers=headers, method="POST")
    # with urllib2.urlopen(req) as f:
    req = urllib2.Request(requrl, headers= headers)
    # req.add_header(headers)
    f = urllib2.urlopen(req, body_data.encode('utf-8'))
    body = f.read()
    data = json.loads(body)['data']
    print "result body : {}".format(data['result'])
    return body
    


@app.route("/jssdk/upload", methods=["POST"])
def upload():
    path = str(uuid.uuid1()) + ".mp3"
    file = request.files['file']
    file.save(path)

    sound = AudioSegment.from_file(path)
    save_path = os.path.basename(path)+".pcm"
    sound.export( save_path, format="wav")

    asr( save_path )

    return make_response('xxx', 200)
# class wx: 
#     def __init__(self):
#         #templates_root = os.path.join(self.app_root, 'templates')
#         self.render = web.template.render()
 
#     def GET(self): 
#         in_data = web.input()
#         print in_data
#         if in_data.has_key('signature'):
#             if not ms_interface.check_signature( in_data ):
#                 return "Invalid Request"
#             if ( in_data.has_key( 'echostr' ) ):
#                 return in_data.echostr
#         else:
#             return "Invalid Request"

#     def POST( self ):
#         in_data = web.input()
#         return 'Invalid Request'

# web.webapi.internalerror = web.debugerror

# def run():
#     token_mngr.start()
#     time.sleep(3)

#     import sys
#     reload(sys)
#     sys.setdefaultencoding('utf-8')

#     web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi( func, addr )
#     app.run()
#     token_mngr.stop()

class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        origin = ('Access-Control-Allow-Origin', '*')
        allow_headers = ('Access-Control-Allow-Headers',
                         'Referer, Accept, Origin, User-Agent, Content-Type')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
            headers.add(*allow_headers)
        else:
            headers = Headers([origin, methods, allow_headers])
        kwargs['headers'] = headers
        return super(MyResponse, self).__init__(response, **kwargs)

app.response_class = MyResponse
token_mngr.start();

if __name__  == '__main__':
    app.run()
#flups.WSGIServer(myapp).run()   
#WSGIServer(myapp,bindAddress=('0.0.0.0',8008)).run()
