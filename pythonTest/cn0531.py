import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

spi.max_speed_hz = 1000000
spi.mode = 1

try:
#    tx = [0x40, 0x00, 0x04]
#    print(f"Sending: {[hex(x) for x in tx]}")
#    resp = spi.xfer2(tx)
#    time.sleep(0.5)

    # Set control register
    tx = [0x20, 0x00, 0x10]
    print(f"Sending: {[hex(x) for x in tx]}")
    resp = spi.xfer2(tx)
#    time.sleep(0.5)

    # Set DAC max output voltage
    tx = [0x1f, 0x00, 0x00]
    print(f"Sending: {[hex(x) for x in tx]}")
    resp = spi.xfer2(tx)
#    time.sleep(0.5)

    # Set software register Reset 0, CLR 0, LDAC 0
#    tx = [0x40, 0x00, 0x00]
#    print(f"Sending: {[hex(x) for x in tx]}")
#    resp = spi.xfer2(tx)
#    time.sleep(5)

    # Set software register : Reset 1, CLR 0, LDAC 0
#    tx = [0x40, 0x00, 0x40]
#    print(f"Sending: {[hex(x) for x in tx]}")
#    resp = spi.xfer2(tx)
#    time.sleep(0.5)

#    rx_dac = [0x90, 0x00, 0x00]
#    rx_ctrl = [0xa0, 0x00, 0x00]
#    rx_clr = [0xb0, 0x00, 0x00]


#    rev = spi.xfer2(rx_clr)
#    time.sleep(0.5)

#    print(f"Received: {[hex(x) for x in rev]}")


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    spi.close()
    print("SPI port closed.")


