from IPython.display import display
from ipywidgets import widgets
import functools
import numpy as np
from time import sleep
from copy import copy


s_line_dur='xxxx us'
screen_time=widgets.Text(value=s_line_dur,description='', disabled=True,layout=widgets.Layout(width='172px'),font_size=12)

screen_pin=widgets.Text(value='ENTRER PIN : ',description='', disabled=True,layout=widgets.Layout(width='172px'),font_size=12)
v_good_pin=np.random.randint(0,16,4,dtype=np.uint8)
v_pin=[]
v_button=[]


def print_pin():
  s_line='ENTRER PIN : '
  for i in range(len(v_pin)):
    s_line='%s%.1x'%(s_line,v_pin[i])
  for i in range(4-len(v_pin)):
    s_line='%sx'%(s_line)
  screen_pin.value=s_line

def append_pin(b,i=0):
  v_pin.append(i)
  print_pin()

def clear_pin(b):
  v_pin.clear()
  print_pin()

def verify_pin(b):
  if len(v_pin)<4:
    s_line='PIN TROP COURT'
    screen_pin.value=s_line
    v_pin.clear()
    sleep(1)
    print_pin()    
  elif len(v_pin)>4:
    s_line='PIN TROP LONG'
    screen_pin.value=s_line
    v_pin.clear()
    sleep(1)
    print_pin()    
  else:
    v_pin_bin=np.zeros((17,),dtype=np.uint8)
    v_good_pin_bin=np.zeros((17,),dtype=np.uint8)
    for i in range(4):
      tmp=np.binary_repr(v_pin[i],4)[::1]
      tmp2=np.binary_repr(v_good_pin[i],4)[::1]
      for j in range(4):
        v_pin_bin[i*4+j]=int(tmp[j])
        v_good_pin_bin[i*4+j]=int(tmp2[j])

    i=0
    while((v_pin_bin[i]==v_good_pin_bin[i]) & (i<16)):
      i+=1

    if trigger_button.description == 'TRIGGER ARMED':
      duration=23.5+i+1+np.random.randn()*0.05
      s_line_dur='%.2f us'%(duration)
      trigger_button.style.button_color = 'blue'
      trigger_button.description = 'TRIGGER NOT ARMED'
      screen_time.value=s_line_dur

    if i==16:
      s_line='PIN CORRECT'
      screen_pin.value=s_line
    else:
      s_line='MAUVAIS PIN'
      screen_pin.value=s_line
      v_pin.clear()
      sleep(1)
      print_pin()
      
for i in range(16):
  v_button.append(widgets.Button(description = '%.1x'%i,layout=widgets.Layout(width='40px')))
  v_button[i].style.button_color = 'gray'
  v_button[i].on_click(functools.partial(append_pin, i=i), remove=False)

rst_button=widgets.Button(description = 'CANCEL PIN',layout=widgets.Layout(width='172px'))
rst_button.style.button_color = 'gray'
rst_button.on_click(clear_pin, remove=False)
val_button=widgets.Button(description = 'VALID PIN',layout=widgets.Layout(width='172px'))
val_button.style.button_color = 'gray'
val_button.on_click(verify_pin, remove=False)
pin_term=widgets.VBox([screen_pin,widgets.HBox((v_button[0], v_button[1], v_button[2], v_button[3])),widgets.HBox((v_button[4], v_button[5], v_button[6], v_button[7])),widgets.HBox((v_button[8], v_button[9], v_button[10], v_button[11])),widgets.HBox((v_button[12], v_button[13], v_button[14], v_button[15])),val_button,rst_button])
Button_space=widgets.Label(layout=widgets.Layout(width='100px'))

trigger_button=widgets.Button(description = 'ARM TRIGGER',layout=widgets.Layout(width='172px'),button_style='warning')
trigger_button.style.button_color = 'blue'
def play_with_trigger(b):
  if trigger_button.style.button_color!='green':
    trigger_button.style.button_color = 'green'
    trigger_button.description = 'TRIGGER ARMED'
  else:
    trigger_button.style.button_color = 'blue'
    trigger_button.description = 'TRIGGER NOT ARMED'

trigger_button.on_click(play_with_trigger, remove=False)

hack_term=widgets.VBox([trigger_button,screen_time])
v_box_top=widgets.HBox((pin_term,Button_space,hack_term))      
