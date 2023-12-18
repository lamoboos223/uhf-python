import serial
import binascii
import re
import threading

# Serial port configuration
port = 'COM3'
baud_rate = 115200  # Replace with the correct baud rate
pattern = r"AA 02 [A-F0-9\s]+? DD"  # Updated pattern with a non-greedy quantifier
epc_pattern = r"E2[\w\s]{34}\b"  

# Create a serial connection with a timeout of 1 second
ser = serial.Serial(
    port=port,
    baudrate=baud_rate,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Send the single polling instruction
# 0xA28 -> 26 dBm
ser.write(bytes.fromhex('AA 00 B7 00 00 B7 DD')) # get transmittion power
ser.write(bytes.fromhex('AA 00 B6 00 02 0A 28 8F DD')) # set transmittion power
ser.write(bytes.fromhex('AA 00 AB 00 01 03 AC DD')) # set frequency to EU Standards
ser.write(bytes.fromhex('AA 00 27 00 03 22 27 10 83 DD')) # read tag
# Function to read RFID cards
def read_rfid_cards():
    counter = 1
    while True:
        response = ser.read(30)  # Adjust the buffer size to match the EPC length when it's a successful reading
        # Extract the EPC value from the notification frame
        response_hex = binascii.hexlify(response).decode().upper()
        response_formatted = ' '.join(response_hex[i:i + 2] for i in range(0, len(response_hex), 2))
        if response_formatted.startswith("AA 02"):
            match = re.search(pattern, response_formatted)
            if match:
                extracted_string = match.group(0)
                # print(f"full frame: {extracted_string}")
                match2 = re.search(epc_pattern, extracted_string)
                if match2:
                    epc = match2.group(0)
                    print(f"Counter: {counter}\tEPC: {epc}")
                    counter = counter + 1
        elif(response_formatted.startswith("AA 01 AB 00")):
            print(response_formatted)

# Create and start the thread for reading RFID cards
rfid_thread = threading.Thread(target=read_rfid_cards)
rfid_thread.start()

# Main thread continues execution
# You can add other code here if needed

# Wait for the RFID thread to finish (optional)
rfid_thread.join()

