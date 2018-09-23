'''
PyGame 键盘事件监听
https://www.pygame.org/docs/ref/key.html#comment_pygame_key_set_repeat

K_SPACE 小车停止
K_w 云台上
K_a 云台左
K_s 云台下
K_d 云台右
K_LEFT 小车左
K_RIGHT 小车向右
K_UP 小车前进
K_DOWN 小车后退

'''
import paho.mqtt.client as mqtt
import time
import pygame
import time
from pyespcar_sdk import PyCarSDK

size = width, height = 320, 240
screen = pygame.display.set_mode(size)
pygame.event.set_allowed([pygame.KEYDOWN,pygame.KEYUP])

def on_message(client, userdata, msg):
    print('topic: {}'.format(msg.topic))
    print('message: {}'.format(str(msg.payload)))

client = mqtt.Client()
client.on_message = on_message

client.connect('localhost', 1883, 60)

sdk = PyCarSDK(client, is_debug=True)

while True:
    events = pygame.event.get()
    sdk.response_keys_event(events)
    time.sleep(0.1)