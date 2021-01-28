# Micropython 1.13 no additional libraries installed
# ESP32 MQTT basic example with periodic non-blocking data publication and subscription to commands topic
#
# Publish topics: 
# 	<ClientID>/status for status information ('MQTT Connected' and 'offline')
# 	<ClientID>/data/json for published data
#
# Subscribe topic:
#	<ClientID>/commands
#
# Copyright 2021 CRCibernetica SA

from umqtt.robust import MQTTClient
import machine
import utime as time
import esp32
import config as c

# If your broker doesn't use any security use this line instead
# client = MQTTClient(c.CLIENTID, c.BROKER, port=c.PORT)
client = MQTTClient(c.CLIENTID, c.BROKER, port=c.PORT, user=c.USER, password=c.PASS)

client.DEBUG=False
client.keepalive=30 # Required for Last Will and Testament
client.set_last_will(c.CLIENTID + '/status', 'offline', retain=True)

start_time = time.ticks_ms()
interval = 10000 # 10 second interval for publishing data

def checkwifi():
    while not sta_if.isconnected():
        time.sleep_ms(500)
        print(".")
        sta_if.connect()
    #print('network config:', sta_if.ifconfig())

# Callback function for incoming messages
def on_message_received(topic, msg):
    print(topic + ' ' + ':' + str(msg))
    if msg == b'ON':
        print('ON')
    elif msg == b'OFF':
        print('OFF')

# Returns True if interval has passed
def ready_to_publish():
    global start_time
    if time.ticks_ms() - start_time > interval:
        start_time = time.ticks_ms()
        return True
    else:
        return False

def publish():
    count = 1
    while True:
        checkwifi() # Make sure wifi is connected, if not reconnect
        client.check_msg() # Check for incoming messages (non-blocking)
        if ready_to_publish(): # If the interval has not passed then don't publish
            client.ping() # Ping the MQTT broker to refresh the keepalive
            temperature=esp32.raw_temperature() # internal temperature of chip
            msg = '{"Count":%u,"Temperature":%2.2f}' % (count,temperature) # Create a message in JSON format
            client.publish(c.CLIENTID + '/data/json', msg)
            count = count + 1
            if count > 99:
                count = 0

client.reconnect() # ensures the MQTT client is connected
client.set_callback(on_message_received)     # First set the callback function for incoming messages
client.subscribe(c.CLIENTID + '/commands')   # then set the subscription topic
client.publish(c.CLIENTID + '/status', 'MQTT connected')

publish() # Repeat forever