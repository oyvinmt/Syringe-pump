"""
Created on Mon Jun  28 08:14:00 2021

@author: Øyvind Taraldsen

"""


import pygame
import logpy as pumpy
from datetime import datetime
import pygame_textinput
import pygame.freetype
import threading
import time

### sets communication ports for usb-serial, these must be set manually as the computer does not know what the pumps are
com1 = "COM6"
com2 = "COM7"
com3 = "COM8"

run = True

## writes data to a logfile with the current time and date
def write_log(logname ,string):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        with open (logname, "a") as file:
            file.write(dt_string + "    "+ string+ "\n")

## creates logfile
def create_log():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    logname ="Syringe_pump_log"+ dt_string+".txt"
    with open (logname, "w") as file:
        file.write("")
    return logname


#### can be modified for n pumps



logfile = create_log()
current_flowrate1 = ""
current_flowrate2 = ""
current_flowrate3 = ""
sem = threading.Semaphore()

### Gets the flowrate from a pump
def get_flowrate1():
    global run
    while True:
        global current_flowrate1
        sem.acquire()
        new_rate1 = p11.logflowrate()
        sem.release()
        print(new_rate1)
        if new_rate1 != current_flowrate1:
            current_flowrate1 = new_rate1
            flow =current_flowrate1[3:]
            pump = current_flowrate1[0:2]
            write_log(logfile, "Flowrate of pump: 1"+  " is set to: "+flow.rjust(12))
            current_flowrate1= new_rate1
        if run != True:
            write_log(logfile, "Flowrate of pump: 1"+  " is set to: "+flow.rjust(12))
            break
        time.sleep(3.5)

def get_flowrate2():
    global run
    while True:
        global current_flowrate2
        sem.acquire()
        new_rate2 = p12.logflowrate()
        sem.release()
        print(new_rate2)
        if new_rate2 != current_flowrate2:
            current_flowrate2 = new_rate2
            flow =current_flowrate2[3:]
            pump = current_flowrate2[0:2]
            write_log(logfile, "Flowrate of pump: 2" +" is set to: "+flow.rjust(12))
            current_flowrate2= new_rate2
        if run != True:
            write_log(logfile, "Flowrate of pump: 2" +" is set to: "+flow.rjust(12))
            break
    time.sleep(3.5)

def get_flowrate3():
    global run
    while True:
        global current_flowrate3
        sem.acquire()
        new_rate3 = p13.logflowrate()
        sem.release()
        print(new_rate3)
        if new_rate3 != current_flowrate3:
            current_flowrate3 = new_rate3
            flow =current_flowrate3[3:]
            pump = current_flowrate3[0:2]
            write_log(logfile, "Flowrate of pump: 3" +" is set to: "+flow.rjust(12))
            current_flowrate3= new_rate3
        if run != True:
            write_log(logfile, "Flowrate of pump: 3" +" is set to: "+flow.rjust(12))
            break
    time.sleep(3.5)

### main loop, draws to the screen and takes user input
def gameloop():
    pygame.init()
    unit_pump_1 = ""
    unit_pump_2 = ""
    unit_pump_3 = ""
    screen = pygame.display.set_mode((600, 200))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    textinput = pygame_textinput.TextInput(font_family="Arial", font_size = 24)
    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get() 
        for event in events:
            if event.type == pygame.QUIT:
                global run
                run = False
                global chain1
                global chain2
                global chain3
                chain1.close()
                chain2.close()
                chain3.close()
                exit()   
        
        loginfo1 = font.render('Current flowrate pump 1: '+current_flowrate1[3:], True, (0, 0, 0))
        loginfo2 = font.render('Current flowrate pump 2: '+current_flowrate2[3:], True, (0, 0, 0))
        loginfo3 = font.render('Current flowrate pump 3: '+current_flowrate3[3:], True, (0, 0, 0))
        if unit_pump_1 == "":
            inputinfo = font.render('Please set correct unit  ', True, (0, 0, 0))
            inputinfo2 = font.render('for pump 1 (u/h, u/m, u/s):', True, (0, 0, 0))
            if textinput.update(events): 
                unit_pump_1 = textinput.get_text()
                textinput = pygame_textinput.TextInput(font_family="Arial", font_size = 24)
        elif unit_pump_2 =="":
            inputinfo = font.render('Please set correct unit ', True, (0, 0, 0))
            inputinfo2 = font.render('for pump 2 (u/h, u/m, u/s):  ', True, (0, 0, 0))
            if textinput.update(events): 
                unit_pump_2 =textinput.get_text()
                textinput = pygame_textinput.TextInput(font_family="Arial", font_size = 24)
        elif unit_pump_3 =="":
            inputinfo = font.render('Please set correct unit ', True, (0, 0, 0))
            inputinfo2 = font.render('for pump 3 (u/h, u/m, u/s):  ', True, (0, 0, 0))
            if textinput.update(events): 
                unit_pump_3 =textinput.get_text()
                textinput = pygame_textinput.TextInput(font_family="Arial", font_size = 24)
        else:
            inputinfo = font.render('To change flowrate, input pump number ', True, (0, 0, 0))
            inputinfo2 = font.render("followed by a space and the new flowrate:", True, (0, 0, 0))
            # Feed it with events every frame
            if textinput.update(events): 
                new_flowrate = textinput.get_text()

                sem.acquire()
                if new_flowrate[0] == "1":
                    p11.setiflowrate(textinput.get_text()[1:],unit_pump_1)
                elif new_flowrate[0] =="2":
                    p12.setiflowrate(textinput.get_text()[1:],unit_pump_2)
                textinput = pygame_textinput.TextInput(font_family="Arial", font_size = 24)
                sem.release()
        screen.blit(inputinfo,(0,120))
        screen.blit(inputinfo2,(0,140))
        # Blit its surface onto the screen
        screen.blit(loginfo1,(0,0))
        screen.blit(loginfo2, (0,40))
        screen.blit(loginfo3, (0,80))
        screen.blit(textinput.get_surface(), (400, 140))
        
        pygame.display.update()
        clock.tick(30)
    
    


try:
    chain1 = pumpy.Chain(com1)
    p11 = pumpy.Pump(chain1,address=0) 
    flowrate_thread1 = threading.Thread(target=get_flowrate1)
    flowrate_thread1.start()
except:
    print("No pump found, try reconnecting pump 1 on  "+ com1)
try:
    chain2 = pumpy.Chain(com2)
    p12 = pumpy.Pump(chain2, address=0)
    flowrate_thread2 = threading.Thread(target=get_flowrate2)
    flowrate_thread2.start()
except:
    print("No pump found, try reconnecting pump 2 on  "+ com2)
try:
    chain3 = pumpy.Chain(com3)
    p13 = pumpy.Pump(chain3, address = 0)
    flowrate_thread3 = threading.Thread(target=get_flowrate3)
    flowrate_thread3.start()
except:
    print("No pump found, try reconnecting pump 3 on "+ com3)



pygame_thread = threading.Thread(target =gameloop)
pygame_thread.start()