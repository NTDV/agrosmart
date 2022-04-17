from flask import Flask, render_template, request, jsonify, redirect, url_for
import RPi.GPIO as GPIO
import mh_z19
import board
import adafruit_dht
import datetime
import signal
import json
import os
import os.path
import time
from threading import Timer

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Relay(object):
    pin = 0

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def __init__(self, pin):
        self.pin = int(pin)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

SETTINGS_PATH = '/home/pi/main/static/data/settings.json'
UPDATE_PATH = '/home/pi/main/static/data/update.json'

Relay1 = Relay(26)
Relay2 = Relay(20)
Relay3 = Relay(21)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # датчик уровня воды
                                                    # датчик CO2 к BCM-12
dht_device = adafruit_dht.DHT22(board.D4)           # датчик температуры\влажности

def setRelayMode(num, mode):
    settings = {}
    with open(SETTINGS_PATH, encoding='utf-8') as settingsFile:
        settings = json.load(settingsFile)
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as settingsFile:
        settings['r' + str(num)] = mode
        json.dump(settings, settingsFile, ensure_ascii=False, indent=4)


def startup():
    if not os.path.isfile(SETTINGS_PATH):
        start_setting = {
            'r1': "-1",
            'r1b': '08:00',
            'r1e': '18:00',
            'r2': "-1",
            'r2b': '08:00',
            'r2e': '18:00',
            'r3': "-1",
            'r3b': '08:00',
            'r3e': '18:00',
            'co2b': '300',
            'co2e': '1500',
            'humb': '30',
            'hume': '70',
            'temb': '15',
            'teme': '40',
        }
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(start_setting, f, ensure_ascii=False, indent=4)

    if not os.path.isfile(UPDATE_PATH):
        start_data = {
            'wat': '-',
            'co2': '-',
            'hum': '-',
            'tmp': '-',
            'cod': '-',
            'cpu': 0,
            'volt': 0,
            'upt': 0,
            'dat': "",
            'tim': "",
        }
        with open(UPDATE_PATH, 'w', encoding='utf-8') as f:
            json.dump(start_data, f, ensure_ascii=False, indent=4)

startup()

app = Flask(__name__)

start_time = datetime.datetime.today()
month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']


def process():
    today = datetime.datetime.today()
    diff = today - start_time
    today = today.timetuple()

    newData = {}

    with open(SETTINGS_PATH, encoding='utf-8') as settingsFile:
        settings = json.load(settingsFile)
        now = datetime.time(today.tm_hour, today.tm_min)
        # print(settings)

        if settings['r1'] == "1":
            Relay1.on()
        elif settings['r1'] == "0":
            begin = datetime.datetime.strptime(settings['r1b'], "%H:%M").time()
            end = datetime.datetime.strptime(settings['r1e'], "%H:%M").time()
            if now >= begin and now < end:
                Relay1.on()
            else:
                Relay1.off()
        else:
            Relay1.off()

        if settings['r2'] == "1":
            Relay2.on()
        elif settings['r2'] == "0":
            begin = datetime.datetime.strptime(settings['r2b'], "%H:%M").time()
            end = datetime.datetime.strptime(settings['r2e'], "%H:%M").time()
            if now >= begin and now < end:
                Relay2.on()
            else:
                Relay2.off()
        else:
            Relay2.off()

        if settings['r3'] == "1":
            Relay3.on()
        elif settings['r3'] == "0":
            begin = datetime.datetime.strptime(settings['r3b'], "%H:%M").time()
            end = datetime.datetime.strptime(settings['r3e'], "%H:%M").time()
            if now >= begin and now < end:
                Relay3.on()
            else:
                Relay3.off()
        else:
            Relay3.off()

    try:
        newData = {
            'wat': GPIO.input(17) == GPIO.HIGH,
            'co2': mh_z19.read_from_pwm(),
            'hum': dht_device.humidity,
            'tmp': dht_device.temperature,
            'cod': os.popen('vcgencmd get_throttled').readline().replace("throttled=", "").replace("\n", ""),
            'cpu': os.popen('vcgencmd measure_temp').readline().replace("temp=", "").replace("'C\n", ""),
            'volt':os.popen('vcgencmd measure_volts core').readline().replace("volt=", "").replace("V\n", ""),
            'upt': diff.days * 24 + diff.seconds / 3600,
            'dat': str(today.tm_mday) + " " + month_list[int(today.tm_mon) - 1] + " " + str(today.tm_year),
            'tim': now.strftime("%H:%M"),
        }
    except Exception as e:
        print()
        print('Ошибка чтения значений')
        print(e)
        print()
    else:
        with open(UPDATE_PATH, 'w', encoding='utf-8') as f:
            json.dump(newData, f, ensure_ascii=False, indent=4)
            print("update.json dumped")
    finally:
        Timer(3, process).start()


Timer(3, process).start()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def static_dir(path):
    return send_from_directory("static", path)


@app.route("/settings")
def settings():
    template_data = {}
    with open(SETTINGS_PATH, encoding='utf-8') as settingsFile:
        template_data = json.load(settingsFile)

    return render_template('settings.html', **template_data)


@app.route('/setup', methods=['POST'])
def handle_data():
    settings = {}
    with open(SETTINGS_PATH, encoding='utf-8') as settingsFile:
        settings = json.load(settingsFile)
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as settingsFile:
        settings['r1b'] = request.form['relay1-begin']
        settings['r1e'] = request.form['relay1-end']
        settings['r2b'] = request.form['relay2-begin']
        settings['r2e'] = request.form['relay2-end']
        settings['r3b'] = request.form['relay3-begin']
        settings['r3e'] = request.form['relay3-end']
        settings['co2b'] = request.form['co2-begin']
        settings['co2e'] = request.form['co2-end']
        settings['humb'] = request.form['humidity-begin']
        settings['hume'] = request.form['humidity-end']
        settings['temb'] = request.form['temperature-begin']
        settings['teme'] = request.form['temperature-end']
        json.dump(settings, settingsFile, ensure_ascii=False, indent=4)
    return redirect(url_for('settings'))


@app.route('/relay1/<mode>')
def relay1_switch(mode):
    setRelayMode(1, mode)
    return '', 200


@app.route('/relay2/<mode>')
def relay2_switch(mode):
    setRelayMode(2, mode)
    return '', 200


@app.route('/relay3/<mode>')
def relay3_switch(mode):
    setRelayMode(3, mode)
    return '', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
