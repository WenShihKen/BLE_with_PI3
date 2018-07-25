from __future__ import print_function
from bluepy import btle
import sys
import binascii
import os

ble_conn = None

class MyDelegate(btle.DefaultDelegate):

    def __init__(self, conn):
        btle.DefaultDelegate.__init__(self)
        self.conn = conn

    def handleNotification(self, cHandle, data):
        print("Notification:", str(cHandle), " data ", str(data))

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
        elif isNewData:
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))


def ble_connect(devAddr):
    global ble_conn
    if not devAddr is None and ble_conn is None:
        ble_conn = btle.Peripheral(devAddr, btle.ADDR_TYPE_PUBLIC)
        ble_conn.setDelegate(MyDelegate(ble_conn))
        print("connected")

def ble_disconnect():
    global ble_conn
    ble_conn = None
    print("disconnected")


if __name__ == '__main__':

    ble_mac = "BLE裝置的mac位置"

    # scan
    scanner = btle.Scanner().withDelegate(MyDelegate(None))
    timeout = 10.0
    devices = scanner.scan(timeout)
    for dev in devices:
        if dev.addr == ble_mac:
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print ("  %s(0x%x) = %s" % (desc, int(adtype), value))
            break

    # connect
    ble_connect(ble_mac)
    # wait notification
    while True:
        ble_conn.waitForNotifications(10.0)

    # disconnect
    ble_disconnect()