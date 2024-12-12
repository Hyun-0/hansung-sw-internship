class RGBLight:
    def __init__(self, red = 0, green = 0, blue = 0, power = 0):
        self.red = red
        self.green = green
        self.blue = blue
        self.isLightOn = False
        
    def change_color(self, rgblight):
        self.red = rgblight.red
        self.green = rgblight.green
        self.blue = rgblight.blue
        self.isLightOn = True
    
    def change_power(self, isLightOn: bool):
        self.isLightOn = isLightOn
        if (0 == self.red) and (0 == self.green) and (0 == self.blue):
            if self.isLightOn:
                self.red = 255
                self.green = 255
                self.blue = 255
            
        
    def to_json(self):
        return {
            "red": self.red,
            "green": self.green,
            "blue": self.blue,
            "isLightOn": self.isLightOn
        }