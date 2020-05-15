import argparse
import logging
import os
import sys
import glob
import time

import serial

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def read_sensor(ser):
    data = ser.readline()
    if data == b'\r\n':
        data = ser.readline()
    data = data.split()
    if len(data) != 14:
        return None

    colors = "{},{},{},{},{},{},{}".format(
        float(data[1]),
        float(data[3]),
        float(data[5]),
        float(data[7]),
        float(data[9]),
        float(data[11]),
        float(data[13]),
    )

    return colors

def main(args):
    if args.query:
        print("Devices:")
        print("\t{}".format(serial_ports()))
        sys.exit(0)
    if args.device is None:
        sys.exit(
            "You must specify the port. E.g. COM1 or /dev/ttyACM0.\nYou can see which ports are available by passing the '-q' flag")
    if args.output is None:
        sys.exit("You must specify the output file.")

    ser = serial.Serial(args.device, 115200)
    with open(args.output + '.csv', 'x') as f:
        if args.verbose:
            print("Temp,450,500,550,570,600,650")
        f.write("Temp,Violet,Blue,Green,Yellow,Orange,Red\n")
        t_end = time.time() + float(args.time)
        while time.time() < t_end:
            reading = read_sensor(ser)
            if reading is not None:
                if args.verbose:
                    print(reading)
                f.write('{}\n'.format(reading))

    sys.exit(0)

if __name__ == "__main__":
    helptext = 'This script will attempt to open the arduino serial port and read sensor values for t seconds.'

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="Time of reading in seconds", default=30)
    parser.add_argument("-o", "--output", help="Path of output file. Will be appended with '.csv'")
    parser.add_argument("-d", "--device", help="Device port")
    parser.add_argument("-v", "--verbose", help="Print readings to STDOUT", action="store_true")
    parser.add_argument("-q", "--query", help="Query serial ports. This flag takes precedence", action="store_true")

    args =  parser.parse_args()

    main(args)