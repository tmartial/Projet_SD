###############
#   IMPORTS   #
###############

from gettext import ngettext
import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import *
from tkinter.messagebox import askokcancel, showinfo, WARNING
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image #(sudo) pip3 install pillow
import os

import AEmodules as AEM
import genalg 
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

def on_click(number):
    if button_end['state']=='normal':
        return 0

    print(all_buttons[number])
    all_buttons[number].configure(highlightbackground='red')

    answer = askokcancel(
        title='Confirmation',
        message='Do you want to select this portrait as final portrait?',
        icon=WARNING)

    if answer:
        portraits = AEM.decode_faces(encoded_faces_6)
        end(portraits[number])

    else :
        for i in range(6):
            all_buttons[i].configure(activebackground='#d9d9d9')
        all_buttons[number].configure(highlightbackground='#d9d9d9')
        button_next.configure(state='normal')
        button_recharge.configure(state='normal')
        button_end.configure(state='normal')

class Portrait(Button):
    def __init__(self, master, number, image):
        Button.__init__(self, master, image=image,command=lambda: on_click(number))


## Variables de contrôle #######################################################################
selected_lvl0 = tk.StringVar()
selected_lvl1 = tk.StringVar()
selected_lvl2 = tk.StringVar()
selected_lvl3 = tk.StringVar()
selected_lvl4 = tk.StringVar()
selected_lvl5 = tk.StringVar()
selected_lvl=[selected_lvl0,selected_lvl1,selected_lvl2,selected_lvl3,selected_lvl4,selected_lvl5]
lvls = (('not at all similar', 0.1),
         ('similar', 0.5),
         ('very similar', 0.9))
index = IntVar(root, value = 1)

## Fonctions ###################################################################################

def show_portraits(portraits):
    ''' This function shows 6 portaits and relative comboboxes into a grid for the notation.
        
        Parameters
        ----------
        portraits : np.array
            a population of 6 portraits
    '''

    global all_radiob
    global all_buttons
    global selected_lvl
    all_buttons=[]
    all_radiob=[]
    number=0

    for number in range(6):
        #liste=os.listdir("./img")
        #imgpath = "./img" +'/'+liste[number] 
        resize_image = image.array_to_img(portraits[number]).resize((250, 200))
        img = ImageTk.PhotoImage(resize_image)

        button=Portrait(root,image=img,number=number)   #button = Portrait(root,number=number,image=img)
        button.photo = img   # assign to class variable to resolve problem with bug in `PhotoImage`
        if number<3:
            R=1
            C=number
        else :
            R=5
            C=number-3

        button.grid(row=R, column=C)
        for lvl in lvls:
            r = Radiobutton(root, text=lvl[0], value=lvl[1], variable=selected_lvl[number])
            r.grid(row=R+1, column=C)
            R+=1  
            all_radiob.append(r)

        #lvl = ttk.Combobox(root, textvariable='selected_lvl'+str(number))
        #lvl['values'] = ["not at all similar","similar","very similar"]
        #lvl['state'] = 'readonly'
        #lvl.grid(row=R+1, column=C)
        
        all_buttons.append(button)
        #all_cb.append(lvl)

        
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=int(0.3)) # nothing
    root.grid_rowconfigure(1, weight=1) # images
    root.grid_rowconfigure(2, weight=int(0.3)) # radiobutton
    root.grid_rowconfigure(3, weight=int(0.3)) # radiobutton
    root.grid_rowconfigure(4, weight=int(0.3)) # radiobutton
    root.grid_rowconfigure(5, weight=1) # images
    root.grid_rowconfigure(6, weight=int(0.3)) # radiobutton
    root.grid_rowconfigure(7, weight=int(0.3)) # radiobutton
    root.grid_rowconfigure(8, weight=int(0.3)) # radiobutton
    root.grid_rowconfigure(9, weight=1) # selection
    root.grid_rowconfigure(10, weight=2) # nothing



def start():
    ''' This function changes the home window into an image notation window.

        It destroys the text labels, add a label 'selection', changes the command 
        and the text of 'button_next' and call the function show_portaits().
    '''

    welcome.destroy()
    intro.destroy()

    show_portraits(portraits)

    ind=index.get()
    selection = Label(root, 
            text='Selection '+str(ind)+'/10')
    selection.grid(row=9, column=1)

    button_next.configure(text='Confirm selection')
    button_next.configure(command=confirm)
    button_next.place(relx=0.5, rely=0.95,anchor='center')

    
    button_recharge.place(relx=0.2, rely=0.95,anchor='center')
    button_end.place(relx=0.8, rely=0.95,anchor='center')



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


def end(img):
    ''' This function changes the image notation window into a end window.

        It destroys the grid with the portraits and the combobox, destroys the buttons, 
        add a label, shows the final portrait and add a button to save it.
    '''

    button_next.destroy()
    button_recharge.destroy()
    button_end.destroy()

    for button in root.grid_slaves():
        button.grid_forget()

    end = Label(root,text='Here is your portrait !',font=("Helvetica", 30))
    end.place(relx=0.5, rely=0.2,anchor='center')

    #image=Image.open('./img/jack.jpeg')
    #pic=ImageTk.PhotoImage(image)
    resize_image = image.array_to_img(img).resize((250, 200))
    pic = ImageTk.PhotoImage(resize_image)
    last_img = Label(root,image=pic)
    last_img.photo=pic
    last_img.place(relx=0.5, rely=0.5,anchor='center')

    button_save = tk.Button(
        root,
        text="Save portrait",
        command = lambda : SaveFile(resize_image)
    )
    button_save.place(relx=0.5, rely=0.8,anchor='center')


def recharge():
    ind=index.get()
    global encoded_faces_6
    global note
    if ind==1 :
        encoded_faces_6 = encoded_faces[np.random.choice(encoded_faces.shape[0], 6, replace=False), :]
    else :
        encoded_faces_6 = genalg.new_generation(encoded_faces_6,note,1,1,1,6,1)    
    portraits = AEM.decode_faces(encoded_faces_6)
    show_portraits(portraits)


def choose_portrait():
    for i in range(6):
        all_buttons[i].configure(activebackground='#345')
    button_next.configure(state='disabled')
    button_recharge.configure(state='disabled')
    button_end.configure(state='disabled')


def confirm():
    ''' This function allows to confirm the notations.

        It shows an askokcancel box. If 'ok' is selected, it goes to the next portrait selection.
        If it's the 5th selection, it calls the function end().

        Raises
        ------
        Warning
            If a portrait got no notation
    '''
    global selected_lvl 
    
    i=0
    for i in range(6):
        if selected_lvl[i].get()=="":
            messagebox.showinfo(title='Warning', 
                message='Please select a notation for each portrait',
                icon=WARNING)
            return 0

    answer = askokcancel(
        title='Confirmation',
        message='Do you want to confirm your selection?',
        icon=WARNING)

    if answer:
        ind=index.get()
        ind+=1
        selection = Label(root,text='Selection '+str(ind)+'/10')
        selection.grid(row=9, column=1)
        index.set(ind)
        j=0
        all_lvl=[]
        for j in range(6):
            all_lvl.append(float(selected_lvl[j].get()))
            global note
            note = np.array(all_lvl)
            selected_lvl[j].set("")
        print(all_lvl)
        global encoded_faces_6
        encoded_faces_6 = genalg.new_generation(encoded_faces_6,note,1,1,1,6,1)
        portraits = AEM.decode_faces(encoded_faces_6)
        show_portraits(portraits)

        if ind==5:
            portraits = AEM.decode_faces(encoded_faces_6)
            end(portraits[0])


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
encoded_faces = np.loadtxt("./encoded_faces_05_04_bis.txt")
# Choix de 6 images au hasard
encoded_faces_6 = encoded_faces[np.random.choice(encoded_faces.shape[0], 6, replace=False), :]
portraits = AEM.decode_faces(encoded_faces_6)


button_next = tk.Button(
    root,
    text="Start identification",
    command=start
)
button_next.place(relx=0.5, rely=0.95,anchor='center')

button_recharge = tk.Button(
    root,
    text="No portrait matches...",
    command=recharge
)

button_end = tk.Button(
    root,
    text="There is my portrait !",
    command=choose_portrait
)

root.mainloop()

