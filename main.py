from machine import Pin, SPI,ADC,PWM
from utime import sleep_ms
from gluttonous_snake import GluttonousSnake
from clock import Clock
from menu import Menu
from net import Wifi
from mqtt_message import MQTTMessage
import ssd1306

#SPI
spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(13))
dc = Pin(4)    # data/command
rst = Pin(2)   # reset
cs = Pin(5)   # chip select, some modules do not have a pin for this
display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)


# Button pins
col_pins_ = [32, 33, 25]
row_pins_ = [27, 26]
col_pins = []
row_pins = []
keymap = [[1,2,3],
          [4,5,6]]

# Passive Buzzer
buzzer = PWM(Pin(12))
buzzer.duty(0)

# Potentiometer
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

# Additional Input
input_pin = ADC(Pin(35))
input_pin.atten(ADC.ATTN_11DB)

#Additional Output
output_pin = Pin(21,Pin.OUT)
output_pin.off()

for pin in row_pins_:
    p = Pin(pin, Pin.OUT)
    p.off()
    row_pins.append(p)

for pin in col_pins_:
    p = Pin(pin, Pin.IN, Pin.PULL_UP)
    col_pins.append(p)

mode = "menu"

while True:
    button = None
    for i, row_pin in enumerate(row_pins):
        row_pin.on()
        for j, col_pin in enumerate(col_pins):
            if not col_pin.value():  # Button pressed (active low)
                button = keymap[i][j]
        sleep_ms(10)
        row_pin.off()
    
    if mode == "menu":
        app = Menu(display)
    
    if mode == "game":
        app = GluttonousSnake(display)
    
    if mode == "clock":
        app = Clock(display)
    
    if mode == 'mqtt':
        app = MQTTMessage(display)
    
    if mode == "wifi":
        app = Wifi(display)
    
    try:
        mode = app.update(button)
    except Exception as e:
        mode = "menu"
        
    
    

                    
            
    





