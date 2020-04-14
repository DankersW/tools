#!/usr/bin/env python3

import paho.mqtt.client as mqtt

MQTT_BROKER_ADDRESS = "10.42.0.25"
MQTT_PORT = 1883
MQTT_STAYALIVE = 60

client = mqtt.Client()
client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT, MQTT_STAYALIVE)
client.publish("topic/test", "Hello world!")
client.disconnect()