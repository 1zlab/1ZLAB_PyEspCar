# -*- coding: utf-8 -*- 
'''

Document
https://pypi.org/project/websocket-client/
'''
import websocket

import websocket
ws = websocket.WebSocket()
ESP32_IP = ''
ESP32_PORT = 8266
ws.connect("ws://example.com/websocket", http_proxy_host="proxy_host_name", http_proxy_port=3128)
