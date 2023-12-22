from umqtt.simple import MQTTClient
from utime import sleep_ms
import _thread
import sys
import urequests

'''http://www.hivemq.com/demos/websocket-client/'''

class MQTTMessage:
    def __init__(self,display):
        server="de9b9f1f.ala.us-east-1.emqxsl.com"
        port = 8883
        user = "kekehurry"
        password = "hk19931111"
        clientid = "kai_esp32"
        self.client = MQTTClient(clientid, server, port, user, password, ssl=True, ssl_params={'server_hostname': server})
        self.client.set_callback(self.callback)
        self.client.connect(clean_session=True)
        self.display = display
        self.topic_list = ["message","todo","chat","code"]
        self.topic = self.topic_list[0]
        self.cursor = 0
        self.page = {}
        self.page_num = {}
        self.messages = {}
        for topic in self.topic_list:
            self.client.subscribe(topic)
            self.page[topic] = 0
            self.page_num[topic] = 0
            self.messages[topic] = []
        self.exit_flag = False
        _thread.start_new_thread(self.check_msg, ())
    
    def _split_text(self,text, chunk_size=16):
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    def _chat(self,text):
        try:
            key = "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"
            headers = {"Authorization": f"Bearer {key}"}
            data = {'model': 'gpt-3.5-turbo', 'messages': [{
                  "role": "system",
                  "content": '''You are a helpful chatbot, when send you a text, you responed in short and breif sentences'''
                },{
                  "role": "user",
                  "content": f"{text}",
                },]}
            r = urequests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            content = r.json()['choices'][0]['message']['content']
            return content
        except Exception as e:
            print(e)
            return str(e)
         
    
    def check_msg(self):
        while not self.exit_flag:
            try:
                self.client.wait_msg()
            except Exception as e:
                print("Error in MQTT thread:", e)

    def callback(self,topic, msg):
        msg = msg.decode('UTF-8')
        topic = topic.decode('UTF-8')
        if topic == "chat":
            msg = self._chat(msg)
        if topic == "code":
            exec(msg)
            msg = "recived code:\n" + msg
        msg = msg.split('\n')
        for m in msg:
            self.messages[topic].extend(self._split_text(m))
        self.page_num[topic] = len(self.messages[topic])//7+1
            
    def display_info(self,topic):
        messages = self.messages[topic][self.page[topic]*7:(self.page[topic]+1)*7]
        for i,message in enumerate(messages):
            self.display.text(message,0,(i+1)*8,1)
            
    def update(self,button):
        if button ==3:
            self.client.disconnect()
            self.exit_flag = True
            return "menu"
        if button ==2:
            self.cursor -= 1
        if button == 5:
            self.cursor += 1
        if self.cursor < 0 :
            self.cursor = len(self.topic_list)-1
        if self.cursor > len(self.topic_list)-1:
            self.cursor = 0
        
        topic = self.topic_list[self.cursor]
            
        if button ==1:
            self.messages[topic] = ''
            self.page_num[topic] = 0
        if button ==4:
            self.page[topic] -= 1
        if button == 6:
            self.page[topic] += 1
        if self.page[topic] < 0 :
            self.page[topic] = self.page_num[topic]
            print(self.page[topic])
        if self.page[topic] > self.page_num[topic]:
            self.page[topic] = 0
        
        self.display.fill(0)
        self.display.text(topic,self.display.width//2-len(topic)*4,0,1)
        self.display_info(topic)
        self.display.show()
        sleep_ms(100)
        
