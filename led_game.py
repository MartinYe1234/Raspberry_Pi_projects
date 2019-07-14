"""
LED Button Game with a GUI
requires a breadboard,leds and buttons
sometimes there is some lag between when the buttons are pushed and when they register
Made by Martin Ye
"""

"""
Import statements
"""
import RPi.GPIO as GPIO
from random import randint
from time import sleep
from Tkinter import *
import tkMessageBox as box

#setting the Tkinter GUI window
window = Tk()
window.title("LED Game")

frame = Frame(window)
"""
Setting up input/output pins on the pi
"""
#GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#set up leds as outputs
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

#set up buttons as inputs
GPIO.setup(8,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(10,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(12,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(16,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(22,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

#dictionaries that links the GPIO pins to the numbering
leds = {'0':7,'1':11,'2':13,'3':15,'4':19,'5':21}
buttons = {8:'0',10:'1',12:'2',16:'3',18:'4',22:'5'}

#global variables needed
answer = []
plyr = []
amount = 5
blink_time = 0.75
pressed = 0


#creates the mode by changing amount of leds flashing and blink_time
def create_mode(mode):
    global amount, blink_time, create_mode
    if mode == "Easy":
        amount = 5
        blink_time = 0.75
        return mode
    elif mode == "Hard":
        amount = 7
        blink_time = 0.5
        return mode
    elif mode == "Chronic Sadness":
        amount = 9
        blink_time = 0.2
        return mode
    else:
        book = "Easy"
        return book
    

#generates sequence and flashes lights
def play():
    #generates the sequence of led flashes
    for i in range(amount):
        led = randint(0,5)
        answer.append(str(led))
            
    #flashes on and off. On time depends on difficulty, off time is set at 0.1 seconds        
    for led in answer:
        GPIO.output(leds[led], True)
        sleep(blink_time)
        GPIO.output(leds[led], False)
        sleep(0.1)


#gets input from player, checks it and outputs result
def check_answer():
    global pressed,answer,plyr,amount,blink_time

    #this will make sure the code waits until the player finishes entering the buttons
    while pressed < amount:
        True
        
    #checks if player was correct
    if plyr == answer:
        box.showinfo("Game Status","You got it correct! Good job!")
    else:
        box.showinfo("Game Status","You suck.\nYou entered:\n" + str(plyr) + "\nThe answer is\n" + str(answer))

    #reset values
    answer = []
    plyr = []
    amount = 5
    blink_time = 0.75
    pressed = 0

        
#checks input from buttons, returns a list
#when the led flashes, that means it registered
def button_press(channel):
    global plyr, pressed
    plyr.append(buttons[channel])
    GPIO.output(leds[buttons[channel]],True)
    sleep(0.1)
    GPIO.output(leds[buttons[channel]],False)
    pressed += 1


"""
function that runs when the dialogue box is open
apparently nothing else in the code runs when the dialogue box is open, which is why
literally everything happens in this function
"""
def dialog():
    global amount
    #ask player to make selections
    box.showinfo("Selection", "Your Choice: \n" + book.get() + "\n\nLights will start flashing 2 seconds after you press OK")
    create_mode(book.get())
    #pause for 2 seconds to give player chance to look at breadboard
    sleep(2)
    #flash the lights
    play()
    box.showinfo("Answer","Please press OK, then enter the correct sequence.")
    #check input and output answers and stuff
    check_answer()

"""
Adding event handlers for when buttons are pressed
"""

#set callback handlers for the button presses
GPIO.add_event_detect(8,  GPIO.RISING, callback=button_press,bouncetime=250)
GPIO.add_event_detect(10, GPIO.RISING, callback=button_press,bouncetime=250)
GPIO.add_event_detect(12, GPIO.RISING, callback=button_press,bouncetime=250)
GPIO.add_event_detect(16, GPIO.RISING, callback=button_press,bouncetime=250)
GPIO.add_event_detect(18, GPIO.RISING, callback=button_press,bouncetime=250)
GPIO.add_event_detect(22, GPIO.RISING, callback=button_press,bouncetime=250)


""" 
Text for dialogue box and formatting
"""
txt1 = Label(window, text = "WELCOME TO LIGHT FLASHY GAME")
txt2 = Label(window, text = "A sequence of LED's will flash on and off.")
txt3 = Label(window, text = "After the lights finish flashing, press the buttons below in the correct order.")
txt4 = Label(window, text = "When you input the sequence, the corresponding light will light up.")
txt5 = Label(window, text = "Wait for the LED to turn off before pressing the next button.")
txt6 = Label(window, text = "If no difficulty is selected, it will default to Easy.")
txt7 = Label(window, text = "Select your difficulty: ")

txt1.pack(padx = 100, pady = 10)
txt2.pack(padx = 100, pady = 10)
txt3.pack(padx = 100, pady = 10)
txt4.pack(padx = 100, pady = 10)
txt5.pack(padx = 100, pady = 10)
txt6.pack(padx = 100, pady = 10)
txt7.pack(padx = 100, pady = 10)

#close button
btn_sel = Button(window, text = "Select", command = dialog)

#store the selections
book = StringVar()
"""
setting up the choices (radio buttons)
"""
#set up options for selections
radio_1 = Radiobutton(frame, text = "Easy", variable = book, value = "Easy")
radio_2 = Radiobutton(frame, text = "Hard", variable = book, value = "Hard")
radio_3 = Radiobutton(frame, text = "Chronic Sadness", variable = book, value = "Chronic Sadness")

#button
btn_sel.pack(side = RIGHT)
radio_1.pack(side = LEFT)
radio_2.pack(side = LEFT)
radio_3.pack(side = LEFT)
frame.pack(padx = 20, pady = 20)

#open dialogue box
window.mainloop()