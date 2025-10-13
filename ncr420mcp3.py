'''**************************************************************************/

I2C 16-Bit 4-Channel Analog to Digital Converter I2C Mini Module

Firmware v1.0 - Python
Author - Yadwinder Singh

4-Channel ADC with 16-Bit Resolution
4 Differential Analog Inputs
Programmable x1-x8 Gain Amplifier
Upto 8 Devices per I2C Port
Up to 3.4MHz Communication Speed
0x68 I2C Start Address 

Hardware Version - Rev A.
Platform - Raspberry Pi

/**************************************************************************/'''
#Setting Up smbus libraries
import smbus
import time
bus = smbus.SMBus(2)



#MCP3426, MCP3427 & MCP3428 addresses are controlled by address lines A0 and A1
# each address line can be low (GND), high (VCC) or floating (FLT)
MCP3428_DEFAULT_ADDRESS                 = 0x68

# /RDY bit definition
MCP3428_CONF_NO_EFFECT                  = 0x00
MCP3428_CONF_RDY                        = 0x80

# Conversion mode definitions
MCP3428_CONF_MODE_ONESHOT               = 0x00
MCP3428_CONF_MODE_CONTINUOUS            = 0x10

# Channel definitions
#MCP3425 have only the one channel
#MCP3426 & MCP3427 have two channels and treat 3 & 4 as repeats of 1 & 2 respectively
#MCP3428 have all four channels
MCP3428_CHANNEL_1                       = 0x00
MCP3428_CHANNEL_2                       = 0x20
MCP3428_CHANNEL_3                       = 0x40
MCP3428_CHANNEL_4                       = 0x60


# Sample size definitions - these also affect the sampling rate
# 12-bit has a max sample rate of 240sps
# 14-bit has a max sample rate of  60sps
# 16-bit has a max sample rate of  15sps
MCP3428_CONF_SIZE_12BIT                 = 0x00
MCP3428_CONF_SIZE_14BIT                 = 0x04
MCP3428_CONF_SIZE_16BIT                 = 0x08
MCP3428_CONF_SIZE_18BIT                 = 0x0C

# Programmable Gain definitions
MCP3428_CONF_GAIN_1X                    = 0x00
MCP3428_CONF_GAIN_2X                    = 0x01
MCP3428_CONF_GAIN_4X                    = 0x02
MCP3428_CONF_GAIN_8X                    = 0x03

# Default :Channel 1,Sample Rate 15SPS(16- bit),Gain x1 Selected
#Default values for the sensor
# ready = MCP3428_CONF_RDY
# channel = MCP3428_CONF_CHANNEL_1
# mode = MCP3428_CONF_MODE_CONTINUOUS
# rate = MCP3428_CONF_SIZE_16BIT
# gain = MCP3428_CONF_GAIN_4X
VRef = 2.048 # 2.048 Volts


# Power on and prepare for general usage.
def initialize():
    byte = MCP3428_CONF_RDY | MCP3428_CONF_MODE_CONTINUOUS | MCP3428_CHANNEL_1 | MCP3428_CONF_SIZE_16BIT | MCP3428_CONF_GAIN_2X
    print("write byte %x" % byte)
    bus.write_byte(MCP3428_DEFAULT_ADDRESS, byte)

#In read mode ,it indicates the output register has been updated with a new conversion.
#In one-shot Conversion mode,writing Initiates a new conversion.

#Set Channel Selection
#C1-C0: Channel Selection Bits
#00 = Select Channel 1 (Default)
#01 = Select Channel 2
#10 = Select Channel 3 
#11 = Select Channel 4 
    
#Set Conversion Mode
#1= Continous Conversion Mode
#0 = One-shot Conversion Mode
        
#Set Sample rate selection bit
# 00 : 240 SPS-12 bits
# 01 : 60 SPS 14 bits
# 10 : 15 SPS 16 bits
        
#Set the PGA gain
# 00 : 1 V/V
# 01 : 2 V/V
# 10 : 4 V/V
# 11 : 8 V/V
   
#Get the measurement for the ADC values  from the register
#using the General Calling method

def getadcread() :
        data = bus.read_i2c_block_data(MCP3428_DEFAULT_ADDRESS,0x00,6)
        print("DATA", data)
        value = ((data[0] << 8) | data[1])
        if (value >= 32768):
                value = 65536 - value
        return value
        
# The output code is proportional to the voltage difference b/w two analog points
#Checking the conversion value
#Conversion of the raw data into 
# Shows the output codes of input level using 16-bit conversion mode

def getconvert():
        code = getadcread()
        print("Raw ADC: ", code)
        mA = 0.000688 * code
        print("mA: ", mA)

        #setSample(rate)
        N = 16 # resolution,number of bits
        voltage = (2 * VRef * code)/ (2**N)
        return voltage

#Initialising the Device.
# https://store.ncd.io/product/4-channel-i2c-4-20ma-current-receiver-with-i2c-interface/

# Note: Set MCP3428 gain to one to read 0-40mA Signal, set the gain at
# two to read 0-20mA and 4-20mA signals. Needs External Power Supply
# to power up the 4-20mA Device.
#
# When resolution is set to 16-bit:
#
#     at 4mA the raw ADC value will be around 5813
#     at 20mA the raw ADC value will be around 29390.

initialize()

while True:
        time.sleep(0.5)
        print( "                MCP3428 Readings ")

        voltage = getconvert()
        print( "\nVoltage of the source is :",voltage,"volts\n")
        print( "                **********************************\n")
