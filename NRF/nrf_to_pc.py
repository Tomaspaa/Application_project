import asyncio
from datetime import datetime
from bleak import BleakScanner, BleakClient, BleakError

# Bluetooth device MAC address
device_address = "D0:0F:5D:7D:BD:E8"

# Variable to track whether the device is connected
device_connected = False

sensor_values_queue = asyncio.Queue()

# List to store four sensor values
sensor_values = []

# File path to save the data
txt_file_path = "vastaanotetut_datat2.txt"

# Function to save sensor data to a text file
def save_sensor_data_to_txt(sensor_data):
    try:
        with open(txt_file_path, "a") as file:
            timestamp = datetime.now()
            line = f"{timestamp} {sensor_data[0]} {sensor_data[1]} {sensor_data[2]} {sensor_data[3]}\n"
            file.write(line)

        print("Data saved to text file.")
    except Exception as e:
        print(f"Error saving data to text file: {e}")

# Callback function for notifications
def notification_callback(sender: int, data: bytearray):
    global device_connected, sensor_values

    # Extract sensor data and save it to a text file
    sensor_data = int.from_bytes(data, byteorder='little')
    sensor_values.append(sensor_data)
    print(sensor_data)
    asyncio.ensure_future(sensor_values_queue.put(sensor_data))
    asyncio.ensure_future(save_sensor_data_to_txt(sensor_data))  # Save to text file

# Function to connect to the device and set up notifications
async def connect_and_setup_notifications(device_address):
    global device_connected
    if device_connected == False:
        try:
            async with BleakClient(device_address) as client:
                # Enable notifications for the characteristic
                await client.start_notify("00001526-1212-efde-1523-785feabcd123", notification_callback)

                print("Connected to the device.")
                device_connected = True

                # Wait for notifications for some time
                await asyncio.sleep(10)  # Adjust the sleep duration as needed

                # Stop notifications
                await client.stop_notify("00001526-1212-efde-1523-785feabcd123")

        except BleakError as e:
            print(f"Error connecting to the device: {e}")
            device_connected = False

# Function to periodically save sensor values to a text file
async def save_sensor_values():
    global sensor_values

    while True:
        await asyncio.sleep(0.5)
        if len(sensor_values) >= 4:
            print("Saving sensor data to text file...")
            save_sensor_data_to_txt(sensor_values[-4:])  # Save the last four values
            sensor_values = []  # Clear the list for the next set of values

# Main loop
async def run():
    global device_connected

    while True:
        print("Scanning for devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            if device.address == device_address and not device_connected:
                print("Device Found:", device.address)
                print("RSSi:", device.rssi)

                # Attempt to connect to the device and set up notifications
                await connect_and_setup_notifications(device_address)

# Run the main loop
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(run())
    asyncio.ensure_future(save_sensor_values())
    loop.run_forever()
except KeyboardInterrupt:
    print("Program stopped.")
finally:
    loop.close()
