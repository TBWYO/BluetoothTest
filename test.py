import asyncio
import bleak
from BluetoothModule import BluetoothHandler

async def main():
    # Create a BluetoothHandler instance
    handler = BluetoothHandler()

    # Connect to the BLE device
    device_address = "00:11:22:33:44:55"
    device = await handler.connect_device(device_address)
    if device is not None:
        print(f"Connected to device {device_address}")
    else:
        #print(f"Failed to connect to device {device_address}")
        return

    # Send a byte of data to the UART TX characteristic
    uart_service_uuid = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    uart_tx_char_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    value_to_send = b"T"
    await handler.write_characteristic(device, uart_service_uuid, uart_tx_char_uuid, value_to_send)
    print(f"Wrote to characteristic {uart_tx_char_uuid} value: {value_to_send}")

    # Receive a byte of data from the UART RX characteristic
    uart_rx_char_uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
    value_received = await handler.read_characteristic(device, uart_service_uuid, uart_rx_char_uuid)
    if value_received is not None:
        print(f"Read from characteristic {uart_rx_char_uuid} value: {value_received}")
    else:
        print(f"Failed to read characteristic {uart_rx_char_uuid}")

# Run the main() coroutine in the event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
