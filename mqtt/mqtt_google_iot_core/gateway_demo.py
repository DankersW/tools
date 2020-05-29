import datetime
import ssl
import time
import threading
from dataclasses import dataclass
import jwt
import paho.mqtt.client as mqtt


@dataclass
class MqttGatewayConfiguration:
    project_id: str = "dankers"
    registry_id: str = "home_automation_light_switches"
    gateway_id: str = "home_automation_light_switches_gateway"
    private_key_file: str = "certificates/rsa_light_switch_private.pem"
    algorithm: str = "RS256"
    cloud_region: str = "europe-west1"
    ca_certs: str = "certificates/roots.pem"
    mqtt_bridge_hostname: str = "mqtt.googleapis.com"
    mqtt_bridge_port: int = 8883


GATEWAY_NAME = 'GCP_GATEWAY'
ONE_MILLISECOND_SECONDS = 0.001

def create_jwt(project_id, private_key_file, algorithm):
    """Create a JWT (https://jwt.io) to establish an MQTT connection."""
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
        current_time = datetime.datetime.now()
    print("{} - {} | Creating JWT from private key file using {}.".format(current_time, GATEWAY_NAME, algorithm))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return '{} - {}'.format(rc, mqtt.error_string(rc))


class GBridge(threading.Thread):
    mqtt_client = None
    g_bridge_connected = False

    attached_devices = []
    pending_messages = []
    pending_subscribed_topics = []

    def __init__(self):
        threading.Thread.__init__(self)
        gateway_configuration = MqttGatewayConfiguration()
        self.gateway_id = gateway_configuration.gateway_id
        self.connect_to_iot_core_broker(gateway_configuration)

    def __del__(self):
        self.detach_all_devices()
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def run(self):
        self.mqtt_client.loop_start()
        self.wait_for_connection(5)
        while self.g_bridge_connected:
            time.sleep(ONE_MILLISECOND_SECONDS)

    def connect_to_iot_core_broker(self, conf):
        # Create the MQTT client and connect to Cloud IoT.
        gateway_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(conf.project_id, conf.cloud_region,
                                                                                conf.registry_id, conf.gateway_id)
        self.mqtt_client = mqtt.Client(gateway_id)
        jwt_pwd = create_jwt(conf.project_id, conf.private_key_file, conf.algorithm)
        self.mqtt_client.username_pw_set(username='unused', password=jwt_pwd)
        self.mqtt_client.tls_set(ca_certs=conf.ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_subscribe = self.on_subscribe
        self.mqtt_client.on_message = self.on_message

        self.mqtt_client.connect(conf.mqtt_bridge_hostname, conf.mqtt_bridge_port)

    def wait_for_connection(self, timeout):
        total_time = 0
        while not self.g_bridge_connected and total_time < timeout:
            time.sleep(1)
            total_time += 1
        if not self.g_bridge_connected:
            current_time = datetime.datetime.now()
            raise RuntimeError("{} - {} | Could not connect to Iot Core MQTT bridge.".format(current_time,
                                                                                             GATEWAY_NAME))

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        current_time = datetime.datetime.now()
        print("{} - {} | Connected to GCP IoT core MQTT Broker with connection Result: {}".format(current_time,
                                                                                                  GATEWAY_NAME,
                                                                                                  error_str(rc)))
        self.g_bridge_connected = True
        self.subscribe_to_topics(self.gateway_id, True)

    def subscribe_to_topics(self, dev_id, gateway):
        config_topic = '/devices/{}/config'.format(dev_id)
        command_topic = '/devices/{}/commands/#'.format(dev_id)
        subscriptions = [{'topic': config_topic, 'qos': 1}, {'topic': command_topic, 'qos': 1}]
        if gateway:
            gateway_error_topic = '/devices/{}/errors'.format(dev_id)
            subscriptions.append({'topic': gateway_error_topic, 'qos': 0})

        for subscription in subscriptions:
            self.subscribe(subscription.get('topic'), subscription.get('qos'))

    def subscribe(self, topic, qos):
        _, mid = self.mqtt_client.subscribe(topic, qos)
        self.pending_subscribed_topics.append(mid)
        while topic in self.pending_subscribed_topics:
            time.sleep(0.01)
        current_time = datetime.datetime.now()
        print('{} - {} | Successfully subscribed to topic \'{}\' with Qos \'{}\'.'.format(current_time, GATEWAY_NAME,
                                                                                          topic, qos))

    def on_disconnect(self, unused_client, unused_userdata, rc):
        current_time = datetime.datetime.now()
        print("{} - {} | Disconnected: {}".format(current_time, GATEWAY_NAME, error_str(rc)))
        self.g_bridge_connected = False

    def on_publish(self, unused_client, unused_userdata, mid):
        current_time = datetime.datetime.now()
        print("{} - {} | ACK received for message \'{}\'".format(current_time, GATEWAY_NAME, mid))
        if mid in self.pending_messages:
            self.pending_messages.remove(mid)

    def on_subscribe(self, unused_client, unused_userdata, mid, granted_qos):
        if granted_qos[0] == 128:
            current_time = datetime.datetime.now()
            print("{} - {} | Subscription result: {} - Subscription failed".format(current_time, GATEWAY_NAME,
                                                                                   granted_qos[0]))
        else:
            if mid in self.pending_subscribed_topics:
                self.pending_subscribed_topics.remove(mid)

    def on_message(self, unused_client, unused_userdata, message):
        payload = message.payload.decode('utf-8')
        current_time = datetime.datetime.now()
        print('{} - {} | Received message \'{}\' on topic \'{}\'.'.format(current_time, GATEWAY_NAME,payload,
                                                                          message.topic))

    def attach_device(self, device_id):
        current_time = datetime.datetime.now()
        print('{} - {} | Attaching device \'{}\'.'.format(current_time, GATEWAY_NAME, device_id))
        attach_topic = '/devices/{}/attach'.format(device_id)
        if device_id not in self.attached_devices:
            self.attached_devices.append(device_id)
        self.publish(attach_topic, "")  # Message content is empty because gateway auth-method=ASSOCIATION_ONLY
        self.subscribe_to_topics(device_id, False)

    def detach_device(self, device_id):
        current_time = datetime.datetime.now()
        print('{} - {} | Detaching device \'{}\'.'.format(current_time, GATEWAY_NAME, device_id))
        detach_topic = '/devices/{}/detach'.format(device_id)
        if device_id in self.attached_devices:
            self.attached_devices.remove(device_id)
        self.publish(detach_topic, "")  # Message content is empty because gateway auth-method=ASSOCIATION_ONLY

    def detach_all_devices(self):
        current_time = datetime.datetime.now()
        print('{} - {} | Detaching all devices. Currently all connected devices: \'{}\'.'.format(current_time,
                                                                                                 GATEWAY_NAME,
                                                                                                 self.attached_devices))
        for device in self.attached_devices[:]:
            self.detach_device(device)
        while self.attached_devices:  # Make sure all devices have been detached
            time.sleep(0.01)

    def publish(self, topic, payload):
        message_info = self.mqtt_client.publish(topic, payload, qos=1)
        self.pending_messages.append(message_info.mid)
        current_time = datetime.datetime.now()
        print('{} - {} | Publishing payload: \'{}\' on Topic \'{}\' with mid \'{}\'.'.format(current_time, GATEWAY_NAME,
                                                                                             payload, topic,
                                                                                             message_info.mid))
        while message_info.mid in self.pending_messages:  # Waiting for message ACK to arrive
            time.sleep(0.01)

    def send_data(self, device_id, event_type, payload):
        if event_type == "telemetry":
            topic = '/devices/{}/events'.format(device_id)
        elif event_type == "state":
            topic = '/devices/{}/state'.format(device_id)
        else:
            current_time = datetime.datetime.now()
            print("{} - {} | Error: Unknown event type {}.".format(current_time, GATEWAY_NAME, event_type))
            return

        self.publish(topic, payload)


def main():
    g_bridge = GBridge()
    g_bridge.start()
    time.sleep(2)

    device_list = ["light_switch_001", "light_switch_002"]
    print("")
    g_bridge.attach_device(device_list[0])
    g_bridge.attach_device(device_list[1])
    print("")
    time.sleep(3)

    print("")
    data = "light_state: 1"
    g_bridge.send_data(device_list[0], "state", data)

    time.sleep(100)
    print("")
    g_bridge.__del__()
    del g_bridge

# todo: include a time off to wait for pending messages and resend
# todo: if a device is going to be detached make sure that device does not have any pending messages


if __name__ == '__main__':
    main()
