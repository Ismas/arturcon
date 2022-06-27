# ArturCON

ArturCON is a quick Python 3 script for using your old Arturia BeatStep as a physical button launch pad for applications, actions, text macros or almost anything that can be made using a keyboard. Just like Stream Deck and the like, but cheaper.

It's capable of:
* Launch any system shortcut 
* Multimedia actions (mute, play and pause, volumen up and down, etc)
* Write strings (so not have to type them every time) 
* Macros for any app by pressing sequences of keys
* Send direct keycodes

You can define a pad as push-only or toggl. If you want a pad to launch a program, just assign a key combination (including some control keys) to it at the system shortcut configuration, then add the same combo to the script config. If just want to activate some application feature, just add the key combination to Arturcon.

The script also provide aditional functionalities as:
* MIDI monitor (for the BeatStep input).
* MIDI thru, in the case you still need the BeatStep to raw communicate to a plugin.
* Blinkenlights, for you to amaze the world.

All these functionalities can be mixed with the main launchpad one. And if you launch it as "--resident" it will survive a suspension or even a BeatStep disconnection and back to work when you reconnect it. 

ArturCON uses the pads, so leaves the pots free for you to assign to other applications (Jack plugins, for example)

![alt text](https://github.com/Ismas/arturcon/blob/master/arturcon.gif?raw=true)
## How to use
Configure your desired actions, launch the script with the desired parameters, connect your BeatStep, be happy.
Read the How to config section at the bottom of this readme.

```bash
python3 ./arturcon.py --resident --monitor --thru --blinken --process
```
You have 16 pads per bank, and 16 banks  of pads, so plenty of combination and posibilities. To change bank just press [CHAN] + [pad number]. Pads are assigned to channels.

Press briefly the [CHAN] button to relit the pads in case the went not correct. The pads are relight every 10 seconds.


### Installation

You need the following dependencies:
* Python 3
* Mido
* pynput
* Scipy

Use your favorite system package manager or the Python one [pip](https://pip.pypa.io/en/stable/) to install them.

```bash
pip install mido
pip install pynput
pip install scipy
```

### Usage

```bash
$ python3 ./arturcon.py --help
ArturCON, the poor man's button deck V0.0.3

Usage: arturcon [parameters]

	Modes (pick one):
	-p, --process:	Use your BeatStep as a button deck (Default)
		The folowwing modes can be used themselves or added to 'process'
	-m, --monitor:	Just print BeatStep MIDI messages at stout
	-t, --thru:	Just creates a virtual output MIDI port and redirects BeatStep messages (not very practical)
	-b, --blinken:	Awesome astonising blinkenlights on your BeatStep! 

	Options:
	-s, --select:	List and select BeatStep MIDI port (autodetected by default)
	-d, --debug:	Print debug messages at stderr
	-r, --resident:	Keeps looking for BeatStep, for start-at-boot use and make permanent. Disables -s and -d
	-v, --version:	Print version and exits
	-h,?, --help:	This text

```

## How to config

Config is made at the top of the script. You have a dictionary of dictionaries (one for bank) with pad to action assign. Actions are defined as pynput constants. I thing it's pretty autoexplanatory, so just gave it a look. 
First dictionary is bank 0/channel 0, second is bank 1/channel 1, and so on.

```python
{ "pad":1, "note": 45, "a":[kk.media_play_pause], "toggle":True, "state":False },
```
* Pad: is the pad number, starting at 0 and reading left to right and top to bottom. So "1" is the second.
* Note: Don't change this, the script will do it for you.
* a: The actions. It's an array of keys to press, a string or a keychar. You have the possible actions below.
* toggle: Define if the button is toggable instead of push-only. When toggle, the pad will be lit magenta when "on" and red when "off". For example, to enable or disable the mute:
```python
{ "pad":7, "note": 51, "a":[kk.media_volume_mute], "toggle":True, "state":False },   
```
* state: Defines the inital state for a toggle pad..


So you have:
* Keys

kk.caps_lock  
kk.backspace  
kk.delete  
kk.enter  
kk.esc  
kk.menu  
kk.num_lock  
kk.space  
kk.tab  
kk.f1 to kk.f12

* Cursors and special 

kk.left  
kk.right  
kk.up  
kk.down  
kk.insert  
kk.home  
kk.end  
kk.page_up  
kk.page_down  
kk.pause  
kk.print_screen  
kk.scroll_lock  

* Actions

kk.media_next  
kk.media_play_pause  
kk.media_previous  
kk.media_volume_down  
kk.media_volume_mute  
kk.media_volume_up  

* Modifiers:

Modifiers act different to other keys. They keep pressed until you specify them to be realeased by invoking again. 
For example for perform and [ALT}+[F4] to close the focused application:
 ```python
{ "pad":14, "note": 42, "a":[kk.alt,kk.f4,kk.alt], "toggle":False, "state":False },
````

kk.alt
kk.alt_gr  
kk.alt_l  
kk.alt_r  
kk.cmd  
kk.cmd_l  
kk.cmd_r  
kk.ctrl  
kk.ctrl_l  
kk.ctrl_r  
kk.shift  
kk.shift_l  
kk.shift_r  

And also have:
* Strings. Just that. You can combine them with the rest of the actions.
 ```python
 { "pad":3, "note": 47, "a":[kk.shift,"M",kk.shift,"yUser",kk.tab], "toggle":False, "state":False },  
```
* Keycodes
Some keyboard shortcuts do not work with the key and you should provide the keycode. Use them this way:
pk.KeyCode(code)
 ```python
{ "pad":15, "note": 43, "a":[kk.ctrl_l, kk.alt_l, pk.KeyCode(76),kk.ctrl_l, kk.alt_l], "toggle":False, "state":False }   
```

# How it works

ArturCON works by reading BeatStep MIDI input, and asigning note values to actions. For this all pads should be assigned to "General" channel and each pad configured to play one note. You don't have to do this as the script does it for you. AFAIK this will not modify your stored configuration, so just stop Arturcon, recall a config and your are done.

# TODOs
* Make something with the pots
* ?

# Bugs
* Sometimes at the actions the first letter of a string is not recognized as uppercase. In that case do [ kk.shift, "r", kk.shift, "est of the string"]
* Sure, many. Just tell me.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
