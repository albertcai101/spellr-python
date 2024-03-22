import serial
import time

# Adjust the serial port to match your setup
ser = serial.Serial('/dev/tty.usbmodem145460101', 9600)

def listen_for_commands():
    running = False
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  # Read the next line from the serial port
            if line == "GO":
                running = True
                print("Received 'GO' command. Starting to print analog readings...")
            elif line == "STOP":
                running = False
                print("Received 'STOP' command. Stopping.")
            elif running:
                # If we're in "running" mode and the line isn't a command, print it
                print(line)

        # It's important to have a small delay to avoid overwhelming the CPU
        time.sleep(0.001)

if __name__ == "__main__":
    listen_for_commands()
