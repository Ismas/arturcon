#!env python3
############################################
# ArturCON:
#   An Arturia BeatStep button launchpad
############################################
# Many thanks to Untergeek for the sysex compilation:
# https://www.untergeek.de/2014/11/taming-arturias-beatstep-sysex-codes-for-programming-via-ipad/
# Ismas May-June 2022, 2024
# https://doublepanic.com
# (c) License MIT
# V0.0.6

import sys
import os
import random
import time
import mido as md
import getopt
import threading
import mido.backends.rtmidi
from pynput import keyboard as pk
from pynput.keyboard import Key as kk
from scipy import rand
from time import sleep

# Quick and dirty globalization
import arturconf as cfg
pads = cfg.pads

#####################
# Don't touch below here
##################################                                  
#GLOBALS
kb      = pk.Controller()
tport   = ""
ioport  = ""
chnl    = 0
achnl   = -1
cols    = { "negro": 0x00, "rojo":0x01, "azul":0x10, "magenta":0x11 }
VER     = "0.0.6"
DO_PROC = False
BLINKEN = False
THRU    = False
DEBUG   = False
MONITOR = False
SELECT  = False
RESIDENT= False
CTRLBTN = 0x20
TAIMER  = 60
LEDON   = cols["rojo"]
LEDOFF  = cols["magenta"]
LEDTOUCH = cols["negro"]
###################################

#################
# AUX FUNCTIONS
#############3
def debug(cadena):
    # Mensajes de debug
    if DEBUG: print("DB: ",cadena, file=sys.stderr)

def error(cadena):
    # Mensajes de error
    print("Error: ",cadena, file=sys.stderr)
    sys.exit(1)

def ledon(pad,color=cols["negro"]):
    # Change pad color
    ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x02 ,0x00 ,0x10 ,0x70+pad ,color ]))
    sleep(.0025)
    #debug("Color: Pad "+str(pad)+" col "+str(color))

def monitor(cadena):
    # Imprime los códigos MIDI recibidos
    if MONITOR: print(str(int(time.time())), cadena, file=sys.stderr)

def select_midin():
    global ioport
    debug("select_midin:---------")
    # Menu para que el usuario seleccione un puerto
    mdins = md.get_ioport_names()
    print("\n\nMIDI ports:\n")
    k=0
    for i in mdins:
        k+=1
        print (k,"-",i)
    n = -1    
    while n < 0:
        try:
            n = int(input("\nMIDI port [0 exit]: "))
            if n > k:
                print("Can't see that")
                n = -1
        except:
            print("Just a number, please")
            n = -1
    if (n==0): exit()
    ioport=md.open_ioport(mdins[n-1])

def keycontrol(lista):
    # Invoca a las teclas. Pueden ser letras, códigos sueltos, modificadores o cadenas
    # Totally hate this
    for tecla in lista:
        # Si es un modificador hago "touch" para dar la posibilidad de soltarla en la secuencia
        ltecla = { tecla }
        if ( kk.alt or kk.alt_l ) in ltecla:
            kb.touch(tecla, not kb.alt_pressed)
            continue
        if kk.alt_gr in ltecla:
            kb.touch(tecla, not kb.alt_gr_pressed)
            continue
        if (kk.ctrl or kk.ctrl_l or kk.ctrl_r) in ltecla:
            kb.touch(tecla, not kb.ctrl_pressed)
            continue
        if (kk.shift or kk.shift_l or kk.shift_r ) in ltecla:
            kb.touch(tecla, not kb.shift_pressed)
            continue     
        # Si es cadena, cadena
        if type(tecla)== str: 
            kb.type(tecla)
        # Si no es ni cadena ni modifier, es código suelto
        else:
            kb.tap(tecla)

def pad2nota(pad):
    # Calcula la nota de un pad
    return pad+(44 if pad<8 else 28)

def sysend(cmd,pad,val):
    # Envía un sysex al chisme para configurar
    # encoders: 0x20 -0x2f
    # controles: 0x58 - 0x5F
    # pads: 0x70 - 0x7f
    ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x02 ,0x00 ,cmd, pad, val ]))
    sleep(.01)

def sysread(b1,b2):
    # Envía un sysex al chisme para leer un parámetro.
    # devuelve el mensaje
    # encoders: 0x20 -0x2f
    # controles: 0x58 - 0x5F
    # pads: 0x70 - 0x7f
    ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x01 ,0x00 ,b1, b2]))
    return ioport.receive()

def inictrl():
    # Assign notes to pads in logic
    for j in pads:   # for each channel/bank
       for i in j:   # for each pad
            i["note"] = i["pad"]+44 if i["pad"]<8 else i["pad"]+28

    # Inicia los pads de control.
    # Chan encendido y como nota
    # Nota chan 0x20
    sysend(0x41, 0x04, 0)   # Global acceleation: low
    for i in range(0,8):
        sysend(0x01 ,0x58+i ,0x09)    # comportamiento: nota
        sysend(0x02 ,0x58+i ,0x70)    # canal: 0 
        sysend(0x03 ,0x58+i ,CTRLBTN)    # nota: CTRLBTN
        sysend(0x06 ,0x58+i ,0x01)    # tipo: gate
        sysend(0x10 ,0x58+i ,0x00)    # Luz chan
        sysend(0x10 ,0x5f ,0x11)    # Luz chan
    for i in range(0,16):                 # Comportamiento de los encoders incluyendo el dial
        sysend(0x02 ,0x20+i ,0x00)        # Canal 1 
        sysend(0x03 ,0x20+i ,0x21+i)      # CC NUMBER
        sysend(0x06 ,0x20+i ,0x00)        # absoluto
        sysend(0x04 ,0x20+i ,0x00)        # lowest
        sysend(0x05 ,0x20+i ,0x7f)        # top

def monchan():
    # Monitoriza canal global cada 2 segundos
    # Receive global midi channel 
    global chnl
    m = sysread(0x40,0x06)
    if m.type=='sysex': 
        chnl=m.data[9]
        inipads()
        debug("monchan: canal -> "+str(chnl))

def inipads(force=False):
    # Enciende los pads que sean toggle con el on o off
    # Los reinicia periodicamente
    global achnl
    if ioport != "":
        if chnl != achnl or force:
            for i in range(15): ledon(i)
            achnl = chnl
        for pad in pads[chnl]:
            if pad["toggle"]:
                ledon(pad["pad"],LEDON if pad["state"] else LEDOFF)
        sysend(0x10 ,0x5f ,0x11)    # Luz shift
    # Timer 
    threading.Timer(TAIMER,inipads,args=[True]).start()

def autocon_check():
    global ioport
    debug("autocon_check:---------")
    ioport = ""
    ports= md.get_ioport_names()
    for port in ports:
        debug("Port: "+str(port))
        if "BeatStep:" in port:
            ioport=md.open_ioport(port, autoreset=True)
            return True
    return False

def autocon(recon=False):
    global ioport

    conn = autocon_check()
    if not recon and not conn: 
        error("Not a BeatStep found. None. Try --select for manual MIDI port selection. ")
        exit()
    else:
        while not conn:
            debug("BeatStep not found. Retrying...")
            sleep(2)
            conn = autocon_check()

    debug("Connected to Arturia BeatStep")
    sleep(2)

def watchdog():
    # Comprueba si el chisme sigue enchufado y lo reenchufa
    global ioport
    debug("watchdog:---------")
    ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x01 ,0x00 ,0x40, 0x06]))
    sleep(0.01)
    m = ioport.poll()

    if isinstance(m, type(None)):  
        ioport.close()
        autocon(recon=True) 
        inictrl()
        inipads()

###################################
# Main funcs
#####################################

def monitorMIDI():
    global MONITOR
    debug("monitorMIDI:---------")
    # Monitoriza los mensajes del canal indicado
    MONITOR=True
    for msg in ioport:
        monitor("%s"%(msg) )

def repeater():
    debug("repeater:---------")
    # Ejecuta el MIDI-THRU: Reenvía los mensaje que llegan
    for msg in ioport:
        tport.send(msg)
        monitor(msg)

def procesa():
# Compara los códigos MIDI con la lista para invocar a las tecals
    debug("procesa:---------")
    global chnl

    #for msg in ioport:
    while True:
        msg = None
        count = 0
        while isinstance(msg, type(None)) and count<10000:
            sleep(0.001)
            msg = ioport.poll()
            count += 1

        if count == 10000: 
            watchdog()
            continue

        if msg.type=='note_on' or msg.type=='note_off':
            if  msg.type=='note_off' and msg.note == CTRLBTN: monchan() # Montiroiza boton cambio canal
            for pad in pads[chnl]:
                if (msg.note == pad["note"]): 
                    keycontrol(pad["a"])    
                    debug("Match: "+str(pad["note"])+"- Pad "+ str(pad["pad"])+" a: "+str(pad["a"])+" toggle:"+str(pad["toggle"])+" stat:"+str(pad["state"]))
                    pad["state"] = not pad["state"]
                    # Espera a que se suelte la tecla
                    for msg2 in ioport:
                            if msg2.note == pad["note"] and msg2.type=='note_off': break
                    if pad["toggle"]:
                        ledon(pad["pad"],LEDON if pad["state"] else LEDOFF)
        if THRU: tport.send(msg)
        monitor(msg)

def blinken(lon=False):
    debug("blinken:---------")
    if lon:
        for i in range(4):
            for col in cols:
                for i in range(1,5):
                    ledon(i+3,cols[col])
                    ledon(i+11,cols[col])
                    ledon(4-i,cols[col])
                    ledon(12-i,cols[col])
                    sleep(.05)
                for i in range(5):
                    ledon(i+3)
                    ledon(i+11)
                    ledon(4-i,)
                    ledon(12-i)
                    sleep(.025)
    for i in range(200 if BLINKEN else 50):
        ledon(random.randint(0,15),cols["rojo"])
        ledon(random.randint(0,15),cols["azul"])
        ledon(random.randint(0,15),cols["magenta"])
        ledon(random.randint(0,15),cols["negro"])
        ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x02 ,0x00 ,0x10 ,0x59+random.randint(0,8),random.randint(0,4) ]))
        ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x02 ,0x00 ,0x10 ,0x59+random.randint(0,8),random.randint(0,4) ]))
        ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x02 ,0x00 ,0x10 ,0x59+random.randint(0,8),random.randint(0,4) ]))
        ioport.send(md.Message('sysex',data=[0x00, 0x20, 0x6B, 0x7F ,0x42 ,0x02 ,0x00 ,0x10 ,0x59+random.randint(0,8),random.randint(0,4) ]))
    for i in range(-22,16):
        ledon(i)        

def usage():
    print("ArturCON, the poor man's button deck V"+str(VER))
    print("\nUsage: arturcon [parameters]")
    print("\n\tModes (pick one):")
    print("\t-p, --process:\tUse your BeatStep as a button deck (Default)")
    print("\t\tThe folowwing modes can be used alone or added to 'process'")
    print("\t-m, --monitor:\tJust print BeatStep MIDI messages at stout")
    print("\t-t, --thru:\tJust creates a virtual output MIDI port and redirects BeatStep messages (not very practical)")
    print("\t-b, --blinken:\tAwesome astonising blinkenlights on your BeatStep! ")
    print("\n\tOptions:")
    print("\t-s, --select:\tList and select BeatStep MIDI port (autodetected by default)")
    print("\t-d, --debug:\tPrint debug messages at stderr")
    print("\t-r, --resident:\tKeeps looking for BeatStep, for start-at-boot use and make permanent. Disables -s and -d")
    print("\t-v, --version:\tPrint version and exits")
    print("\t-h, -?, --help:\tThis text\n")

##################################333   
# main
####################################

def main(argv):
    global tport, DEBUG, DO_PROC, THRU, MONITOR, BLINKEN, SELECT, RESIDENT

    # Read arguments
    try:
        opts, args = getopt.getopt(argv,"pmtbdsvrh?",["process","monitor","thru","blinken","select","debug","version","help","resident"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Order is importante
    for opt, arg in opts:
        if opt in ("-h","-?","--help"): 
            usage()
            sys.exit(0)
        if opt in ("-v","--version"): 
            print("V:"+VER)
            sys.exit(0)
        if opt in ("-d","--debug"):     DEBUG = True
        if opt in ("-p","--process"):   DO_PROC = True 
        if opt in ("-t","--thru"):      THRU = True  
        if opt in ("-m","--monitor"):   MONITOR = True  
        if opt in ("-b","--blinken"):   BLINKEN = True
        if opt in ("-s","--select"):    SELECT = True
        if opt in ("-r","--resident"):  
            RESIDENT = True
            SELECT   = False
            DEBUG    = False

    # If thru selected open port
    if THRU: tport = md.open_output("ArturCON_0",True)

    # Use choosen de detection
    select_midin() if SELECT else autocon(RESIDENT)

    # Greeting
    print("Arturcon at your service!")

    if not (MONITOR or BLINKEN or THRU) or DO_PROC:
        blinken(BLINKEN)
        inictrl()
        monchan()
        inipads()
        procesa() 
    if BLINKEN: blinken(True)
    if MONITOR: monitorMIDI()
    if THRU:    repeater()
    debug("END-----------")
if __name__ == "__main__":
    # DETACH!
    #if os.fork(): sys.exit()
    # RRUN!
    main(sys.argv[1:])
