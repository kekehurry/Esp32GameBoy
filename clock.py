from machine import RTC,SPI,Pin
import ntptime
import utime
import ssd1306
import framebuf
import urequests

class Clock:
    def __init__(self,display,location="Cambridge,MA,US"):
        # Initialize the RTC
        self.rtc = RTC()
        self.display = display
        self.location_list = ["Cambridge,MA,US","Guangzhou,China","London,UK"]
        self.cursor = 0
        self.location = self.location_list[self.cursor]
        self.get_weather()
        self.sync_time()
        self.icon_list = {
            "Clouds" : b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x07\xe0\x00\x07\xfc\x00\x0f\xff\x00\x1f\xff\x80\x7f\xff\x80\xff\xff\xe0\xff\xff\xe0\xff\xff\xf0\xff\xff\xf0\x7f\xff\xe0\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            "Rain" : b'\x00\x00\x00\x07\xde\x00\x0f\xff\x00\x0f\xff\x80\x7f\xff\x80\xff\xff\xe0\xff\xff\xf0\xff\xff\xf0\xff\xff\xf0\x7f\xff\xe0?\xff\xc0\x03\xff\x00\x00\x1e\x00\x00\x00\x00\x18a\x80\x18a\x80\x12a\x80\x03\x0c\x00\x03\x0c\x00\x00\x00\x00',
            "Clear" : b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x00\x01\xfc\x00\x03\xfc\x00\x07\xfe\x00\x07\xfe\x00\x07\xfe\x00\x07\xfe\x00\x03\xfc\x00\x03\xfc\x00\x00\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            "Snow" : b'\x00`\x00\x03l\x00\x03\xfc\x00\x19\xf9\x80\x18\xf1\x80\xeccp|c\xe0>g\xc0\xff\xff\xf0\x01\xf8\x00\x01\xf8\x00\xff\xff\xf0>g\xc0|c\xe0\xeccp\x18\xf1\x80\x19\xf9\x80\x03\xfc\x00\x03l\x00\x00`\x00',
            "Thunderstorm" :b'\x01\xfc\x00\x01\xfc\x00\x03\xfc\x00\x03\xf8\x00\x03\xf8\x00\x07\xf0\x00\x07\xff\x00\x07\xfe\x00\x0f\xfc\x00\x01\xf8\x00\x01\xf0\x00\x01\xe0\x00\x03\xc0\x00\x03\x80\x00\x03\x80\x00\x07\x00\x00\x06\x00\x00\x04\x00\x00\x08\x00\x00\x00\x00\x00',
            "Other":b'\x00\x00\x00\x03\xe0\x00\x07\xf0\x00\x0f\xfc\x00?\xff\x00\x7f\x7f\x00\x7f\xff\xc0\x7f\xff\xe0?\xff\xf0\x1f\xff\xe0\x1f\xff\xe0\x0f\xbc\xc0\x07\x00\x00?\xe0\x00=\xe0\x00\x00\x7f\xc0\x00\x7f\xc0\x00\x00\x00\x1f\xf8\x00\x00\x00\x00'
            }
        self.display_info()
    
    def sync_time(self):
        # Synchronize with a time server
        ntptime.settime()
        current_time_ntp = utime.time()
        time_tuple = utime.localtime(current_time_ntp + self.timezone)
        self.rtc.datetime(time_tuple[0:3] + (0,) + time_tuple[3:6] + (0,))
    
    def get_weather(self):
        api_key = "e9666079ecaf8f26473616adcadf2d74"
        location = self.location
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&APPID={api_key}&units=metric"
        response = urequests.get(api_url)
        weather_data = response.json()
        self.weather = weather_data["weather"][0]["main"]
        self.timezone = weather_data["timezone"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        self.temperature = "T:{:.1f}`C".format(temperature)
        self.humidity = "H:{}%".format(humidity)
        self.wind_speed = "W:{:.1f}m/s".format(wind_speed)

    def display_info(self):
        local_time = self.rtc.datetime()
        time = "{:02}/{:02} {:02}:{:02}:{:02}".format(local_time[1], local_time[2],local_time[4], local_time[5], local_time[6])
        self.display.fill(0)
        city = self.location.split(",")[0]
        self.display.text(city,self.display.width//2-4*len(city),0,1)
        self.display.text(time,self.display.width//2-4*len(time),self.display.height-8,1)
        self.display.text(self.temperature,self.display.width//2,16,1)
        self.display.text(self.humidity,self.display.width//2,28,1)
        self.display.text(self.wind_speed,self.display.width//2,40,1)
        self.display.text(self.weather[:6],self.display.width//4-4*len(self.weather[:6]),40,1)
        
        # draw icon
        if self.weather in self.icon_list.keys():
            buffer = bytearray(self.icon_list[self.weather])
        else:
            buffer = bytearray(self.icon_list["Other"])
        
        fb = framebuf.FrameBuffer(buffer, 20, 20, framebuf.MONO_HLSB)
        self.display.blit(fb,self.display.width//4-10,16)
        self.display.show()
    
    def update(self,button):
        if button==3:
            return "menu"
        
        if button ==2:
            self.cursor -= 1
        if button == 5:
            self.cursor += 1
        if self.cursor < 0 :
            self.cursor = 2
        if self.cursor > len(self.location_list)-1:
            self.cursor = 0
        
        if self.location != self.location_list[self.cursor]:
            self.location = self.location_list[self.cursor]
            self.get_weather()
            self.sync_time()
        
        #auto update
        if utime.time()%60==0:
            self.get_weather()
            self.sync_time()
            
        self.display_info()
        
            


    
    
    
    
        
