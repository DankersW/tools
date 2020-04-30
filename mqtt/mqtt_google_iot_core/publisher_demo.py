import datetime
import json
import ssl
import time

import jwt
import paho.mqtt.client as mqtt
from dataclasses import dataclass


@dataclass
class MqttBridgeConfiguration:
    project_id: str = "dankers"
    registry_id: str = "dankers-iot"
    device_id: str = "test-LED"
    private_key_file: str = "certificates/rsa_private.pem"
    algorithm: str = "RS256"
    cloud_region: str = "europe-west1"
    ca_certs: str = "certificates/roots.pem"
    num_messages: int = 50
    mqtt_bridge_hostname: str = "mqtt.googleapis.com"
    mqtt_bridge_port: int = 8883
    message_type: str = "event"


def create_jwt(project_id, private_key_file, algorithm):
    """Create a JWT (https://jwt.io) to establish an MQTT connection."""
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))


class Device(object):
    def __init__(self):
        self.temperature = 0
        self.connected = False

    def wait_for_connection(self, timeout):
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge.')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        print('Published message acked.')

    def on_subscribe(self, unused_client, unused_userdata, unused_mid, granted_qos):
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        payload = message.payload.decode('utf-8')
        if not payload:
            return
        data = json.loads(payload)
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(payload, message.topic, str(message.qos)))
        print(data)


def main():
    args = MqttBridgeConfiguration()

    # Create the MQTT client and connect to Cloud IoT.
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(args.project_id, args.cloud_region,
        args.registry_id, args.device_id)
    client = mqtt.Client(client_id)
    jwt_pwd = create_jwt(args.project_id, args.private_key_file, args.algorithm)
    client.username_pw_set(username='unused', password=jwt_pwd)
    client.tls_set(ca_certs=args.ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    device = Device()

    client.on_connect = device.on_connect
    client.on_publish = device.on_publish
    client.on_disconnect = device.on_disconnect
    client.on_subscribe = device.on_subscribe
    client.on_message = device.on_message

    client.connect(args.mqtt_bridge_hostname, args.mqtt_bridge_port)
    client.loop_start()

    mqtt_telemetry_topic = '/devices/{}/events'.format(args.device_id)
    mqtt_state_topic = '/devices/{}/state'.format(args.device_id)
    mqtt_config_topic = '/devices/{}/config'.format(args.device_id)

    device.wait_for_connection(5)
    client.subscribe(mqtt_config_topic, qos=1)

    for _ in range(args.num_messages):
        device.temperature += 1
        payload = json.dumps({'temperature': device.temperature, 'other': 12})
        print('Publishing payload: {} - Topic: {}'.format(payload, mqtt_telemetry_topic))
        client.publish(mqtt_telemetry_topic, payload, qos=1)

        if device.temperature % 10 == 0:
            state = device.temperature % 20
            state_payload = json.dumps({'state': state})
            print('Publishing payload: {} - Topic: {}'.format(state_payload, mqtt_state_topic))
            client.publish(mqtt_state_topic, state_payload, qos=1)

        time.sleep(1)

    client.disconnect()
    client.loop_stop()
    print('Finished loop successfully. Goodbye!')


if __name__ == '__main__':
    main()
