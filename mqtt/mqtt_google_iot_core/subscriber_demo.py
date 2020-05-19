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
    registry_id: str = "home_automation_light_switches"#"dankers-iot"
    device_id: str = "light_switch_001"#"test-LED"
    private_key_file: str = "certificates/rsa_light_switch_private.pem"#"certificates/rsa_private.pem"
    algorithm: str = "RS256"#"RS256"
    cloud_region: str = "europe-west1"
    ca_certs: str = "certificates/roots.pem"
    num_messages: int = 10
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
    device_active = True

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
        # Example string to send " {"temperature": 25, "deviceActive": 0} "
        payload = message.payload.decode('utf-8')
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(payload, message.topic, str(message.qos)))

        try:
            data = json.loads(payload)
            if "temperature" in data:
                self.temperature = data["temperature"]
            if "deviceActive" in data:
                self.device_active = data["deviceActive"]
        except ValueError as e:
            print("error when decoding JSON: {}".format(e))

        print("temp: {} - device_active: {}".format(self.temperature, self.device_active))


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
    device.wait_for_connection(5)

    mqtt_commands_topic = '/devices/{}/commands/#'.format(args.device_id)
    client.subscribe(mqtt_commands_topic, qos=1)

    while device.device_active:
        time.sleep(0.1)

    time.sleep(2)
    client.disconnect()
    client.loop_stop()
    print('Finished loop successfully. Goodbye!')


if __name__ == '__main__':
    main()
