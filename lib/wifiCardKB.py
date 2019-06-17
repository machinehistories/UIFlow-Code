from m5ui import *
from m5stack import *
import unit
import time
from wifiCfg import wlan_sta, screenShow, doConnect, saveWiFi

setScreenColor(0x000000)
lcd.font(lcd.FONT_DejaVu24)
while True:
    try:
        card = unit.get(unit.CARDKB, unit.PORTA)
        break
    except:
        lcd.setTextColor(lcd.RED, lcd.BLACK)
        lcd.print("CardKB not connect..", lcd.CENTER, lcd.CENTER)
        btnText('A', '<--- connect here')

setScreenColor(0x000000)

def show_title():
    lcd.font(lcd.FONT_Comic)
    lcd.setTextColor(lcd.WHITE, lcd.ORANGE)
    lcd.rect(0, 0, 320, 30, lcd.ORANGE, lcd.ORANGE)
    lcd.print("Wi-Fi Config", lcd.CENTER, 2)
    lcd.setTextColor(lcd.WHITE, lcd.BLACK)

show_title()
label_ssid = M5TextBox(20, 70, "SSID:", lcd.FONT_DejaVu18, lcd.ORANGE, rotate=0)
ssid = M5TextBox(97, 70, "Scanning.....", lcd.FONT_DejaVu18, lcd.ORANGE, rotate=0)
rect = M5Rect(0, 130, 320, 3, 0xFFFFFF, 0xFFFFFF)
label_pwd = M5TextBox(20, 168, "PWD:", lcd.FONT_DejaVu18, lcd.ORANGE, rotate=0)
password = M5TextBox(97, 168, "", lcd.FONT_DejaVu18, lcd.ORANGE, rotate=0)

choose_circle = M5Circle(100, 38, 3, 0x00ff71, 0x00ff71)
choose_circle.hide()

lcd.font(lcd.FONT_Default)
btnText('A', "Connect")
btnText('B', "  SSID  ")
btnText('C', "Wi-Fi Scan")

pos_x_start = 110
pos_y_start = 34
pos_step = 15

page = 0
pos = 0

wifiList = None
link_pwd = ''
link_ssid = ''

def wifi_update():
    global wifiList
    wifiList = [i[0].decode() for i in wlan_sta.scan()]
    wifiList = [wifiList[i: i+6] for i in range(0, len(wifiList), 7)]

def pageUpdate():
    global pos
    pos = 0
    lcd.font(lcd.FONT_Default)
    lcd.rect(96, 31, 224, 99, lcd.BLACK, lcd.BLACK)
    for i in range(len(wifiList[page])):
        lcd.print(wifiList[page][i][:20], pos_x_start, pos_y_start + pos_step*i, lcd.WHITE)
    choose_circle.setPosition(y=pos_y_start + 4 + pos*15)

def ssid_loop():
    global pos, page, link_ssid, link_pwd
    pos = 0
    page = 0
    while True:
        if btnC.wasPressed():
            pos = pos + 1
            if pos >= len(wifiList[page]):
                page = page + 1
                if page >= len(wifiList):
                    page = 0
                pageUpdate()
            choose_circle.setPosition(y=pos_y_start + 4 + pos*15)
        if btnB.wasPressed():
            link_ssid = wifiList[page][pos]
            link_pwd = card.keyString
            break
        if btnA.wasPressed():
            pos = pos - 1
            if pos < 0:
                page = page - 1
                if page < 0:
                    page = len(wifiList) - 1
                pageUpdate()
                pos = len(wifiList[page]) - 1
            choose_circle.setPosition(y=pos_y_start + 4 + pos*15)
        password.setText(card.keyString)
        time.sleep_ms(10)

wifi_update()
ssid.setText(wifiList[0][0])
link_ssid = wifiList[0][0]

btnB._event |= 0x01

while True:
    if btnA.wasPressed():
        screenShow()
        link_pwd = card.keyString
        if doConnect(link_ssid, link_pwd, True):
            saveWiFi(link_ssid, link_pwd)
            import uiflow
            uiflow.start('flow')
            uiflow.modeSet('internet')
            import machine
            machine.reset()
        else:
            setScreenColor(0x000000)
            show_title()
            label_ssid.show()
            ssid.show()
            rect.show()
            label_pwd.show()
            password.show()
            lcd.font(lcd.FONT_Default)
            btnText('A', "Connect")
            btnText('B', "  SSID  ")
            btnText('C', "Wi-Fi Scan")
    if btnB.wasPressed():
        lcd.rect(96, 31, 224, 99, lcd.BLACK, lcd.BLACK)
        lcd.font(lcd.FONT_Default)
        pageUpdate()
        btnText('A', "   <<<   ")
        btnText('B', "Select")
        btnText('C', "     >>>       ")
        # press btnB exit
        ssid_loop()
        lcd.rect(96, 31, 224, 99, lcd.BLACK, lcd.BLACK)
        lcd.font(lcd.FONT_Default)
        btnText('A', "Connect")
        btnText('B', "  SSID  ")
        btnText('C', "Wi-Fi Scan")
        ssid.setText(wifiList[page][pos][:18])
        ssid.show()
    if btnC.wasPressed():
        ssid.setText('Scanning.....')
        wifi_update()
        btnB._event |= 0x01
        ssid.setText(wifiList[0][0])
        link_ssid = wifiList[0][0]
        link_pwd = card.keyString

    password.setText(card.keyString)
    time.sleep_ms(10)