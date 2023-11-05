from machine import Pin
import utime


class KeyPad():
    def __init__(self, KP_rows=[4,5,6,7] , KP_cols=[8,9,10,11]):
        
        self.key = None
        self.characters = [["1","2","3","A"],
                           ["4","5","6","B"],
                           ["7","8","9","C"],
                           ["*","0","#","D"]]
        
        self.KP_rows = KP_rows
        self.KP_cols = KP_cols
        
        self.row_pins = []
        self.col_pins = []
        
        for cnt in range(0, 4):
             self.row_pins.append(Pin(self.KP_rows[cnt], Pin.OUT))
             self.col_pins.append(Pin(self.KP_cols[cnt], Pin.IN, Pin.PULL_DOWN))
    
    def start(self):
        while True:
            self.key = self.getKey()
            # utime.sleep(0.3)
            
    
    def getKey(self):
        key = []
        for cnt_1 in range(4):
            self.row_pins[cnt_1].high()
            # print(self.row_pins[cnt_1].value())
            for cnt_2 in range(4):
                # print(self.col_pins[cnt_2].value())
                if(self.col_pins[cnt_2].value() == 1):
                    key.append(self.characters[cnt_1][cnt_2])
                    # print(self.characters[cnt_1][cnt_2])
                    utime.sleep(0.3)
            self.row_pins[cnt_1].low()
        if key == [] :
            return None
        else:
            return key[0]
