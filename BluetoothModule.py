import asyncio
import bleak

class BluetoothHandler:
    def __init__(self):
        # Get the event loop for the current thread
        self.loop = asyncio.get_event_loop()
        # Create a dictionary to store discovered devices
        self.devices = {}

    async def scan_devices(self, timeout=5.0):
        # Clear the devices dictionary
        self.devices.clear()
        # Discover BLE devices within the specified timeout
        devices = await bleak.discover(timeout=timeout)
        # Add discovered devices to the devices dictionary
        for d in devices:
            self.devices[d.address] = d.name

    async def connect_device(self, address):
        try:
            # Connect to the specified BLE device
            device = await bleak.BleakClient(address).connect()
            return device
        except Exception as e:
            print(f"Failed to connect to device {address}: {str(e)}")
            return None

    async def read_characteristic(self, device, service_uuid, characteristic_uuid):
        try:
            # Read the specified characteristic from the device
            value = await device.read_gatt_char(characteristic_uuid, uuid=service_uuid)
            return value
        except Exception as e:
            print(f"Failed to read characteristic {characteristic_uuid}: {str(e)}")
            return None

    async def write_characteristic(self, device, service_uuid, characteristic_uuid, value):
        try:
            # Write the specified value to the specified characteristic on the device
            await device.write_gatt_char(characteristic_uuid, value, response=True, uuid=service_uuid)
        except Exception as e:
            print(f"Failed to write characteristic {characteristic_uuid}: {str(e)}")

    async def start_notifications(self, device, service_uuid, characteristic_uuid, callback):
        # Define a notification handler function that calls the specified callback function
        def notification_handler(sender, data):
            callback(data)
        # Start notifications for the specified characteristic on the device
        await device.start_notify(characteristic_uuid, notification_handler, uuid=service_uuid)

    async def stop_notifications(self, device, service_uuid, characteristic_uuid):
        # Stop notifications for the specified characteristic on the device
        await device.stop_notify(characteristic_uuid, uuid=service_uuid)
