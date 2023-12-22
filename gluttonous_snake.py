from machine import Pin, SPI,ADC,PWM
from utime import sleep_ms
import ssd1306
import framebuf
from urandom import getrandbits,randint



class GluttonousSnake:
    def __init__(self,display):
        self.display = display
        self.init_game()
    
    def _draw_heart(self,x,y):
        heart = [
            "01100110",
            "11111111",
            "11111111",
            "01111110",
            "00111100",
            "00011000",
            "00000000"
        ]
        heart_width = len(heart[0])
        heart_height = len(heart)

        start_x = max(0, x - heart_width // 2)
        start_y = max(0, y - heart_height // 2)

        for row in range(heart_height):
            for col in range(heart_width):
                pixel = heart[row][col]
                if pixel == "1":
                    self.display.pixel(start_x + col, start_y + row, 1)
                    self.heart.append(((start_y + row)//self.size,(start_x + col)//self.size))
                    
    def _draw_christmas(self):
        buffer = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x0f\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80\x00\x1b\x80\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00c\x07\x80\x0c\x19\x8c\x1e\x02\x0c\x00\x00\x00\x00\x00\x00\x00c\x0f\xc0\x0c4\xcc?\x07\x0c\x00\x00\x00\x00\x00\x00\x00\xf7\x9f\xc0\x1ef\xde\x7f\x07\x1e\x00\x00\x00\x00\x00\x00\x00\xff\x9f\xec\x1e`~\x7f\x8f\xbe\x00\x00\x00\x00\x00\x00\x00\xff\xff\xee?\xd8\x7f\xff\xdf\xff\x00\x00\x00\x00\x00\x00\x00\xff\xff\xfe\x7f\xd8?\xff\xdf\xff\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x7f\x80\x1f\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xc3\x1f\xff\xff\xff\xc0\x00\x00\x00\x00\x00\x00\xff\xff\xff\xffC\x0f\xff\xff\xff\xc0\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe\x00\x07\xff\xff\xff\xe0\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe\x18\xc7\xff\xff\xff\xe0\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfc\x00\x03\xff\xff\xff\xf7\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf0\xff\xff\xff\xff\xff\xff\xff\xf3\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xe3\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x1f\xff\xff\xff\xff\xff\xf8\x00\x00\x00\x00\xff\xf8\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x07\xff\xff\xff\xff\x00\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        fb = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB)
        self.display.fill(0)
        self.display.blit(fb, 0, 0)
        self.display.text("Merry",10,8,1)
        self.display.text("Christmas",10,20,1)
        for i in range(100):
            x = randint(0,128)
            y = randint(0,64)
            self.display.pixel(x,y,1)
            logo = [
             "1111111",
             "1000000",
             "1011111",
             "1010000",
             "1011111",
             "1000001",
             "1110111"
             ]
        self. _draw_logo(logo[:self.count],90,8)
        self.count+=1
        if self.count > len(logo):
            self.count = len(logo)
        self.display.show()
        sleep_ms(200)
    
    def _draw_logo(self,logo,x,y):
        logo_width = len(logo[0])
        logo_height = len(logo)
        line_width  = 3
        for row in range(logo_height):
            for col in range(logo_width):
                if logo[row][col] == "1":
                    self.display.fill_rect(col * 3+x, row*3+y, 3, 3,1)
    
    def init_game(self):
        # Snake initialization
        self.size = 4
        self.font_size = 8
        self.width = self.display.width//self.size
        self.height = (self.display.height-self.font_size)//self.size
        self.snake = [(5, 7), (5, 6), (5, 5)]
        self.snake_direction = (0, 1)  # Initial direction: right
        # Food initialization
        self.food = (getrandbits(6) % self.height, getrandbits(5) % self.width)
        self.run = True
        self.game_over = False
        self.get_reward = False
        self.heart = []
        self.score = 0
        self.count = 1
        
        # Initialize display
        # self.display.fill(0)

        # Draw the tile
        # self.display.text("Kai's",self.display.width//2-20, self.display.height//2-self.font_size*2, 1)
        # self.display.text("Gluttonous Snake",0, self.display.height//2, 1)
        # self.display.show()
    
    def pause_game(self):
        if self.score<100:
            self.run = (not self.run)
            if not self.run:
                self.display.fill(0)
                self.display.text("Pause",self.display.width//2-20, self.display.height//2-self.font_size, 1)
                self.display.show()
                sleep_ms(500)
    
    def listen_to_controller(self,button):
        if button == 1:
            self.pause_game()
            sleep_ms(100)
        #if button == 3:
            #self.init_game()
        elif button == 2 and self.snake_direction != (1, 0):  # Up button
            self.snake_direction = (-1, 0)
        elif button == 5 and self.snake_direction != (-1, 0):  # Down button
            self.snake_direction = (1, 0)
        elif button == 4 and self.snake_direction != (0, 1):  # Left button
            self.snake_direction = (0, -1)
        elif button == 6 and self.snake_direction != (0, -1):  # Right button
            self.snake_direction = (0, 1)
    
    def update(self,button):
        self.listen_to_controller(button)
        
        if button==3:
            return "menu"
            
        if self.game_over:
            self.display.fill(0)
            self.display.text("Game Over",self.display.width//2-30, self.display.height//2-self.font_size, 1)
            self.display.show()
            self.run = False
        
        if self.score==100:
            self.display.fill(0)
            self.display.text("Congratulations!",self.display.width//2-60, self.display.height//2-self.font_size, 1)
            self.display.show()
            sleep_ms(1000)
            self.score += 1
            self.run = False
        
        if self.score>100:
            self._draw_christmas()
            self.run = False
            

        if self.run:
            # Update snake position
            head = (
                (self.snake[0][0] + self.snake_direction[0]) % self.height,
                (self.snake[0][1] + self.snake_direction[1]) % self.width,
            )
            self.snake.insert(0, head)
            # Check if the snake has eaten the food
            if head == self.food:
                self.food = (getrandbits(6) % self.height, getrandbits(5) % self.width)  # Generate new food
                self.score += 5
            else:
                # If not, remove the last segment of the snake
                tail = self.snake.pop()
            
            if head in self.heart:
                self.score += 5
                
            # Check for collisions with the snake's own body
            if head in self.snake[1:]:
                self.run = False
                self.game_over = True
            
            # Clear the display
            self.display.fill(0)

            # Draw the snake
            for segment in self.snake:
                self.display.fill_rect(segment[1] * self.size, segment[0] * self.size, self.size, self.size,1)

            # Draw the food
            if self.score == 95:
                self._draw_heart(self.food[1] * self.size, self.food[0] * self.size)
            else:
                self.display.fill_rect(self.food[1] * self.size, self.food[0] * self.size, self.size, self.size,1)
            
            # Draw Score
            self.display.text("Score:%03d"%self.score,self.width//2+15,self.display.height-self.font_size,1)

            # Present the display
            self.display.show()
            
            #Control the speed
            sleep_ms(100-self.score//2)

    

    

    







