import os, sys

sys.path.insert(1, os.path.dirname(__file__)+'/../Basnet')

from PIL import Image
from PIL import ImageDraw
import numpy as np
import basnet
import pygame as pg
import cv2



def get_rects(mask):
    mask_cv = np.asarray(mask) 
    contours, hierarchy = cv2.findContours(mask_cv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []

    for contour in contours:
        rect = cv2.boundingRect(contour)
        rects.append(rect)

    return rects


def draw_rects(img, rects):

    img_draw = ImageDraw.Draw(img)

    for rect in rects:
        x, y, w, h = rect 
        shape = [(x, y), (x + w, y + h)]
        img_draw.rectangle(shape, outline=(0, 255, 0))

    img.show()


def get_mask(img):

    basnet.load_BASNet()
    mask = basnet.run(np.asarray(img)).convert("L")

    return mask


def get_overlay(img):
    mask = get_mask(img)


    mask_resized = mask.resize(size=img.size, resample=Image.BILINEAR)
    blank = Image.new(mode="RGBA", size=img.size, color=0)
    overlay = Image.composite(img, blank, mask=mask_resized)

    rects = get_rects(mask_resized)
    
    return overlay, rects


def conv_cv_pygame(cv_image):
    mode = "RGB"
    size = cv_image.shape[1::-1]
    data = cv_image.tobytes()
     
    frame_pg = pg.image.fromstring(data, size, mode)
          
    return frame_pg


def conv_pil_pygame(cv_image):
    mode = cv_image.mode
    size = cv_image.size
    data = cv_image.tobytes()
        
    frame_pg = pg.image.fromstring(data, size, mode)
          
    return frame_pg
