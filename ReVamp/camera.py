import os
import sys
import threading
import time
import random
import subprocess
import tkinter
from tkinter import filedialog

import cv2
import numpy as np
import pygame as pg
from PIL import Image

import img_tools
from load_assets import *
from ui_element import button, toggle_button


'''
class : Camera
param : widht : int, height : int, caption : str, address : str (default : "none")
constructor : set the constants and create a capture obj and window obj
'''


class camera():
    def __init__(self, width, height, caption, address="none"):

        self.width = width
        self.height = height
        self.caption = caption
        self.address = address
        self.run = False
        self.mode = 'camera'
        self.allow_object = True
        self.object_overlays = []
        self.object_rects = []
        self.cursor_pos = (0, 0)
        self.frame_border = (10, 60)

        # connection to camera
        self.capture = cv2.VideoCapture(0)

        # address of the IP cam
        if not address == "none":
            success = self.capture.open(address)

            if not success:
                print("Couldn't connect to IP camera")
                self.capture.release()
                print("Connecting to device camera.....")
                self.capture = cv2.VideoCapture(0)
            else:
                print("successfully connected to IP camera")

    # * main thread
    def camera_loop(self):

        # creating a window
        self.window = pg.display.set_mode(
            (self.width, self.height), pg.NOFRAME)
        pg.display.set_caption(self.caption)

        click = False
        mouse_button = 'up'
        selected_rect = -1

        loading_frame_ind = 0
        loading_frame_delay = 1

        resize_fct = 0

        ui_elements = {}
        ui_elements['revamp'] = button(50, 19, 920, self.height - self.frame_border[1]/2 + 20, small_revamp, self.window)
        ui_elements['capture'] = button(
            50, 50, 480, self.height - self.frame_border[1]/2, capture_icon, self.window)
        ui_elements['obj_toggle'] = toggle_button(
            50, 50, 210, self.frame_border[1]/2, toggle_on, toggle_off, self.window, toggle_mode=True)
        ui_elements['camera_menu'] = button(
            40, 40, 40, self.frame_border[1]/2, camera_menu, self.window)
        ui_elements['open_icon'] = button(
            50, 50, 100, self.frame_border[1]/2, open_icon, self.window)
        ui_elements['object_detect'] = button(
            50, 50, 153, self.frame_border[1]/2, object_detect, self.window)
        ui_elements['gallery'] = button(
            60, 50, 50, self.height - self.frame_border[1]/2, gallery, self.window)
        ui_elements['cross'] = button(
            20, 20, 930, self.frame_border[1]/2, cross, self.window)
        ui_elements['confirm'] = button(
            50, 50, 480, self.height - self.frame_border[1]/2, confirm_icon, self.window)
        ui_elements['back'] = button(
            24, 30, 30, self.frame_border[1]/2, back, self.window)
        ui_elements['v_flip'] = button(
            40, 40, 300, self.frame_border[1]/2, v_flip, self.window)
        ui_elements['h_flip'] = button(
            40, 40, 350, self.frame_border[1]/2, h_flip, self.window)
        ui_elements['rot_clock'] = button(
            40, 40, 400, self.frame_border[1]/2, rot_clock, self.window)
        ui_elements['rot_anti'] = button(
            40, 40, 450, self.frame_border[1]/2, rot_anti, self.window)
        ui_elements['move'] = toggle_button(
            30, 30, 490, self.frame_border[1]/2, move, move, self.window, toggle_mode=False)
        ui_elements['minus'] = button(
            30, 30, 530, self.frame_border[1]/2, minus, self.window)
        ui_elements['reset'] = button(
            26, 26, 560, self.frame_border[1]/2, reset, self.window)
        ui_elements['plus'] = button(
            30, 30, 590, self.frame_border[1]/2, plus, self.window)
        ui_elements['save'] = button(
            30, 30, 640, self.frame_border[1]/2, save, self.window)

        ui_layer = {}
        ui_layer['camera'] = ['capture',
                              'obj_toggle', 'camera_menu', 'gallery', 'cross', 'revamp', 'open_icon', 'object_detect']
        ui_layer['loading'] = ['capture',
                               'obj_toggle', 'camera_menu', 'gallery', 'cross', 'revamp', 'open_icon', 'object_detect']
        ui_layer['object'] = ['confirm', 'back', 'cross', 'revamp']
        ui_layer['overlay'] = ['v_flip', 'h_flip',
                               'rot_clock', 'rot_anti', 'move', 'back', 'plus', 'reset', 'minus', 'cross', 'capture', 'gallery', 'save', 'revamp']

        for i in range(2):
            for tmp_ind in range(len(loading_img)):
                self.window.fill((0, 0, 0))
                image_pixel_array = pg.PixelArray(
                loading_img[tmp_ind].convert_alpha())
                image_pixel_array.replace((65, 200, 244), (255, 255, 255))
                img = pg.PixelArray.make_surface(image_pixel_array)

                self.window.blit(
                    img, (self.width/2 - loading_width/2, self.height/2 - loading_height/2 + 100))

                self.window.blit(revamp, (self.width/2 - revamp.get_width()/2, self.height/2 - revamp.get_height()/2 - 100))
                pg.display.update()

                pg.time.delay(90)

        while self.run:

            # check for events in the window
            for event in pg.event.get():
                self.cursor_pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    self.run = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    click = True
                elif event.type == pg.MOUSEBUTTONUP:
                    click = False

            if click and mouse_button == 'up':
                mouse_button = 'press'
            elif click and mouse_button == 'press':
                mouse_button = 'down'
            elif not click:
                mouse_button = 'up'

            if True:
                # get CV_umat of image from captue obj
                ret, frame_array = self.capture.read()
                frame_array = cv2.resize(frame_array, (self.width - self.frame_border[0]*2, self.height - self.frame_border[1]*2))
                frame_array = cv2.cvtColor(frame_array, cv2.COLOR_BGR2RGB)

                # convert CV_umat to PIL image obj and pygame surface
                frame_pil = Image.fromarray(frame_array, mode="RGB")
                frame_pg = img_tools.conv_cv_pygame(frame_array)

            # display main frame
            self.window.blit(frame_pg, (self.frame_border[0], self.frame_border[1]))

            # * ------------------------------------------------------------------------------------------
            # * camera mode ------------------------------------------------------------------------------
            # * ------------------------------------------------------------------------------------------
            if self.mode == 'camera':
                if ui_elements['capture'].hover(self.cursor_pos) and mouse_button == 'press':
                    image_path = os.path.dirname(__file__) + '/../Captures/'

                    while True:
                        random_name = str(random.randint(100000000, 199999999))
                        if os.path.exists(image_path + random_name + '.jpg'):
                            continue
                        else:
                            frame_pil.save(image_path + random_name + '.jpg')
                            break
                    print('image saved')


                elif ui_elements['obj_toggle'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.allow_object = ui_elements['obj_toggle'].toggle()

                elif ui_elements['camera_menu'].hover(self.cursor_pos) and mouse_button == 'press':
                    print('menu')
                
                elif ui_elements['cross'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.run = False

                elif ui_elements['gallery'].hover(self.cursor_pos) and mouse_button == 'press':
                    captures_path = os.path.dirname(
                        __file__) + '\\..\\Captures\\'
                    subprocess.Popen(r'explorer "{}"'.format(captures_path))

                elif ui_elements['open_icon'].hover(self.cursor_pos) and mouse_button == 'press':
                    captures_path = os.path.dirname(
                        __file__) + '\\..\\Captures\\'

                    tkinter.Tk().withdraw()
                    overlay_path = filedialog.askopenfilename(initialdir = captures_path)
                    open_overlay = pg.image.load(overlay_path)

                    self.object_overlays = [open_overlay]
                    self.object_rects = [(self.width/2 - open_overlay.get_width()/2, self.height/2 - open_overlay.get_height()/2, open_overlay.get_width(), open_overlay.get_height())]
                    initial_cursor_pos = -1
                    self.mode = 'overlay'

                elif ui_elements['object_detect'].hover(self.cursor_pos) and mouse_button == 'press':
                    captures_path = os.path.dirname(
                        __file__) + '\\..\\Captures\\'

                    tkinter.Tk().withdraw()
                    image_path = filedialog.askopenfilename(initialdir = captures_path)
                    image = Image.open(image_path)

                    self.mode = 'loading'
                    overlay_thread = threading.Thread(
                    target=self.create_overlay, args=(image,))
                    overlay_thread.start()
                    

                elif self.allow_object and mouse_button == 'press' and self.cursor_pos[0] > self.frame_border[0] and self.cursor_pos[1] > self.frame_border[1] and self.cursor_pos[0] < self.width - self.frame_border[0] and self.cursor_pos[1] < self.height - self.frame_border[1]:
                    self.mode = 'loading'
                    overlay_thread = threading.Thread(
                        target=self.create_overlay, args=(frame_pil,))
                    overlay_thread.start()

            # * ------------------------------------------------------------------------------------------
            # * loading mode -----------------------------------------------------------------------------
            # * ------------------------------------------------------------------------------------------
            elif self.mode == 'loading':

                image_pixel_array = pg.PixelArray(
                    loading_img[loading_frame_ind//loading_frame_delay].convert_alpha())
                image_pixel_array.replace((65, 200, 244), (255, 255, 255))
                img = pg.PixelArray.make_surface(image_pixel_array)

                self.window.blit(
                    img, (self.width/2 - loading_width/2, self.height/2 - loading_height/2))
                loading_frame_ind = (
                    loading_frame_ind+1) % (len(loading_img)*loading_frame_delay)

                if len(self.object_overlays) != 0:
                    loading_frame_ind = -1
                    selected_rect = -1
                    self.mode = 'object'

                pg.time.delay(100)

            # * ------------------------------------------------------------------------------------------
            # * object mode ------------------------------------------------------------------------------
            # * ------------------------------------------------------------------------------------------
            elif self.mode == 'object':

                for i in range(len(self.object_overlays)):
                    if selected_rect == -1:
                        self.window.blit(
                            self.object_overlays[i], self.object_rects[i][:2])
                    else:
                        if i == selected_rect:
                            selected_overlay = pg.transform.scale(
                                self.object_overlays[i], (self.object_rects[i][2] + 6, self.object_rects[i][3] + 6))
                            self.window.blit(
                                selected_overlay, (self.object_rects[i][0] - 3, self.object_rects[i][1] - 3))
                        else:
                            self.window.blit(
                                self.object_overlays[i], self.object_rects[i][:2])


                if ui_elements['confirm'].hover(self.cursor_pos) and mouse_button == 'press':
                    if selected_rect == -1:
                        selected_rect = 0
                    self.object_overlays = [
                        self.object_overlays[selected_rect]]
                    self.object_rects = [self.object_rects[selected_rect]]
                    initial_cursor_pos = -1
                    self.mode = 'overlay'

                elif ui_elements['back'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.object_overlays = []
                    self.object_rects = []
                    self.mode = 'camera'

                elif ui_elements['cross'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.run = False

                elif mouse_button == 'press':
                    for rect in self.object_rects:
                        if self.cursor_pos[0] > rect[0] and self.cursor_pos[1] > rect[1] and self.cursor_pos[0] < rect[0] + rect[2] and self.cursor_pos[1] < rect[1] + rect[3]:
                            selected_rect = self.object_rects.index(rect)
                            break

            # * ------------------------------------------------------------------------------------------
            # * overlay mode -----------------------------------------------------------------------------
            # * ------------------------------------------------------------------------------------------
            elif self.mode == 'overlay':
                resized_overlay = pg.transform.scale(self.object_overlays[0], (self.object_rects[0][2] + resize_fct, self.object_rects[0][3] + resize_fct))
                self.window.blit(
                    resized_overlay, self.object_rects[0][:2])

                rect = self.object_rects[0]

                if ui_elements['move'].toggle_mode:
                    resized_rect = (rect[0], rect[1], rect[2] + resize_fct, rect[3] + resize_fct) 
                    pg.draw.rect(self.window, (255, 255, 255), resized_rect, 1)

                if ui_elements['v_flip'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.object_overlays = [pg.transform.flip(
                        self.object_overlays[0],  True, False)]

                elif ui_elements['h_flip'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.object_overlays = [pg.transform.flip(
                        self.object_overlays[0],  False, True)]

                elif ui_elements['gallery'].hover(self.cursor_pos) and mouse_button == 'press':
                    captures_path = os.path.dirname(
                        __file__) + '\\..\\Captures\\'
                    subprocess.Popen(r'explorer "{}"'.format(captures_path))

                elif ui_elements['capture'].hover(self.cursor_pos) and mouse_button == 'press':
                    image_path = os.path.dirname(__file__) + '/../Captures/'

                    while True:
                        random_name = str(random.randint(100000000, 199999999))
                        if os.path.exists(image_path + random_name + '.jpg'):
                            continue
                        else:
                            sub = self.window.subsurface((self.frame_border[0], self.frame_border[1], self.width - self.frame_border[0]*2, self.height - self.frame_border[1]*2))
                            pg.image.save(sub, image_path + random_name + '.jpg')
                            break
                    print('image saved')

                elif ui_elements['save'].hover(self.cursor_pos) and mouse_button == 'press':
                    image_path = os.path.dirname(__file__) + '/../Captures/'

                    while True:
                        random_name = str(random.randint(100000000, 199999999))
                        if os.path.exists(image_path + random_name + '.png'):
                            continue
                        else:
                            pg.image.save(self.object_overlays[0], image_path + random_name + '.png')
                            break
                    print('image saved')

                elif ui_elements['rot_clock'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.object_overlays = [pg.transform.rotate(
                        self.object_overlays[0],  -90)]

                    self.object_rects = [(rect[0], rect[1], rect[3], rect[2])]

                elif ui_elements['rot_anti'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.object_overlays = [pg.transform.rotate(
                        self.object_overlays[0],  90)]

                    self.object_rects = [(rect[0], rect[1], rect[3], rect[2])]

                elif ui_elements['move'].hover(self.cursor_pos) and mouse_button == 'press':
                    ui_elements['move'].toggle()

                elif ui_elements['plus'].hover(self.cursor_pos) and mouse_button == 'down':
                    resize_fct += 1

                elif ui_elements['minus'].hover(self.cursor_pos) and mouse_button == 'down':
                    resize_fct -= 1

                elif ui_elements['reset'].hover(self.cursor_pos) and mouse_button == 'press':
                    resize_fct = 0

                elif ui_elements['cross'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.run = False

                elif ui_elements['back'].hover(self.cursor_pos) and mouse_button == 'press':
                    self.object_overlays = []
                    self.object_rects = []
                    self.mode = 'camera'

                elif ui_elements['move'].toggle_mode and mouse_button == 'press' and self.cursor_pos[0] > rect[0] and self.cursor_pos[1] > rect[1] and self.cursor_pos[0] < rect[0] + rect[2] and self.cursor_pos[1] < rect[1] + rect[3]:
                    initial_cursor_pos = self.cursor_pos
                
                elif mouse_button == 'down':
                    if initial_cursor_pos != -1:
                        dx = self.cursor_pos[0] - initial_cursor_pos[0]
                        dy = self.cursor_pos[1] - initial_cursor_pos[1]
                        rect = (rect[0] + dx, rect[1] + dy, rect[2], rect[3])
                        self.object_rects = [rect]
                        initial_cursor_pos = self.cursor_pos
                else:
                    initial_cursor_pos = -1

            # black border
            pg.draw.rect(self.window, (0, 0, 0), (0, 0, self.width, self.frame_border[1]), 0)
            pg.draw.rect(self.window, (0, 0, 0), (0, 0, self.frame_border[0], self.height), 0)
            pg.draw.rect(self.window, (0, 0, 0), (0, self.height - self.frame_border[1], self.width, self.frame_border[1]), 0)
            pg.draw.rect(self.window, (0, 0, 0), (self.width - self.frame_border[0], 0, self.frame_border[0], self.height), 0)

            # display ui elements
            for element_key in ui_layer[self.mode]:
                ui_elements[element_key].display()

            # update the display
            pg.display.update()

        pg.quit()

    # * start the main thread

    def start(self):
        self.run = True

        self.main_thread = threading.Thread(target=self.camera_loop)
        self.main_thread.start()
        print("Camera started")

    def close(self):
        self.run = False

    def create_overlay(self, frame_pil):
        overlay_pil, rects = img_tools.get_overlay(frame_pil)

        overlay_pg = img_tools.conv_pil_pygame(overlay_pil)
        for rect in rects:
            self.object_overlays.append(overlay_pg.subsurface(rect))
            self.object_rects.append((rect[0] + self.frame_border[0], rect[1] + self.frame_border[1], rect[2], rect[3]))
