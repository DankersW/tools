#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import sys

MQTT_BROKER_ADDRESS = "10.42.0.25"
MQTT_PORT = 1883
MQTT_STAYALIVE = 60

TOPICS = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    time = datetime.datetime.now()
    payload = msg.payload.decode('utf-8')
    print("{} | Received message: \"{}\" on Topic: \"{}\"".format(time, payload, msg.topic))


client = mqtt.Client()
client.connect(MQTT_BROKER_ADDRESS, MQTT_PORT, MQTT_STAYALIVE)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
