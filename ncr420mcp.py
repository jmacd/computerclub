# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP3426
# This code is designed to work with the MCP3426_I2CADC I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=MCP3426_I2CADC#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(2)

# MCP3426 address, 0x68(104)
# Send configuration command
#		0x10(16)	Continuous conversion mode, Channel-1, 12-bit Resolution

bus.write_byte(0x68, 0x19)

time.sleep(0.5)
# MCP3426 address, 0x68(104)
# Read data back from 0x00(0), 2 bytes
# raw_adc MSB, raw_adc LSB
data = bus.read_i2c_block_data(0x68, 0x00, 2)

raw_adc = (data[0] * 256) + data[1]

# Output data to screen
print("Digital Value of Analog Input is : %d" % raw_adc)
