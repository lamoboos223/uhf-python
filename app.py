import serial
import binascii
import time
import re


# Serial port configuration
port = 'COM3'
baud_rate = 115200  # Replace with the correct baud rate
pattern = r"AA 02 [A-F0-9\s]+? DD"  # Updated pattern with a non-greedy quantifier
epc_pattern = r"E2[\w\s]{34}\b"  

# Create a serial connection with a timeout of 1 second
ser = serial.Serial(
    port=port,
    baudrate= baud_rate,
    parity= serial.PARITY_NONE,
    stopbits= serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Send the single polling instruction
instruction = bytes.fromhex('AA 00 27 00 03 22 27 10 83 DD')  # Command frame for single polling instruction
ser.write(instruction)
while True:
    response = ser.read(1024)  # Adjust the buffer size (e.g., 1024) based on your requirements
    # Extract the EPC value from the notification frame
    response_hex = binascii.hexlify(response).decode().upper()
    response_formatted = ' '.join(response_hex[i:i+2] for i in range(0, len(response_hex), 2))

    if "AA 02" in response_formatted:
        match = re.search(pattern, response_formatted)
        if match:
            extracted_string = match.group(0)
            print(f"full frame: {extracted_string}")
            match2 = re.search(epc_pattern, extracted_string)
            if match2:
                extracted_string = match2.group(0)
                print(f"tag: {extracted_string}")
    else:
        print("No tag found or invalid response.")
    time.sleep(1)
