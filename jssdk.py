#!/usr/bin/python
# encoding=utf-8
from flask import Flask, jsonify, request, make_response, Response
import os
import time
from xml.etree import ElementTree as ET
from token_manager import TokenManager
from sign import Sign
# from db import *



app = Flask(__name__)
token_mngr = TokenManager()
host = 'http://www.xrrjkj.com'

invalid_request="Invalid Request"


@app.route("/jssdk", methods=["POST"])
def config():
    print '********************************'
    ticket = token_manager.get_ticket()
    sign = Sign( ticket, request.data['url'] )
    return sign.sign()



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
        return super().__init__(response, **kwargs)

if __name__  == '__main__':
    app.response = MyResponse
    app.run(host='0.0.0.0', port=9010)
#flups.WSGIServer(myapp).run()   
#WSGIServer(myapp,bindAddress=('0.0.0.0',8008)).run()
