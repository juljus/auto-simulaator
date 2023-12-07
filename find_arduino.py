import serial.tools.list_ports

def find_arduino_port():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description
    ]
    if arduino_ports:
        return arduino_ports[0]
    else:
        return None

if __name__ == "__main__":
    arduino_port = find_arduino_port()
    if arduino_port:
        print(f"Arduino board is connected to port: {arduino_port}")
    else:
        print("Arduino board is not connected.")