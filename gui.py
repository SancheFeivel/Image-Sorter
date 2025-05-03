from tkinter import *
from tkinter.scrolledtext import ScrolledText
import image_sorter as sorter
import types
import sys
import threading


def redirect_stdout(widget):
    def write(s):
        widget.insert(END, s)
        widget.see(END)
        widget.update_idletasks()
    def flush():
        pass
    return types.SimpleNamespace(write=write, flush=flush)

w = 720
h = 480

hell = "Helvetica", 20


root = Tk()
root.resizable(False, False)
root.title("")
root.geometry(f"{w}x{h}")
root.configure(bg="blue")

def start_main_screen():
    main_screen = Frame(root, bg="black")
    main_screen.place(relheight=1, relwidth=1)

    Folder_text = Label(main_screen,text="Input Folder:", font=(hell), fg="white", bg="black")
    Folder_text.pack(pady=4, padx= 10,side="top", anchor="nw")
    
    Folder_input = Entry(main_screen, font=(hell), width=400)
    Folder_input.configure(bg="black", fg= "white")
    Folder_input.pack (pady=4, padx= 10,side="top", anchor="nw")
    

    Start_button = Button(main_screen, text= "Submit", font=(hell), command=lambda:submit_clicked(Folder_input))
    Start_button.config(fg="white", bg="black")
    Start_button.pack(pady=4, padx= 10,side="top", anchor="nw")
    

def submit_clicked(Folder_input):
    global sorter_thread
    output_screen()
    sorter.working_folder = Folder_input.get()
    sys.stdout = redirect_stdout(output_text) 
    print(sorter.working_folder)
    
    sorter_thread = threading.Thread(target=sorter.path_check)
    sorter_thread.start()
    check_if_sorter_done()

def check_if_sorter_done():
    if sorter_thread.is_alive():
        root.after(200,check_if_sorter_done)
    else:
        show_buttons()
    

def show_buttons():
    processing_text.pack_forget()
    go_to_folder.pack(pady=7, padx=10, side="top", anchor= "nw")
    finish_button.pack(pady=7, padx=10, side="top", anchor= "nw")
    

def output_screen():
    global output_text, finish_button, go_to_folder, processing_text
    
    image_output_screen = Frame(root, bg="black")
    image_output_screen.place(relheight=1, relwidth=1)
    
    output_text = ScrolledText(image_output_screen, width= 700, height=20, fg="white", bg="black")
    output_text.pack(pady= (12,4), padx= 10, side="top", anchor="nw")
    
    processing_text = Label(image_output_screen,text="Processing...", font=(hell), fg="white", bg="black")
    processing_text.pack(pady=7, padx=10, side="top", anchor= "nw")
    
    go_to_folder = Button(image_output_screen, command=lambda:sorter.open_folder(),text= "Folder", font=(hell))  
    go_to_folder.config(fg="white", bg="black")
    
    finish_button = Button(image_output_screen, command=lambda:finished_pressed(), text= "Finish", font=(hell))
    finish_button.config(fg="white", bg="black")


def finished_pressed():
    start_main_screen()
 
    
start_main_screen()

root.mainloop()


