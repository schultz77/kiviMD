import machine
import time

vsysChannel = machine.ADC(29)  # Pin 29 corresponds ADC 3
maxInputVoltage = 3.3
adcRange = 65535 # 2^16

while True:
  adcReading = vsysChannel.read_u16()
  adcVoltage = (adcReading * maxInputVoltage) / adcRange
  vsysVoltage = adcVoltage * 3 # ADC Voltage is divided by 3 after reading
  print(vsysVoltage)
