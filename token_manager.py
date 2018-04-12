#!/usr/bin/python
# encoding : utf-8

import threading
import time
import httplib
import json
#import commands

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton  

# APPID="wx8d318dd436013ad3"
# APPSecret="ef662f9aa7c6d8f0c6691cbce646763d"
APPID="wx6b6146e1028f0c2d"
APPSecret="3a253147cb987ecdea9bb6cad250306f"

@singleton
class TokenManager( threading.Thread ):
    def __init__( self ):
        threading.Thread.__init__( self )
        self.to_stop = False
        self.access_token=""
        self.expires_time = 7200
        self.ticket =""

        self.__gettoken();
        self.__getticket();

    def run( self ):
        while not self.to_stop:
            if self.expires_time < 20:
                self.__gettoken()
                self.__getticket()

            time.sleep( 10 )
            self.expires_time -= 10

    def __gettoken(self):
        conn = httplib.HTTPSConnection( 'api.weixin.qq.com' )
                #data = urllib.urlencode( { 'secret':APPSecret, 'grant_type':'client_credential', 'appid':APPID } )
        conn.request( 'GET', '/cgi-bin/token?grant_type=client_credential&appid='+APPID+'&secret='+APPSecret )
        res = conn.getresponse()
        if res.status != 200:
            print "get response error" 
            conn.close()
            return

        body = res.read()
        conn.close()
        json_data = json.loads( body )
        json_data['access_token'] 
        if json_data.has_key( "errcode" ):
            print json_data['errmsg']
        else:
            self.access_token = json_data['access_token']
            self.expires_time = int(json_data['expires_in'])
            print 'access_token:' + self.access_token + ' expires_time:' + str(self.expires_time)

    def __getticket(self):
        conn = httplib.HTTPSConnection( 'api.weixin.qq.com' )
        conn.request( 'GET', '/cgi-bin/ticket/getticket?access_token='+self.access_token+'&type=jsapi');
        res = conn.getresponse()
        if res.status != 200:
            print "get response error" 
            conn.close()
            return


        body = res.read()
        conn.close()
        json_data = json.loads( body )
        if json_data.has_key( "ticket" ):
            self.ticket = json_data['ticket']
            print 'ticket:' + self.ticket 

    def stop( self ):
        self.to_stop = True

    def get_token( self ):
        return self.access_token

    def get_ticket( self ):
        return self.ticket
