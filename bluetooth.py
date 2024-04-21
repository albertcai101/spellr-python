import serial
import time

# The port and baud rate
# need to forget the device to properly connect
bluetoothSerialPort = '/dev/tty.HC-05'
baudRate = 9600

try:
    bluetoothSerial = serial.Serial(bluetoothSerialPort, baudRate)
    print("Connected to Bluetooth device on", bluetoothSerialPort)

    while True:
        # Read a single byte
        if bluetoothSerial.inWaiting() > 0:
            receivedData = bluetoothSerial.read().decode() # Read and decode a single byte
            print(receivedData, end='', flush=True) # Print the received byte without adding a newline

except serial.SerialException as e:
    print("Could not connect to Bluetooth device:", e)

except KeyboardInterrupt:
    print("\nDisconnected from Bluetooth device.")

finally:
    if 'bluetoothSerial' in locals() or 'bluetoothSerial' in globals():
        bluetoothSerial.close()
