import glob
import time
import Adafruit_ADS1x15

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

    return -1

def read_ph():
    # https://files.atlas-scientific.com/Gravity-pH-datasheet.pdf
    value = adc.read_adc(0, gain=GAIN)
    voltage = value * (3.3 / 32767) + 0.33
    ph = (-5.6548 * voltage) + 15.509

    return ph