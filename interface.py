###############
#   IMPORTS   #
###############

import tkinter as tk
from tkinter import *
from tkinter.messagebox import askokcancel, showinfo, WARNING
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image
import os


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
    

# decoded_imgs[i] 

def show_portraits():
    global all_buttons
    all_buttons=[]
    print(all_buttons)
    number=0
    
    liste=os.listdir("./img") # Recupere le nom de tous les fichiers d'un dossier

    for number in range(6):
        imgpath = "./img" +'/'+liste[number] ## strchemin:str, chemin d'accès à l'image  
        resize_image = Image.open(imgpath).resize((218, 178))
        img = ImageTk.PhotoImage(resize_image)  ## Chargement d'une image à partir de PIL
    
        button = Portrait(root,number=number,image=img)
        button.photo = img   # assign to class variable to resolve problem with bug in `PhotoImage`
        if number<3:
            button.grid(row=1, column=number)
        else :
            button.grid(row=2, column=number-3)
        
        all_buttons.append(button)
        
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=2)
    root.grid_rowconfigure(2, weight=2)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=3)


index = IntVar(root, value = 1)
def start():
    welcome.destroy()
    intro.destroy()
    show_portraits()
    ind=index.get()
    selection = Label(root, 
            text='Selection '+str(ind)+'/10')
    selection.grid(row=4, column=1)
    button_next.configure(text='Confirm selection')
    button_next.configure(state='disabled')
    button_next.configure(command=confirm)


def SaveFile(img):
    #data = [('All tyes(*.*)', '*.*')]
    file = asksaveasfile(mode='w', defaultextension = '.jpeg')
    if file :
        img.save(file)


def end():
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
    ind=index.get()
    answer = askokcancel(
        title='Confirmation',
        message='You have selected '+str(select.get())+' image(s). Do you want to confirm your selection?',
        icon=WARNING)

    if answer:
        ind+=1
        selection = Label(root,text='Selection '+str(ind)+'/10')
        selection.grid(row=4, column=1)
        index.set(ind)
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
    text="This software allows you to create a robot portrait from an image bank.\nChoose the faces that most resemble the person concerned.\nYou can choose between 1 and 6 images at a time by clicking on it, during 10 selections.\nBe careful! You can't go back on your selection.",
    font=("Helvetica", 15))
intro.pack()
intro.place(relx=0.5, rely=0.5,anchor='center')

button_next = tk.Button(
    root,
    text="Start identification",
    command=start
)
button_next.place(relx=0.5, rely=0.95,anchor='center')


root.mainloop()

