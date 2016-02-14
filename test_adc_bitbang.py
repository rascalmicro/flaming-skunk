import RPi.GPIO as GPIO
import sys
import time

CLK = 11
MISO = 9
MOSI = 10
CS = 8

def setupSPIPins():
    ''' Set all pins as an output except MISO (Master Input, Slave Output)'''
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(CS, GPIO.OUT)


def transfer_byte(data):
    retVal = 0

#    print data

    for bit in range(8):
        # Set RPi's output bit high or low depending on highest bit of data field
        if data & 0x80:
            GPIO.output(MOSI, GPIO.HIGH)
        else:
            GPIO.output(MOSI, GPIO.LOW)

        # Advance data to the next bit
        data <<= 1

        # Read 1 data bit in
        if GPIO.input(MISO):
            retVal |= 0x1
    
        # Advance input to next bit
        retVal <<= 1

        # Pulse the clock pin HIGH then immediately low
        GPIO.output(CLK, GPIO.HIGH)
        GPIO.output(CLK, GPIO.LOW)

#    print retVal
    return retVal/2

def transfer_bytes(bytes):
    
    # data <<= (8-numBits)
    received_bytes = [transfer_byte(byte) for byte in bytes]
    return received_bytes

def readadc(channel):
    if channel > 7 or channel < 0:
        return -1

    # Datasheet says chip select must be pulled high between conversions
    GPIO.output(CS, GPIO.HIGH)
    
    # Start the read with both clock and chip select low
    GPIO.output(CS, GPIO.LOW)
    GPIO.output(CLK, GPIO.HIGH)

    reading = transfer_bytes([1, 8 + channel << 4, 0])

    GPIO.output(CS, GPIO.HIGH)

    return ((reading[1] & 3) << 8) + reading[2]

if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        setupSPIPins()
    
        while True:
            for i in range(8):
                value = readadc(i)
                print "%4d" % value,
            time.sleep(0.2)
            print;

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)
