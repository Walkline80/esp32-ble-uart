"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
Gitee: https://gitee.com/walkline/esp32-ble-uart
Original repo: https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_uart_peripheral.py
"""
import ubluetooth as bt
from ble.tools import BLETools
from ble.const import BLEConst

__UART_UUID = bt.UUID("512f4174-89ef-11ea-bc55-0242ac130003")
__TX_UUID = bt.UUID("d3c55e7a-89ef-11ea-bc55-0242ac130003")
__RX_UUID = bt.UUID("dd608f2c-89ef-11ea-bc55-0242ac130003")

__UART_SERVICE = (
	__UART_UUID,
	(
		(__TX_UUID, bt.FLAG_NOTIFY,),
		(__RX_UUID, bt.FLAG_WRITE,),
	),
)


class BLEUART:
	def __init__(self, ble, rx_callback=None, name="mpy-uart", rxbuf=100):
		self.__ble = ble
		self.__rx_cb = rx_callback
		self.__conn_handle = None

		self.__write = self.__ble.gatts_write
		self.__read = self.__ble.gatts_read
		self.__notify = self.__ble.gatts_notify

		self.__ble.active(False)
		print("activating ble...")
		self.__ble.active(True)
		print("ble activated")

		self.__ble.config(rxbuf=rxbuf)
		self.__ble.irq(handler=self.__irq)
		self.__register_services()

		self.__adv_payload = BLETools.advertising_generic_payload(
			services=(__UART_UUID,),
			appearance=BLEConst.Appearance.GENERIC_COMPUTER,
		)
		self.__resp_payload = BLETools.advertising_resp_payload(
			name=name
		)

		self.__advertise()

	def __register_services(self):
		(
			(
				self.__tx_handle,
				self.__rx_handle,
			),
		) = self.__ble.gatts_register_services((__UART_SERVICE,))

	def __advertise(self, interval_us=500000):
		self.__ble.gap_advertise(None)
		self.__ble.gap_advertise(interval_us, adv_data=self.__adv_payload, resp_data=self.__resp_payload)
		print("advertising...")

	def __irq(self, event, data):
		if event == BLEConst.IRQ.IRQ_CENTRAL_CONNECT:
			self.__conn_handle, addr_type, addr, = data
			print("[{}] connected, handle: {}".format(BLETools.decode_mac(addr), self.__conn_handle))

			self.__ble.gap_advertise(None)
		elif event == BLEConst.IRQ.IRQ_CENTRAL_DISCONNECT:
			self.__conn_handle, _, addr, = data
			print("[{}] disconnected, handle: {}".format(BLETools.decode_mac(addr), self.__conn_handle))

			self.__conn_handle = None
			self.__advertise()
		elif event == BLEConst.IRQ.IRQ_GATTS_WRITE:
			conn_handle, value_handle = data

			if conn_handle == self.__conn_handle and value_handle == self.__rx_handle:
				if self.__rx_cb:
					self.__rx_cb(self.__read(self.__rx_handle)) # .decode().strip())

	def write(self, data):
		"""
		将数据写入本地缓存，等待中心设备读取
		"""
		self.__write(self.__tx_handle, data)

	def send(self, data):
		"""
		将数据写入本地缓存，并推送到中心设备
		"""
		self.__write(self.__tx_handle, data)

		if self.__conn_handle is not None:
			self.__notify(self.__conn_handle, self.__tx_handle, data)


def demo():
	from machine import Pin

	def rx_callback(data):
		print("rx received: {}".format(data))

		led.value(1 if data == b'on' or data == b'\x01' else 0)
		uart.write("on" if led.value() else "off")

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
