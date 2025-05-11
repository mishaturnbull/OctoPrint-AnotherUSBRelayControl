import hid
import atexit

"""

This relay object uses the HID library instead of usb. 

Some scant details about the USB Relay
http://vusb.wikidot.com/project:driver-less-usb-relays-hid-interface

cython-hidapi module:
https://github.com/trezor/cython-hidapi

Installing the module:
sudo apt-get install python-dev libusb-1.0-0-dev libudev-dev
pip install --upgrade setuptools
pip install hidapi

A list of avaible methods for the hid object:
https://github.com/trezor/cython-hidapi/blob/6057d41b5a2552a70ff7117a9d19fc21bf863867/chid.pxd#L9

"""

class Relay(object):
        """docstring for Relay"""
        def __init__(self, idVendor=0x16c0, idProduct=0x05df):
                self.h = hid.device()
                self.h.open(idVendor, idProduct)
                self.h.set_nonblocking(1)
                atexit.register(self.cleanup)

        def cleanup(self):
            self.h.close()

        def state(self, relay, on=False):
                """

                Getter/Setter for the relay.  

                Getter - If only a relay is specified (with an int), then that relay's status 
                is returned.  If relay = 0, a list of all the statuses is returned.
                True = on, False = off.

                Setter - If a relay and on are specified, then the relay(s) status will be set.
                Either specify the specific relay, 1-8, or 0 to change the state of all relays.
                on=True will turn the relay on, on=False will turn them off.

                """

                # An integer can be passed instead of the a byte, but it's better to
                # use ints when possible since the docs use them, but it's not neccessary.
                # https://github.com/jaketeater/simpleusbrelay/blob/master/simpleusbrelay/__init__.py
                start = 0xA0
                state = 1 if on else 0
                cksum = start + relay + state
                message = [start, relay, state, cksum]

                self.h.write(message)

if __name__ == '__main__':
        from time import sleep

        # Create a relay object
        relay = Relay(idVendor=0x16c0, idProduct=0x05df)

        # (Setter) Turn switch 1 on
        relay.state(1, on=True)

        # (Getter) Print the status of switch 1
        print(relay.state(1))

        sleep(1)

        #relay.state(2, on=True)

        #print(relay.state(2))
        #sleep(1)

        # Turn all switches off
        relay.state(0, on=False)

        # Print the state of all switches
        print(relay.state(0))
