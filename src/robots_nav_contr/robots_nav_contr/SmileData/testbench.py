#!/usr/bin/env python3
import smile_Subscriber
import time


values = smile_Subscriber.SerialHandler('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-port0', "9600")

data_ = values.read_from_serial()

while True:
    print("Data =  ", data_)
    time.sleep(2)