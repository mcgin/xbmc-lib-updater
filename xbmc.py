#!/usr/bin python

settings = {
    'hostname': '192.168.0.4',
    'port': '80',
    'username': 'XBMC',
    'password': 'XBMC',
    'mac_address': '0:0:0:0:0:0'
}

http_address = 'http://%s:%s/jsonrpc' % (settings['hostname'], settings['port'])
username = settings['username']
password = settings['password']

try:
    import json
except ImportError:
    import simplejson as json
import urllib2, base64, time, socket, struct

class XBMCJSON:

    def __init__(self, server):
        self.server = server
        self.version = '2.0'

    def __call__(self, **kwargs):
        method = '.'.join(map(str, self.n))
        self.n = []
        return XBMCJSON.__dict__['Request'](self, method, kwargs)

    def __getattr__(self,name):
        if not self.__dict__.has_key('n'):
            self.n=[]
        self.n.append(name)
        return self

    def Request(self, method, kwargs):
        data = [{}]
        data[0]['method'] = method
        data[0]['params'] = kwargs
        data[0]['jsonrpc'] = self.version
        data[0]['id'] = 1

        data = json.JSONEncoder().encode(data)
        content_length = len(data)

        content = {
            'Content-Type': 'application/json',
            'Content-Length': content_length,
        }
   
        request = urllib2.Request(self.server, data, content)
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        f = urllib2.urlopen(request)
        response = f.read()
        f.close()
        response = json.JSONDecoder().decode(response)

        try:
            return response[0]['result']
        except:
            return response[0]['error']


xbmc = XBMCJSON(http_address)

mac_address = settings['mac_address']
addr_byte = mac_address.split(':')
hw_addr = struct.pack('BBBBBB',
    int(addr_byte[0], 16),
    int(addr_byte[1], 16),
    int(addr_byte[2], 16),
    int(addr_byte[3], 16),
    int(addr_byte[4], 16),
    int(addr_byte[5], 16)
)


#Send wakeup packet
#msg = '\xff' * 6 + hw_addr * 16
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#s.sendto(msg, ("255.255.255.255", 9))


xbmc.VideoLibrary.Scan()
time.sleep(600)
xbmc.AudioLibrary.Scan()
#xbmc.System.Shutdown()
