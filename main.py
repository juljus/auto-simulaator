import serial
import pyautogui
import time

serial_port = '/dev/tty.usbmodem1101' # Siia peab kirjutama oma arduino porti. Hiljem võib ka testida, find_arduino.py abil, mis port see on.
baud_rate = 9600

# Tee jada side lahti
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def process_message(message):
    try:
        number, function = message.decode().strip().split(' ')
        try:
            delay = 1/float(number) 
        except:
            delay = 0

        # TODO! Lisada teised funktsioonid
        key = ''
        if function == 'r':
            if delay<0:
                key = 'right'
            elif delay > 0:
                key = 'left'
        elif function == 'p':
            key = 'down'
        # elif function == 'g':
        #     key = 'up'
        else:
            key = None
        return abs(delay), key
            
    except ValueError:
        print("Invalid message format. Frequency should be a number.")
        return None, None

if __name__ == "__main__":
    try:
        multiplier = 1
        last_update = time.time()
        last_key = None
        while True:
            message = ser.readline()
            
            delay, key = process_message(message)
            try:
                if last_update + delay*multiplier < time.time():
                    pyautogui.press(key)
                    # peab veel proovima kuidas seda paremini teha keyup/down kasutades
                    # if last_key is not None:
                    #     pyautogui.keyUp(last_key)
                    # pyautogui.keyDown(key)
                    last_key = key
                    last_update = time.time()
                    ser.flush() # To avoid buffer overflow
            except KeyboardInterrupt:
                print("KeyboardInterrupt: Stopping the script.")
                break
            except:
                print("No key to release")
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the script.")
    finally:
        ser.close()
