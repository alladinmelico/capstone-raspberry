import evdev
from evdev import categorize, ecodes
import requests


class Device():
    name = 'Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader'
    url = 'http://localhost:5000'
    @classmethod
    def list(cls, show_all=False):
        # list the available devices
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        if show_all:
            for device in devices:
                print("event: " + device.fn, "name: " + device.name, "hardware: " + device.phys)
        return devices

    @classmethod
    def connect(cls):
        # connect to device if available
        try:
            device = [dev for dev in cls.list() if cls.name in dev.name][0]
            device = evdev.InputDevice(device.fn)
            return device
        except IndexError:
            print("Device not found.\n - Check if it is properly connected. \n - Check permission of /dev/input/ (see README.md)")
            exit()

    @classmethod
    def run(cls):
        device = cls.connect()
        container = []
        device.grab()
        # bind the device to the script
        print("RFID scanner is ready....")
        print("Press Control + c to quit.")
        for event in device.read_loop():
            # enter into an endeless read-loop
            if event.type == ecodes.EV_KEY and event.value == 1:
                digit = evdev.ecodes.KEY[event.code]
                if digit == 'KEY_ENTER':
                    # create and dump the tag
                    tag = "".join(i.strip('KEY_') for i in container)
                    print('tag', tag)
                    if (len(tag) >= 10): 
                        try:
                            requests.get('http://localhost:5000/check' + '?tag=' + tag)
                        except Exception:
                            print ('RFID unable to connect to the local server')
                    container = []
                else:
                    container.append(digit)

Device.run()