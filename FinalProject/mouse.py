from pynput.mouse import Controller, Button
import time
import random
mouse = Controller()

while True:
    mouse.click(Button.left, 1)
    print('clicked')
    time.sleep(random.randint(5, 20))

 