import serial
import click
import logging
import time
import subprocess as sp

HEADER_STR_LEN=156
CR = b'\r'
SETUP=b's'

logging.basicConfig(level=logging.INFO)
@click.command()
@click.option('--serial-device', default='/dev/tty.usbserial', required=True)
@click.argument('config', type=click.File('rt'), required=True)
def start(serial_device, config):
    
    ser = serial.Serial(serial_device, timeout=10)
    ser.write(CR)
    ser.read(HEADER_STR_LEN)
    setupstring = None
    spectrocmd = ''
    # Читаем строки из конфигурационного файла
    for line in config.readlines():
        cmd = line.split(maxsplit=1)
        if cmd[0].startswith('SETUP:'):
            setupstring = cmd[1]
            ser.timeout=0
            logging.info("Begin configure controller")
            writereadstr(ser, cmd[1])
            logging.info("End configure controller")
            d=ser.readall()
            logging.info(d.decode("utf-8"))
            
        elif cmd[0].startswith('RUN:'):
            N = int(cmd[1])
            K = int(setupstring[-3:])
            logging.info("Start run cycler %d times"%N)
            ser.timeout=10
            for n in range(N):
                ser.write(b'l')
                ret = ser.read(6)
                logging.info(ret.decode("utf-8"))
                for k in range(K):
                    ser.write(b'y')
                    
                    if k+1!=K:
                        ret=ser.read(10)
                    else:
                        ret=ser.read(8)
                    logging.info(ret.decode("utf-8"))
                ret = ser.read(154)
                logging.info(ret.decode("utf-8"))

        elif cmd[0].startswith("SPECTRO:"):
            spectrocmd = cmd[1]
            print(spectrocmd)
            a=sp.Popen([r'--serial-device=/dev/ttyUSB1', r'"%s"'%spectrocmd], 2048, './spectro.py')
            a.wait()

        elif cmd[0].startswith("STOP"):
            logging.info("Stop App")
            ser.close()
            break


    return

    
def writereadstr(dev, s):
    """
    Write string into device char by char
    """
    for c in s:
        dev.write(c.encode('utf-8'))
        time.sleep(0.2)


    



if __name__ == "__main__":
    start()
    
