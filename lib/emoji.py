from time import sleep
from m5stack import lcd

class Emoji:
    def __init__(self, x_number=7, y_number=7, width=15, gap=9):
        self._x = int((320 - x_number*(width+gap) - gap) / 2)
        self._y = int((240 - y_number*(width+gap) - gap) / 2) 
        self._x_number = x_number
        self._y_number = y_number
        self._width = width
        self._gap = gap
        self._lcd = lcd
        self.show_normal()
  
    def draw_square(self, x_number, y_number, color):
        x = self._x + x_number*(self._width+self._gap) + self._gap
        y = self._y + y_number*(self._width+self._gap) + self._gap
        self._lcd.rect(x, y, self._width, self._width, color, color)    
    
    def show_normal(self, img=4):
        img = min(img, 5)
        self._lcd.image(0, 0, 'emojiImg/{}.jpg'.format(img))

        self._lcd.rect(self._x, self._y, 
                self._x_number*self._width+self._gap*(self._x_number+1), 
                self._y_number*self._width+self._gap*(self._y_number+1),
                self._lcd.DARKGREY, self._lcd.DARKGREY)
    
        for i in range(self._x_number):
            for j in range(self._y_number):
                self.draw_square(i, j, self._lcd.WHITE)
            

    def show_map(self, s_map, color=0xfd8585):
        for i in range(7): 
            for j in range(7):
                if s_map[i][j] == 0:
                    self.draw_square(j, i, self._lcd.WHITE)
                else:
                    self.draw_square(j, i, color)
    
    def clear(self):
         for i in range(7): 
            for j in range(7):
                self.draw_square(j, i, self._lcd.WHITE)
               
    def show_love(self, color=0xfd8585):
        self.a = [[ 0, 0, 0, 0, 0, 0, 0],
            [ 0, 1, 0, 0, 0, 1, 0],
            [ 1, 1, 1, 1, 1, 1, 1],    
            [ 0, 1, 1, 1, 1, 1, 0],     
            [ 0, 0, 1, 1, 1, 0, 0],     
            [ 0, 0, 0, 1, 0, 0, 0],     
            [ 0, 0, 0, 0, 0, 0, 0]]    

        for i in range(7): 
            for j in range(7):
                if self.a[i][j] == 0:
                    self.draw_square(j, i, self._lcd.WHITE)
                else:
                    self.draw_square(j, i, color)
    

    
    

    
