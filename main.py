import serial
from pynput.keyboard import Controller
import time

# Siia peab kirjutama oma arduino porti. Hiljem võib ka testida, find_arduino.py abil, mis port see on.
serial_port = '/dev/tty.usbmodem1101'
baud_rate = 9600

keyboard = Controller()
# Tee jada side lahti
ser = serial.Serial(serial_port, baud_rate, timeout=1)


def process_message(message):
    try:
        # print(message.decode().strip())
        number, function = message.decode().strip().split(' ')
        try:
            delay = float(number)
        except:
            delay = 0

        # TODO! Lisada teised funktsioonid
        fixing_negative = 1 
        fixing_positive = 1
        key = ''
        if function == 'r':
            if delay < 0:
                key = 'a'
                delay *= fixing_negative
            elif delay > 0:
                key = 'd'
                delay *= fixing_positive
            else:
                key = 'up'
                delay = 0
        elif function == 'p':
            key = 's'
            delay = 0
        elif function == 'g':
            key = 'w'
            delay = 0
        else:
            key = None
        return abs(delay), key

    except ValueError:
        return None, None


if __name__ == "__main__":
    try:
        multiplier = 1
        delay_threshold = 40
        last_update = time.time()
        last_key = 'up'
        while True:
            #message = ser.readline()
            message = ser.readline()

            delay, key = process_message(message)
            if delay == None or key == None:
                pass
            else:
                try:
                    # if last_update + delay*multiplier < time.time():
                    # keyboard.press(key)
                    # peab veel proovima kuidas seda paremini teha release/down kasutades
                    #print(delay, key, last_key)
                    if key == 'w':
                        keyboard.press(key)
                        keyboard.release('s')
                    elif key == 's':
                        keyboard.press(key)
                        keyboard.release('w')
                    elif delay > delay_threshold:
                        if key == 'd':
                            #keyboard.press(key)
                            keyboard.press(key)
                            keyboard.release('a')
                            last_key = key
                        elif key == 'a':
                            #keyboard.press(key)
                            keyboard.press(key)
                            keyboard.release('d')
                            last_key = key
                    else:
                        keyboard.release('a')
                        keyboard.release('d')
                        #print(key)

                    # last_update = time.time()
                    #ser.flush()  # To avoid buffer overflow
                    #ser.reset_input_buffer()  # To avoid buffer overflow
                    #ser.reset_output_buffer()  # To avoid buffer overflow
                except KeyboardInterrupt:
                    print("KeyboardInterrupt: Stopping the script.")
                    break
                except:
                    # print("No key to release")
                    pass

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the script.")
    finally:
        ser.close()
