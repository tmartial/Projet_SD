###############
#   IMPORTS   #
###############

import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import *
from tkinter.messagebox import askokcancel, showinfo, WARNING
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image #(sudo) pip3 install pillow
import os

import AEmodules as AEM
from keras.preprocessing import image
import numpy as np


#########################
#   WINDOW PARAMETERS   #
#########################

root = tk.Tk()
root.title('PROJET EETO')

window_width = 900
window_height = 700
root.resizable(False, False)

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


######################
#   IDENTIFICATION   #
######################

## Sélection par choix #########################################################################
"""
select = IntVar(root, value = 0)
def on_click(number):
    print(all_buttons[number])
    if  all_buttons[number]['highlightbackground']=='red':
        all_buttons[number].configure(highlightbackground='#d9d9d9')
    else :
        all_buttons[number].configure(highlightbackground='red')

    for i in range(6):
        if  all_buttons[i]['highlightbackground']=='red':
            button_next.configure(state='active')
            break
        else:
            button_next.configure(state='disabled')
    
    sel=0
    for i in range(6):
        if  all_buttons[i]['highlightbackground']=='red':
            sel+=1
            select.set(sel)   

class Portrait(Button):
    def __init__(self, master, number, image):
        Button.__init__(self, master, image=image,command=lambda: on_click(number),activebackground='#345')
 """ 

## Variables globales ##########################################################################
selected_lvl0 = tk.StringVar()
selected_lvl1 = tk.StringVar()
selected_lvl2 = tk.StringVar()
selected_lvl3 = tk.StringVar()
selected_lvl4 = tk.StringVar()
selected_lvl5 = tk.StringVar()
index = IntVar(root, value = 1)
global decoded_faces 


## Fonctions ###################################################################################
def show_portraits():
    ''' This function shows 6 portaits and relative comboboxes into a grid for the notation.
        
        Parameters
        ----------
        list : np.array
            a population of 6 portraits
    '''

    global all_cb
    all_cb=[]
    number=0

    portraits = decoded_faces[np.random.choice(decoded_faces.shape[0], 6, replace=False), :]

    for number in range(6):
        #liste=os.listdir("./img")
        #imgpath = "./img" +'/'+liste[number] 
        #resize_image = Image.open(imgpath).resize((218, 178))
        #img = ImageTk.PhotoImage(resize_image)
        img = ImageTk.PhotoImage(image.array_to_img(portraits[number]))

        button=Label(root,image=img)   #button = Portrait(root,number=number,image=img)
        button.photo = img   # assign to class variable to resolve problem with bug in `PhotoImage`
        if number<3:
            R=1
            C=number
        else :
            R=3
            C=number-3

        button.grid(row=R, column=C)
        lvl = ttk.Combobox(root, textvariable='selected_lvl'+str(number))
        lvl['values'] = ["not at all similar","similar","very similar"]
        lvl['state'] = 'readonly'
        lvl.grid(row=R+1, column=C)
        
        #all_buttons.append(button)
        all_cb.append(lvl)
        
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=2)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=2)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=2)


def start():
    ''' This function changes the home window into an image notation window.

        It destroys the text labels, add a label 'selection', changes the command 
        and the text of 'button_next' and call the function show_portaits().
    '''

    welcome.destroy()
    intro.destroy()
    show_portraits()
    ind=index.get()
    selection = Label(root, 
            text='Selection '+str(ind)+'/10')
    selection.grid(row=5, column=1)
    button_next.configure(text='Confirm selection')
    #button_next.configure(state='disabled')
    button_next.configure(command=confirm)


def notation(list):
    ''' This function changes the list of notations from strings to integrers.

        - not at all similar = 0.1
        - similar = 0.5
        - very similar = 0.9
        
        Parameters
        ----------
        list : list[str]
            a list of the notations

        Returns
        -------
        list[int]
            a list of int (0.1, 0.5, 0.9)
    '''

    i=0
    for i in range(len(list)):
        if list[i]=="not at all similar":
            list[i]=0.1
        elif list[i]=="similar":
            list[i]=0.5
        elif list[i]=="very similar":
            list[i]=0.9

    return list


def SaveFile(img):
    ''' This function allows to save an image in .jpeg format.
        
        Parameters
        ----------
        img : np.array
            a vector of the final portrait
    '''

    #data = [('All tyes(*.*)', '*.*')]
    file = asksaveasfile(mode='w', defaultextension = '.jpeg')
    if file :
        img.save(file)


def end():
    ''' This function changes the image notation window into a end window.

        It destroys the grid with the portraits and the combobox, destroys the 'button_next', 
        add a label, shows the final portrait and add a button to save it.
    '''

    button_next.destroy()
    for button in root.grid_slaves():
        button.grid_forget()

    end = Label(root,text='Here is your portrait !',font=("Helvetica", 30))
    end.place(relx=0.5, rely=0.2,anchor='center')

    image=Image.open('./img/jack.jpeg')
    pic=ImageTk.PhotoImage(image)
    last_img = Label(root,image=pic)
    last_img.photo=pic
    last_img.place(relx=0.5, rely=0.5,anchor='center')

    button_save = tk.Button(
        root,
        text="Save portrait",
        command = lambda : SaveFile(image)
    )
    button_save.place(relx=0.5, rely=0.8,anchor='center')


def confirm():
    ''' This function allows to confirm the notations.

        It shows an askokcancel box. If 'ok' is selected, it goes to the next portrait selection.
        If it's the 3th selection, it calls the function end().

        Raises
        ------
        Warning
            If a portrait got no notation
    '''

    i=0
    for i in range(6):
        if all_cb[i].get()=="":
            messagebox.showinfo(title='Warning', 
                message='Please select a notation for each portrait',
                icon=WARNING)
            return 0

    ind=index.get()
    answer = askokcancel(
        title='Confirmation',
        message='Do you want to confirm your selection?',
        icon=WARNING)

    if answer:
        ind+=1
        selection = Label(root,text='Selection '+str(ind)+'/10')
        selection.grid(row=4, column=1)
        index.set(ind)

        j=0
        all_lvl=[]
        for j in range(6):
            all_lvl.append(all_cb[j].get())
            notation(all_lvl)
            all_cb[j].set("")
        print(all_lvl)
        show_portraits()

        if ind==3:
            end()


############
#   MAIN   #
############

welcome = Label(root, 
    text='Welcome to the EETO Project !',
    font=("Helvetica", 30))
welcome.pack()
welcome.place(relx=0.2, rely=0.2)

intro = Label(root, 
    text="This software allows you to create a robot portrait from an image bank.\nChoose a notation for each portrait using the combobox.\nYou can choose between 3 notations : 'not at all similar','similar' and 'very similar'\nThere are 10 selections with 6 portraits to note each time.\nBe careful! You can't go back on your selection.",
    font=("Helvetica", 15))
intro.pack()
intro.place(relx=0.5, rely=0.5,anchor='center')

# Charge les 400 images encodées
encoded_faces = np.loadtxt("encoded_faces_05_04_bis.txt")
decoded_faces = AEM.decode_faces(encoded_faces)

button_next = tk.Button(
    root,
    text="Start identification",
    command=start
)
button_next.place(relx=0.5, rely=0.95,anchor='center')


root.mainloop()

