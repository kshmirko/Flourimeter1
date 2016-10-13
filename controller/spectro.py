#!/home/kshmirko/miniconda3/bin/python

import serial
import click


@click.command()
@click.option('--serial-device', default='/dev/ttyUSB1', required=True)
@click.argument('cmd', required=True)
def spectrometer(serial_device, cmd):
    #print(cmd)
    ser = serial.Serial(serial_device, timeout=600)
    ser.write(("%s\r"%cmd).encode('utf-8'))
    response = ser.readline()
    ser.close()
    print(response.decode('utf-8'))
    


if __name__=='__main__':

    spectrometer()

