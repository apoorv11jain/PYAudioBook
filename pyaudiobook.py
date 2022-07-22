from tkinter import *
import PyPDF2
from tkinter import filedialog
import pyttsx3
import pygame

root = Tk()
root.title('ineuron-audio-books')
root.geometry("500x500")


def play_book():
    song = song_box.get(ACTIVE)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0)

def stop_book():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

global paused
paused =False
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def Text_to_speech(file_content, file_name):
    engine = pyttsx3.init()
    s = file_name.replace('.pdf', '.wav')
    engine.save_to_file(file_content,s)
    engine.runAndWait()
    song_box.insert(END,s)



def open_pdf():
    open_file = filedialog.askopenfilename(
        initialdir="E:\\Downloads\\",
        title = "Open PDF File",
        filetypes=([('PDF Files', '*.pdf')]))
    page_text =''

    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        num_page = pdf_file.numPages
        for i in range(num_page):
            page = pdf_file.getPage(i)
            page_text += page.extractText()
        file_name = open_file.split("/")[-1]
        file_name.replace(".pdf","")
        Text_to_speech(page_text,file_name)

#creation of a menu
my_menu = Menu(root)
root.config(menu=my_menu)

#adding drop downs
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label = 'File', menu= file_menu)
file_menu.add_command(label='Open', command=open_pdf)

file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)






pygame.mixer.init()

song_box = Listbox(root, bg="black", fg='white', width= 60)
song_box.pack(pady=20)



play_btn_img = PhotoImage(file='audio button images/play50.png')
pause_btn_img = PhotoImage(file='audio button images/pause50.png')
stop_btn_img = PhotoImage(file='audio button images/stop50.png')


control_frame =Frame(root)
control_frame.pack()



play_btn = Button(control_frame, image= play_btn_img, borderwidth= 0, command=play_book)
pause_btn = Button(control_frame, image= pause_btn_img, borderwidth= 0, command= lambda : pause(paused))
stop_btn= Button(control_frame, image= stop_btn_img, borderwidth= 0, command= stop_book)


play_btn.grid(row= 0, column=2, padx=10)
pause_btn.grid(row= 0, column=3, padx=10)
stop_btn.grid(row= 0, column=4, padx=10)








root.mainloop()