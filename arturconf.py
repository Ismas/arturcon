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
        { "pad":0, "a":[kk.media_previous], "toggle":False, "state":False },   
        { "pad":1, "a":[kk.media_play_pause], "toggle":True, "state":False },   
        { "pad":2, "a":[kk.media_next], "toggle":False, "state":False },   
        { "pad":3, "a":["mylogin",kk.tab], "toggle":False, "state":False },   
        { "pad":4, "a":[kk.shift,"M",kk.shift,"ypassword",kk.enter], "toggle":False, "state":False },   
        { "pad":5, "a":[kk.media_volume_down], "toggle":False, "state":False },   
        { "pad":6, "a":[kk.media_volume_up], "toggle":False, "state":False },   
        { "pad":7, "a":[kk.media_volume_mute], "toggle":True, "state":False },   
        { "pad":8, "a":[kk.shift, kk.tab, kk.shift], "toggle":False, "state":False },   
        { "pad":9, "a":[kk.alt, kk.tab], "toggle":True, "state":False },   
        { "pad":10,"a":[kk.tab], "toggle":False, "state":False },   
        { "pad":11,"a":[kk.ctrl_r, kk.ctrl_r, kk.alt_l, kk.print_screen,kk.alt_l], "toggle":False, "state":False },   
        { "pad":12,"a":["three",kk.tab,"fields",kk.tab,"fulfilled",kk.enter], "toggle":False, "state":False },   
        { "pad":13,"a":[kk.shift,"A",kk.shift,"secondpassword",kk.enter], "toggle":False, "state":False },   
        { "pad":14,"a":[kk.alt,kk.f4,kk.alt], "toggle":False, "state":False },   
        { "pad":15,"a":[kk.ctrl_l, kk.alt_l, pk.KeyCode(76),kk.ctrl_l, kk.alt_l], "toggle":False, "state":False }   
    ],[ #channel/bank 1
        { "pad":0, "a":["Second bank example"], "toggle":True, "state":True }   
    ],[ #channel/bank 2, and so on up to 15
    ],[],[],[],[],[],[],[],[],[],[],[],[],[]
]
