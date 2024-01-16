#!env python3
# Don´t touch this
from pynput import keyboard as pk
from pynput.keyboard import Key as kk

##################################################
# ACTION MAPS
# EL CANAL midi es un bancos. 16 canales.
##################################################

#channel is positional, pad isn't
#This is it for rendimiento
pads = [
    [ #channel/bank 0
        { "pad":0, "note": 44, "a":[kk.media_previous], "toggle":False, "state":False },   
        { "pad":1, "note": 45, "a":[kk.media_play_pause], "toggle":True, "state":False },   
        { "pad":2, "note": 46, "a":[kk.media_next], "toggle":False, "state":False },   
        { "pad":3, "note": 47, "a":["mylogin",kk.tab], "toggle":False, "state":False },   
        { "pad":4, "note": 48, "a":[kk.shift,"M",kk.shift,"ypassword",kk.enter], "toggle":False, "state":False },   
        { "pad":5, "note": 49, "a":[kk.media_volume_down], "toggle":False, "state":False },   
        { "pad":6, "note": 50, "a":[kk.media_volume_up], "toggle":False, "state":False },   
        { "pad":7, "note": 51, "a":[kk.media_volume_mute], "toggle":True, "state":False },   
        { "pad":8, "note": 36, "a":[kk.shift, kk.tab, kk.shift], "toggle":False, "state":False },   
        { "pad":9, "note": 37, "a":[kk.alt, kk.tab], "toggle":True, "state":False },   
        { "pad":10, "note": 38, "a":[kk.tab], "toggle":False, "state":False },   
        { "pad":11, "note": 39, "a":[kk.ctrl_r, kk.ctrl_r, kk.alt_l, kk.print_screen,kk.alt_l], "toggle":False, "state":False },   
        { "pad":12, "note": 40, "a":["three",kk.tab,"fields",kk.tab,"fulfilled",kk.enter], "toggle":False, "state":False },   
        { "pad":13, "note": 41, "a":[kk.shift,"A",kk.shift,"secondpassword",kk.enter], "toggle":False, "state":False },   
        { "pad":14, "note": 42, "a":[kk.alt,kk.f4,kk.alt], "toggle":False, "state":False },   
        { "pad":15, "note": 43, "a":[kk.ctrl_l, kk.alt_l, pk.KeyCode(76),kk.ctrl_l, kk.alt_l], "toggle":False, "state":False }   
    ],[ #channel/bank 1
        { "pad":0, "note": 44, "a":["Second bank example"], "toggle":True, "state":True }   
    ],[ #channel/bank 2, and so on up to 15
    ],[],[],[],[],[],[],[],[],[],[],[],[],[]
]
