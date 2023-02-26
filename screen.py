import arcade

class Screen(arcade.Window):

    def __init__(self, pixelSize, rows, cols, screen):
        self.ROWS = rows
        self.COLS = cols
        self.PIXEL_SIZE = pixelSize
        self.SCREEN_WIDTH = pixelSize * cols
        self.SCREEN_HEIGHT = pixelSize * rows
        self.SCREEN = screen
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Chip8.py")

    def updateScreen(self, screen):
        self.SCREEN = screen

    def draw(self):
        # print(self.SCREEN)
        arcade.start_render()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = col * self.PIXEL_SIZE + self.PIXEL_SIZE // 2
                y = self.SCREEN_HEIGHT - (row * self.PIXEL_SIZE + self.PIXEL_SIZE // 2)
                if self.SCREEN[col + row * self.COLS] == 1:
                    color = arcade.color.WHITE
                else:
                    color = arcade.color.BLACK
                arcade.draw_rectangle_filled(x, y, self.PIXEL_SIZE, self.PIXEL_SIZE, color)
        arcade.finish_render()
