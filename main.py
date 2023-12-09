import serial
import pyautogui
import time

# Siia peab kirjutama oma arduino porti. Hiljem võib ka testida, find_arduino.py abil, mis port see on.
serial_port = 'COM14'
baud_rate = 9600

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
                delay *= fixing_positive
            elif delay > 0:
                key = 'd'
                delay *= fixing_negative
        elif function == 'p':
            key = 's'
        elif function == 'g':
            key = 'w'
        else:
            key = None
        return abs(delay), key

    except ValueError:
        return None, None


if __name__ == "__main__":
    try:
        multiplier = 1
        delay_threshold = 30
        last_update = time.time()
        last_key = 'a'
        while True:
            message = ser.readline()

            delay, key = process_message(message)
            if delay == None or key == None:
                pass
            try:
                # if last_update + delay*multiplier < time.time():
                # pyautogui.press(key)
                # peab veel proovima kuidas seda paremini teha keyup/down kasutades
                print(delay, key, last_key)
                if key == 'w':
                    pyautogui.keyDown(key)
                    pyautogui.keyUp('s')
                elif key == 's':
                    pyautogui.keyDown(key)
                    pyautogui.keyUp('w')
                elif last_key is not None and delay < delay_threshold:
                    pyautogui.keyUp(last_key)
                    last_key = key
                if last_key != key:
                    pyautogui.keyDown(key)
                # last_update = time.time()
                ser.flush()  # To avoid buffer overflow
                ser.reset_input_buffer()  # To avoid buffer overflow
                ser.reset_output_buffer()  # To avoid buffer overflow
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
