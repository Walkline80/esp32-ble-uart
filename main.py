"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/esp32-ble-uart
"""
import ubluetooth as bt
from ble.ble_uart import BLEUART

def demo():
	from machine import Pin

	def rx_callback(data):
		print("rx received: {}".format(data))

		led.value(1 if data == b'on' else 0)
		uart.send("on" if led.value() else "off")

	def button_callback(pin):
		led.value(not led.value())
		uart.send("on" if led.value() else "off")

	ble = bt.BLE()
	uart = BLEUART(ble, rx_callback)

	led = Pin(2, Pin.OUT, value=0)
	button = Pin(0, Pin.IN, Pin.PULL_UP)

	button.irq(button_callback, Pin.IRQ_RISING)


if __name__ == "__main__":
	demo()
