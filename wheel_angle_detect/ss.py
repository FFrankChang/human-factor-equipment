from pymodbus.client import ModbusSerialClient


# create client object
client = ModbusSerialClient("com5")

# connect to device
client.connect()

# set/set information for as many times as needed
rr = client.read_coils(0x01)
# client.write_coil(0x01, values)
print(rr)
# disconnect device
client.close()