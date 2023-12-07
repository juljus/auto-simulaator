import serial
import pyautogui
import time

serial_port = 'COM14' # Siia peab kirjutama oma arduino porti. Hiljem võib ka testida, find_arduino.py abil, mis port see on.
baud_rate = 9600

# Tee jada side lahti
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def process_message(message):
    try:
        # print(message)
        # print(message.decode().strip())
        delay, function = message.decode().strip().split(' ')
        delay = float(delay) 
        
        # TODO! Lisada teised funktsioonid
        key = 'right'
        if function == 'r':
            if delay<0:
                key = 'left'
        elif function == 'p':
            key = 'down'
        else:
            key = None
        return delay, key
            
    except ValueError:
        print("Invalid message format. Frequency should be a number.")

if __name__ == "__main__":
    try:
        last_update = time.time()
        last_key = None
        while True:
            message = ser.readline()
            
            delay, key = process_message(message)
            try:
                if last_update + delay < time.time():
                    if last_key is not None:
                        pyautogui.keyUp(last_key)
                    pyautogui.keyDown(key)
                    last_key = key
                    last_update = time.time()
            except:
                print("No key to release")
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the script.")
    finally:
        ser.close()
