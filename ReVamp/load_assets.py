import pygame as pg
import os

loading_img = []
loading_width = 100
loading_height = 100

revamp = pg.image.load( os.path.dirname(__file__) + '/assets/ReVamp.png' )
small_revamp = pg.image.load( os.path.dirname(__file__) + '/assets/small_ReVamp.png' )


for i in range(1,1000):
    try:
        path = os.path.dirname(__file__) + '/assets/loading/loading (' + str(i) + ').png'
        loading_img.append(pg.transform.scale(pg.image.load(path),(loading_width, loading_height))) 
    except Exception as e:
        break

capture_icon = pg.image.load( os.path.dirname(__file__) + '/assets/capture.png' )

toggle_on =  pg.image.load( os.path.dirname(__file__) + '/assets/toggle_on.png' )
toggle_off =  pg.image.load( os.path.dirname(__file__) + '/assets/toggle_off.png' )

camera_menu = pg.image.load( os.path.dirname(__file__) + '/assets/camera_menu.png' )

open_icon = pg.image.load( os.path.dirname(__file__) + '/assets/open.png' )

object_detect = pg.image.load( os.path.dirname(__file__) + '/assets/object_detect.png' )

cross = pg.image.load( os.path.dirname(__file__) + '/assets/cross.png' )

gallery = pg.image.load( os.path.dirname(__file__) + '/assets/gallery.png' )

confirm_icon = pg.image.load( os.path.dirname(__file__) + '/assets/confirm.png' )
back = pg.image.load( os.path.dirname(__file__) + '/assets/back.png' )

v_flip = pg.image.load( os.path.dirname(__file__) + '/assets/v_flip.png' )
h_flip = pg.image.load( os.path.dirname(__file__) + '/assets/h_flip.png' )

rot_clock = pg.image.load( os.path.dirname(__file__) + '/assets/rot_clock.png' )
rot_anti = pg.image.load( os.path.dirname(__file__) + '/assets/rot_anti.png' )

move = pg.image.load( os.path.dirname(__file__) + '/assets/move.png' )

plus = pg.image.load( os.path.dirname(__file__) + '/assets/plus.png' )
minus = pg.image.load( os.path.dirname(__file__) + '/assets/minus.png' )
reset = pg.image.load( os.path.dirname(__file__) + '/assets/reset.png' )

save = pg.image.load( os.path.dirname(__file__) + '/assets/save.png' )