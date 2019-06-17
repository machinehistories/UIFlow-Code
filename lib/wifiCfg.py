import network, json, machine, time
from m5stack import lcd, btnA, btnB, btnC
from uiflow import cfgRead
from uiflow import cfgWrite

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)

def screenShow():
	lcd.font(lcd.FONT_Default)
	lcd.setColor(0xCCCCCC, 0)
	lcd.rect(0, 210, 320, 30, lcd.BLACK, lcd.BLACK)
	message = 'reconnect'
	lcd.text(62 - int(lcd.textWidth(message) / 2), 235 - lcd.fontSize()[1], message)
	message = 'set wifi'
	lcd.text(253 - int(lcd.textWidth(message) / 2), 235 - lcd.fontSize()[1], message)

_reconnectTime = 0
_reconnectState = True
def reconnect(block=False):
	global _reconnectTime, _reconnectState
	if wlan_sta.isconnected():
		return True
		
	if time.ticks_ms() > _reconnectTime:
		if wlan_sta.isconnected():
			return True

		if _reconnectState == True:
			_reconnectState = False
			_reconnectTime = time.ticks_ms() + 1000
			print("disconnect, wait next ...")
			wlan_sta.disconnect()
			return False

		_reconnectTime = time.ticks_ms() + 15000
		_reconnectState = True

		if not wlan_sta.isconnected():
			wlan_sta.active(True)
			jdata = cfgRead('wifi')
			if jdata:
				wlan_sta.connect(jdata['ssid'], jdata['password'])
		return True
	else:
		return False

def doConnect(ntwrk_ssid, netwrk_pass, lcdShow=False):
	if lcdShow:
		lcd.font(lcd.FONT_DejaVu18)
		lcd.setCursor(0, 0)
		lcd.rect(0, 0, 320, 210, lcd.BLACK, lcd.BLACK)
	if not wlan_sta.isconnected():
		wlan_sta.active(True)
		print('Connect Wi-Fi: SSID:'+ntwrk_ssid+' PASSWD:'+netwrk_pass+' network...')
		wlan_sta.connect(ntwrk_ssid, netwrk_pass)
		if lcdShow:
			lcd.println('Connect WiFi: \r\nWiFi SSID:'+ntwrk_ssid)
			lcd.print('Connecting.')
		a=0
		while not wlan_sta.isconnected() | (a > 20) :
			time.sleep_ms(500)
			a+=1
			print('.', end='')
			if lcdShow:
				lcd.print('.',wrap=1)
		if wlan_sta.isconnected():
			print('\nConnected. Network config:', wlan_sta.ifconfig())
			if lcdShow:
				lcd.println("Connected! \r\nNetwork config:\r\n"+wlan_sta.ifconfig()[0]+', '+wlan_sta.ifconfig()[3])
			saveWiFi(ntwrk_ssid, netwrk_pass)
			return (True)
		else : 
			print('\nProblem. Not Connected to :'+ntwrk_ssid)
			if lcdShow:
				lcd.println('.',wrap=1)
				lcd.println('Problem. Not Connected to :'+ntwrk_ssid)
			wlan_sta.disconnect()
			return (False)
	return (True)

def autoConnect(lcdShow=False):
	if lcdShow:
		screenShow()
	try:
		if not wlan_sta.isconnected():
			jdata = cfgRead('wifi')
			ssid = jdata['ssid']
			passwd = jdata['password']
			if ssid == '' and passwd == '':
				history = machine.nvs_getstr('history')
				if history != None:
					data = json.loads(history)
					ssid = data[-1][0]
					passwd = data[-1][1]
					jdata['ssid'] = ssid
					jdata['password'] = passwd
					cfgWrite('wifi', jdata)
				else:
					raise OSError
			if doConnect(ssid, passwd, lcdShow):
				return (True)
			print('connect fail!')

			if not wlan_sta.isconnected():
				while True:
					time.sleep_ms(20)
					if btnA.wasReleased():
						if doConnect(ssid, passwd, lcdShow):
							return (True)
					elif btnC.wasPressed():
						wlan_sta.disconnect()
						import wifiWebCfg
						wifiWebCfg.webserver_start()
		else:
			return (True)
	except OSError:
		# Web server for connection manager
		import wifiWebCfg
		wifiWebCfg.webserver_start()

def saveWiFi(ssid, password):
	ssidMap = {}
	ssidMap['ssid'] = ssid
	ssidMap['password'] = password

	cfgWrite('wifi', ssidMap)

	change = False
	wifi_history = machine.nvs_getstr("history")
	
	if wifi_history != None:
		wifi_history = json.loads(wifi_history)
		for i in wifi_history:
			if i[0] == ssid:
				i[1] = password
				change = True
				break
		if not change:
			if len(wifi_history) == 4:
				wifi_history.pop(0)
			wifi_history.append([ssid, password])
	else:
		wifi_history = [[ssid, password]]
	
	machine.nvs_setstr('history', json.dumps(wifi_history))

def isconnected():
	return wlan_sta.isconnected()
