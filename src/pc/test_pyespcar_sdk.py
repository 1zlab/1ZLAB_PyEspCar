import paho.mqtt.client as mqtt
from pyespcar_sdk import PyCarSDK

mqtt_client = mqtt.Client()
# mqtt_client.on_message = on_message
mqtt_client.connect('localhost', 1883, 60)
sdk = PyCarSDK(mqtt_client, is_debug=True)
