import serial
import binascii
import time

port = 'COM3'
baud_rate = 9600  # Replace with the correct baud rate

# Create a serial connection with a timeout of 1 second
ser = serial.Serial(
    port=port,
    baudrate= baud_rate,
    parity= serial.PARITY_NONE,
    stopbits= serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.close()
ser.open()

while True:
    data = str(binascii.hexlify(ser.read(17)))
    if data != "":
        print(f"tag: {data[6:22]}")
    else:
        print("no tag detected")
    time.sleep(1)