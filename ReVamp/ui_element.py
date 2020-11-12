import pygame as pg


class button():
    def __init__(self, width, height, x, y, icon, window, visible=True):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.icon = pg.transform.scale(icon, (width, height))
        self.visible = visible
        self.window = window

    def hover(self, cursor_pos):
        if not self.visible:
            return False
        if cursor_pos[0] > self.x - self.width/2 and cursor_pos[0] < self.x + self.width/2 and cursor_pos[1] > self.y - self.height/2 and cursor_pos[1] < self.y + self.height/2:
            return True
        return False

    def display(self):
        if self.visible:
            self.window.blit(self.icon, (self.x - self.width/2, self.y - self.height/2))

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True



class toggle_button():
    def __init__(self, width, height, x, y, icon_on, icon_off, window, toggle_mode=False):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.icon_on = pg.transform.scale(icon_on, (width, height))
        self.icon_off = pg.transform.scale(icon_off, (width, height))
        self.visible = True
        self.toggle_mode = toggle_mode
        self.window = window

    def hover(self, cursor_pos):
        if not self.visible:
            return False
        if cursor_pos[0] > self.x - self.width/2 and cursor_pos[0] < self.x + self.width/2 and cursor_pos[1] > self.y - self.height/2 and cursor_pos[1] < self.y + self.height/2:
            return True
        return False

    def display(self):
        if self.visible:
            if self.toggle_mode:
                self.window.blit(self.icon_on, (self.x - self.width/2, self.y - self.height/2))
            else:
                self.window.blit(self.icon_off, (self.x - self.width/2, self.y - self.height/2))

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def toggle(self):
        self.toggle_mode = not self.toggle_mode
        
        return self.toggle_mode
