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

## Variables de contrôle ##########################################################################

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


## Sélection par choix ############################################################################

def on_click(number):
    ''' This function defines the Portrait selected as the final portrait.
        
        When a Portrait is selected, its highlightbackground changes in red.
        It shows an askokcancel box :
            If 'ok' is selected, it calls the function end() with the selected Portrait as final portrait. 
            If 'cancel' is selected, the buttons are reactivated, the highlightbackground of the selected 
            Portrait and the activebackgrounds are removed.
        
        Parameters
        ----------
        number : int
            the id of the portrait clicked [0-5]

        Raises
        ------
        Return 0
            If 'button_end' isn't clicked
    '''
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
    ''' This class defines what is a Portrait.
        
        A Portrait is a button with an image and an id.
        
        Parameters
        ----------
        master
            the parent window
        number
            the id of the portrait
        image
            the image of the portrait

        Example
        --------
        >>>liste=os.listdir("./img")
        >>>imgpath = "./img" +'/'+liste[1]
        >>>image=Image.open(imgpath)
        >>>img = ImageTk.PhotoImage(image)
        >>>portrait=Portrait(root,image=img,number=1)   
        >>>portrait.photo = img   # resolve problem with bug in `PhotoImage`
        >>>portrait.pack(ipadx=10,ipady=10)
    '''
    def __init__(self, master, number, image):
        Button.__init__(self, master, image=image,command=lambda: on_click(number))




## Sélection par notation ###################################################################################

def show_portraits(portraits):
    ''' This function shows 6 Portaits and relative radiobuttons into a grid for the notation.

        Each Portrait has 3 radiobuttons underneath : 'not at all similar', 'similar' and 'very similar'.
        Only 1 of these 3 radiobuttons can be selected.

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

        button=Portrait(root,image=img,number=number) 
        button.photo = img   # resolve problem with bug in `PhotoImage`
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


## Changement de fenêtre ##########################################################################

def start():
    ''' This function changes the home window into an image notation window.

        It destroys the text labels, add a label 'selection', changes the command and the text of 'button_next', 
        places and enables the 'button_recharge' and the 'button_end' and calls the function show_portaits().
    '''

    welcome.destroy()
    intro.destroy()

    show_portraits(portraits)

    ind=index.get()
    selection = Label(root, 
            text='Selection '+str(ind)+'/5')
    selection.grid(row=9, column=1)

    button_next.configure(text='Confirm selection')
    button_next.configure(command=confirm)
    button_next.place(relx=0.5, rely=0.95,anchor='center')

    button_recharge.configure(state='normal')
    button_recharge.place(relx=0.2, rely=0.95,anchor='center')
    button_end.configure(state='normal')
    button_end.place(relx=0.8, rely=0.95,anchor='center')


def recharge():
    ''' This function recharges the 6 Portraits displayed.

        If no selection has been done, it chooses 6 new faces from the encoded ones.
        If selection has been done, it calls again the function new_generation() with the previous selection.
    '''
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
    ''' This function allows to select a Portrait as the final portrait.
        
        The Portrait's activebackgrounds changes in black.
        The 'button_next', 'button_recharge' and 'button_end' are disabled.
    '''
    for i in range(6):
        all_buttons[i].configure(activebackground='#345')
    button_next.configure(state='disabled')
    button_recharge.configure(state='disabled')
    button_end.configure(state='disabled')


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

        It hides the grid with the Portraits and the radiobuttons, hides the 'button_recharge' and the 'button_end',
        add a label, shows the final portrait, add a button to save it and modify the 'button_next' into a
        restart button.
    '''

    button_recharge.place_forget()
    button_end.place_forget()

    for button in root.grid_slaves():
        button.grid_forget()

    end_lbl.place(relx=0.5, rely=0.2,anchor='center')

    #image=Image.open('./img/jack.jpeg')
    #pic=ImageTk.PhotoImage(image)
    resize_image = image.array_to_img(img).resize((250, 200))
    pic = ImageTk.PhotoImage(resize_image)
    last_img.configure(image=pic)
    last_img.photo=pic
    last_img.place(relx=0.5, rely=0.5,anchor='center')

    button_save.configure(command = lambda : SaveFile(resize_image))
    button_save.place(relx=0.5, rely=0.8,anchor='center')

    button_next.configure(text='Restart')
    button_next.configure(command=lambda:[reset(),start()])
    button_next.configure(state='normal')
    button_next.place(relx=0.5, rely=0.95,anchor='center')


def reset():
    ''' This function allows to hide the end window and reset the first 6 Portraits.
        
        It hides the label, the 'button_save' and the 'last_img'. 
        It chooses 6 new faces from the encoded ones.
        It set the index to '1'.
    '''
    end_lbl.place_forget()
    button_save.place_forget()
    last_img.place_forget()

    global encoded_faces_6
    global portraits
    encoded_faces_6 = encoded_faces[np.random.choice(encoded_faces.shape[0], 6, replace=False), :]
    portraits = AEM.decode_faces(encoded_faces_6)

    index.set(1)


def confirm():
    ''' This function allows to confirm the notations.

        It shows an askokcancel box :
            If 'ok' is selected, it goes to the next portrait selection. All notations are collected inside
            a list of int (note: 0.1, 0.5, 0.9). Then the notations are reset, and it calls the function
            new_generation() with the 6 faces, the list note and other parameters predefined. Then it calls
            the function show_portraits() with the new faces generated.
            If it's the 6th selection, it calls the function end() with the first Portrait of the final selection.
 
            If 'cancel' is selected, it closes the askokcancel box.

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
        selection = Label(root,text='Selection '+str(ind)+'/5')
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
        encoded_faces_6 = np.append(encoded_faces_6, encoded_faces[np.random.choice(encoded_faces.shape[0], 1, replace=False), :],axis = 0)
        note = np.append(note, 0.2)
        encoded_faces_6 = genalg.new_generation(encoded_faces_6,note,1,0.8,0.1,6,2.5)
        portraits = AEM.decode_faces(encoded_faces_6)
        show_portraits(portraits)

        if ind==6:
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
    text="This software allows you to create a robot portrait from an image bank.\n\nChoose between 3 notations for each portrait : 'not at all similar','similar' or 'very similar'\nThere are 5 selections with 6 portraits to note each time.\n\nYou can recharge the generated portraits or choose the final one\nat any time by clicking on the corresponding button.\n\nBe careful! You can't go back on your selection.",
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

button_save = tk.Button(
        root,
        text="Save portrait"
    )

end_lbl = Label(root,text='Here is your portrait !',font=("Helvetica", 30))

last_img = Label(root,image=ImageTk.PhotoImage(image.array_to_img(portraits[0])))

root.mainloop()

