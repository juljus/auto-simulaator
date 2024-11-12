import serial
from pynput.keyboard import Controller
import time

# Constants
rool_neutral = 40

# Siia peab kirjutama oma arduino porti. Hiljem võib ka testida, find_arduino.py abil, mis port see on.
serial_port = '/dev/tty.usbmodem101'
baud_rate = 9600

keyboard = Controller()
# Tee jada side lahti
ser = serial.Serial(serial_port, baud_rate, timeout=1)


def process_message(message):
    try:
        print("message: " + message.decode())
        number, function = message.decode().strip().split(' ')
        print("number: " + number, "; function: " + function)

        key = ''
        number = int(number)
        if function == 'r':
            if number < -rool_neutral:
                key = 'a'
            elif number > rool_neutral:
                key = 'd'
            else:
                key = 'neutral'
        elif function == 'p':
            key = 's'
        elif function == 'g':
            key = 'w'
        elif function == 'n':
            key = 'up'

        return key, abs(number)

    except ValueError:
        print("ValueError: Could not split the message.")
        return None, None


if __name__ == "__main__":
    try:
        while True:
            message = ser.readline()

            key, number = process_message(message)

            if number == None or key == None:
                pass
            else:
                try:
                    print("key: " + key, "; number: " + str(number))
                    if key == 'a':
                        keyboard.press(key)
                        keyboard.release('d')
                    elif key == 'd':
                        keyboard.press(key)
                        keyboard.release('a')
                    elif key == 'neutral':
                        keyboard.release('a')
                        keyboard.release('d')
                    elif key == 's':
                        keyboard.press(key)
                        keyboard.release('w')
                    elif key == 'w':
                        keyboard.press(key)
                        keyboard.release('s')
                    elif key == 'up':
                        keyboard.release('w')
                        keyboard.release('s')
                    else:
                        pass

                except KeyboardInterrupt:
                    print("KeyboardInterrupt: Stopping the script.")
                    break
                except:
                    pass

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the script.")
    finally:
        ser.close()
