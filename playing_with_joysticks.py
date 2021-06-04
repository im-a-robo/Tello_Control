"""Simple example showing how to get gamepad events."""

from __future__ import print_function


from inputs import get_gamepad
from time import sleep

fps = 10

def main():
    """Just print out some event infomation when the gamepad is used."""
    while True:
        sleep(1 / fps)
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)


if __name__ == "__main__":
    main()