import RPi.GPIO as GPIO
import time
import logging
import paho.mqtt.client as mqtt
from OpenSSL import SSL
import os
import ssl

log = logging.getLogger('RemoTV.hardware.l298n')

logging.basicConfig(level=logging.DEBUG)

sleeptime = 0.2
rotatetimes = 0.4

StepPinForward = None
StepPinBackward = None
StepPinLeft = None
StepPinRight = None


def setup(robot_config):
    global StepPinForward
    global StepPinBackward
    global StepPinLeft
    global StepPinRight
    global sleeptime
    global rotatetimes

    sleeptime = robot_config.getfloat('l298n', 'sleeptime')
    rotatetimes = robot_config.getfloat('l298n', 'rotatetimes')

    log.debug("GPIO mode : %s", str(GPIO.getmode()))

    GPIO.setwarnings(False)
    GPIO.cleanup()

    if robot_config.getboolean('tts', 'ext_chat'):  # ext_chat enabled, add motor commands
        extended_command.add_command('.set_rotate_time', set_rotate_time)
        extended_command.add_command('.set_sleep_time', set_sleep_time)

    # TODO passing these as tuples may be unnecessary, it may accept lists as well.
    StepPinForward = tuple(map(int, robot_config.get('l298n', 'StepPinForward').split(',')))
    StepPinBackward = tuple(map(int, robot_config.get('l298n', 'StepPinBackward').split(',')))
    StepPinLeft = tuple(map(int, robot_config.get('l298n', 'StepPinLeft').split(',')))
    StepPinRight = tuple(map(int, robot_config.get('l298n', 'StepPinRight').split(',')))


def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setup(37, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)

    if payload == 'f':
        GPIO.output(38, GPIO.HIGH)
        time.sleep(sleeptime)
        GPIO.output(38, GPIO.LOW)
    if payload == 'b':
        GPIO.output(37, GPIO.HIGH)
        time.sleep(sleeptime)
        GPIO.output(37, GPIO.LOW)
    if payload == 'l':
        GPIO.output(15, GPIO.HIGH)
        time.sleep(sleeptime * rotatetimes)
        GPIO.output(15, GPIO.LOW)
    if payload == 'r':
        GPIO.output(16, GPIO.HIGH)
        time.sleep(sleeptime * rotatetimes)
        GPIO.output(16, GPIO.LOW)
    if payload == 'z':
        GPIO.output(36, GPIO.HIGH)
        time.sleep(sleeptime * rotatetimes)
        GPIO.output(36, GPIO.LOW)
    if payload == 'x':
        GPIO.output(35, GPIO.HIGH)
        time.sleep(sleeptime * rotatetimes)
        GPIO.output(35, GPIO.LOW)

client = mqtt.Client(transport="websockets")

# Set the TLS/SSL parameters for the client
client.tls_set(
    certfile='/home/pi/claw/fullchain.pem',
    keyfile='/home/pi/claw/privkey.pem',
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=SSL.SSLv23_METHOD
)

client.username_pw_set(username="omar", password="fuckomar")

# client.tls_insecure_set(False)

client.on_message = on_message

client.connect('clawclan.co.uk', 8083)

client.subscribe("clawmachine2/controls")

client.loop_forever()

logging.debug("Using SSL version %s", conn.version())
