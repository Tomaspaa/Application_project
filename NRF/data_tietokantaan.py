from bleak import BleakScanner, BleakClient, BleakError
import asyncio
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("dotenv.env")
# Bluetooth device MAC address
device_address = "D0:0F:5D:7D:BD:E8"

# MySQL server details
mysql_host = os.getenv("DB_HOST")
mysql_user = os.getenv("DB_USER")
mysql_password = os.getenv("DB_PASSWORD")
mysql_database = os.getenv("DB_NAME")

# Variable to track whether the device is connected
device_connected = False

sensor_values_queue = asyncio.Queue()

# List to store four sensor values
sensor_values = []

# Function to save sensor data to MySQL
def save_sensor_data_to_mysql(sensor_data):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            autocommit=True 
        )
        print("Connected to MySQL.")

        cursor = connection.cursor()

        sql_query = "INSERT INTO rawdata (timestamp, groupid, from_mac, to_mac, sensorvalue_a, sensorvalue_b, sensorvalue_c, sensorvalue_d) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (datetime.now(), "16", "nrf5340", "rasp", sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3])
        cursor.execute(sql_query, values)

        '''    
        cursor.execute("INSERT INTO rawdata (timestamp, groupid, from_mac, to_mac, sensorvalue_a, sensorvalue_b, sensorvalue_c, sensorvalue_d) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                      (datetime.now(), "16", "	nrf5340", "rasp", sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3]))
        '''

        connection.commit()
        print("Data saved to MySQL database.")
    except Exception as e:
        print(f"Error saving data to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        
# Callback function for notifications
def notification_callback(sender: int, data: bytearray):
    global device_connected, sensor_values

    #print(f"Notification received: {data}")

    # Extract sensor data and save it to MySQL database

    sensor_data = int.from_bytes(data, byteorder='little')
    sensor_values.append(sensor_data)
    print(sensor_data)
    asyncio.ensure_future(sensor_values_queue.put(sensor_data))
# Function to connect to the device and set up notifications
async def connect_and_setup_notifications(device_address):
    global device_connected

    try:
        async with BleakClient(device_address) as client:
            # Enable notifications for the characteristic
            await client.start_notify("00001526-1212-efde-1523-785feabcd123", notification_callback)

            print("Connected to the device.")
            device_connected = True

            # Wait for notifications for some time
            await asyncio.sleep(60)  # Adjust the sleep duration as needed

            # Stop notifications
            await client.stop_notify("00001526-1212-efde-1523-785feabcd123")

    except BleakError as e:
        print(f"Error connecting to the device: {e}")
        device_connected = False
# Function to periodically save sensor values to MySQL
async def save_sensor_values():
    global sensor_values

    while True:
        await asyncio.sleep(0.5)
        if len(sensor_values) >= 4:
            print("Saving sensor data to MySQL...")
            save_sensor_data_to_mysql(sensor_values[-4:])  # Save the last four values
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
