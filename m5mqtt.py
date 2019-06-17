import m5base
import machine
from m5stack import lcd
from lib.wifiCfg import autoConnect
from lib.wifiCfg import wlan_sta, reconnect
from simple import MQTTClient
import _thread
import time

class M5mqtt:
    
    def __init__(self, client_id, server, port, user=None, password=None, keepalive=300):
        if m5base.get_start() != 1:
            autoConnect(lcdShow=True)
            lcd.clear()
        else:
            raise ImportError('mqtt need download...')

        if user == '':
            user = None
        
        if password == '':
            password = None

        self.mqtt = MQTTClient(client_id, server, port, user, password, keepalive)
        self.mqtt.set_callback(self._on_data)
        try:
            self.mqtt.connect()
        except:
            lcd.clear()
            lcd.font(lcd.FONT_DejaVu24)
            lcd.setTextColor(lcd.RED)
            lcd.print('connect fail', lcd.CENTER, 100)
        self.topic_callback = {}
        self.mqttState = True
        self.ping_out_time = time.ticks_ms() + 60000

    def _msg_deal(self, param):
        state, msg = self.mqtt.topic_get()
        if state == 0:
            pass
        elif state == 1:
            # receive req
            self.ping_out_time = time.ticks_ms() + 60000
        elif state == 2:
            self.ping_out_time = time.ticks_ms() + 60000
            topic = msg[0] if type(msg[0]) == str else msg[0].decode('utf-8')
            data = self.mqtt.topic_msg_get(msg[1])
            self._on_data(topic, data.decode())

    def _on_data(self, topic, data):
        self.topic_callback[topic](data)

    def on_connect(self):
        for i in self.topic_callback.keys():
            self.mqtt.subscribe(i)

    def _daemonTask(self):
        timeBegin = time.ticks_ms()
        while True:
            if time.ticks_ms() - timeBegin > 10000:
                timeBegin = time.ticks_ms()
                try:
                    if self.mqtt.ping():
                        self.ping_out_time = time.ticks_ms() + 2000
                    else:
                        self.mqttState = False
                        self.mqtt.lock_msg_rec()
                except:
                    self.mqttState = False
                    self.mqtt.lock_msg_rec()
  
            # ping ok, but not receive req
            if time.ticks_ms() > self.ping_out_time:
                self.mqttState = False
                self.mqtt.lock_msg_rec()
                          
            if self.mqttState == False:
                if wlan_sta.isconnected():
                    try:
                        self.mqtt.set_block(True)
                        self.mqtt.connect()
                        self.on_connect()
                        self.mqtt.set_block(False)
                        self.mqtt.unlock_msg_rec()
                        self.mqttState = True
                        self.ping_out_time = time.ticks_ms() + 60000
                    except Exception as e:
                        pass
                else:
                    reconnect()

            self._msg_deal(1)
            time.sleep_ms(100)

    def start(self):
        _thread.start_new_thread(self._daemonTask, ())

    def subscribe(self, topic, callback):
        self.mqtt.subscribe(topic)
        self.topic_callback[topic] = callback

    def unsubscribe(self, topic):
        pass

    def publish(self, topic, data):
        if type(topic) is int:
            topic = str(topic)
        if type(data) is int:
            data = str(data)
        if self.mqttState:
            try:
                self.mqtt.publish(topic, data)
            except:
                self.mqttState = False