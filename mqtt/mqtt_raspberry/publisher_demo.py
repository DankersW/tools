#!/usr/bin/env python3
# usage python3 publisher_demo.py [topic] [data]

import paho.mqtt.client as mqtt
import sys

MQTT_BROKER_ADDRESS = "192.168.1.125"
MQTT_PORT = 1883
MQTT_STAYALIVE = 60

topic = sys.argv[1]
data = sys.argv[2]

print("topic: " + str(topic) + "\t data: " + str(data))

client = mqtt.Client()
client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT, MQTT_STAYALIVE)
client.publish(topic, data)
client.disconnect()
