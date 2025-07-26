from machine import I2C
from microplate.charlcd_i2c_driver import CharLcdDriver
from microplate.charlcd_buffered import CharLCD

i2c = I2C(0, scl=22, sda=21)
devices = i2c.scan()

drv = CharLcdDriver(devices[0])

lcd = CharLCD(20, 4, drv, 0, 0)
lcd.init()

lcd.write("Hello !", 0, 0)
lcd.flush()
