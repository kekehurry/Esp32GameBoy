from machine import Pin
import network
import utime as time




class Wifi:
    
    def __init__(self,display=None):
        self.wifi = network.WLAN(network.STA_IF)
        self.ip = self.wifi.ifconfig()[0]
        self.led_pin = Pin(2,Pin.OUT)
        if display:
            self.display = display
        
       
    def scan_and_connect(self):
        wifi_ssid = None
        wifi_password = None
        self.wifi.active(True)
        for ssid, bssid, channel, RSSI, authmode, hidden in self.wifi.scan():
            ssid = ssid.decode("utf-8")
            if ssid == "WIFI1":
                wifi_ssid = ssid
                wifi_password = "******"
            if ssid == "WIFI2":
                wifi_ssid = ssid
                wifi_password = "******"
        
        if wifi_ssid:
            wait_seconds = 0
            while not self.wifi.isconnected():
                print(".", end="")
                self.wifi.connect(wifi_ssid, wifi_password)
                time.sleep(1)
                wait_seconds +=1
                if wait_seconds > 60:
                    print("Wifi not connected!")
                    break
                
        if self.wifi.isconnected():
            self.ip = self.wifi.ifconfig()[0]
            self.led_pin.on()
        
    def activate(self):
        self.wifi.active(True)
    
    def deactivate(self):
        self.wifi.active(False)
    
    def update(self,button):
        self.display.fill(0)
        if self.wifi.isconnected():
            text = "My IP Address"
            self.display.text(text,self.display.width//2-len(text)*4,self.display.height//2-8,1)
            self.display.text(self.ip,self.display.width//2-len(self.ip)*4,self.display.height//2+8,1)
        else:
            text = "Wifi disconnected!"
            self.display.text(text,self.display.width//2-len(text)*4,self.display.height//2-8,1)
        self.display.show()
        if button ==3 or button==5:
            return "menu"



            
            
        
        
    


