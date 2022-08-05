from tkinter import *
import PyPDF2
from tkinter import filedialog,messagebox
import pyttsx3
import pygame
import pymongo
import gridfs
import logging
import os

logging.basicConfig(filename="audiobook.log", level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
root = Tk()
root.title('ineuron-audio-books')
root.geometry("500x500")

location = "E:\\ineuron\\pyaudiobook\\media\\"

def delete_audio():
    '''
    This Function is used to delete the Audiobook present in the media folder
    This function does not require any argument to be passed during the call
    It delete the Active or selected audiobook when called
    It does not return anything
    :return: NONE
    '''
    try:
        file_to_delete = book_box.get(ACTIVE)
        book_box.delete(ACTIVE)
        os.remove(location+file_to_delete)
        logging.info(f"{file_to_delete} have been removed")

    except WindowsError:
        messagebox.showinfo(title= "CANNOT DELETE THE FILE" ,message="The File cannot be deleted because it is currently is being used try restarting the app")

    except Exception as e:
        logging.error(e)


def load_database():
    '''
    This function is Used to Load the audiobook stored in the MongoDB
    This function does not require any argument to be passed during the call
    It download all the files that are not prensent in the Media Folder when called
    It does not return anything
    :return: NONE
    '''
    try:
        list_of_files_present_in_media = os.listdir(location)
        db=mongo_conn()
        for i in db.fs.files.find():
            if i['filename']  not in list_of_files_present_in_media:
                data = i
                my_id = data['_id']
                fs = gridfs.GridFS(db)
                outputdata = fs.get(my_id).read()
                download_location = location +i['filename']
                output = open(download_location, "wb")
                output.write(outputdata)
                output.close()
                logging.info(f"the file is not found so {i} downloaded from the mongoDB")
        load_audio()
    except Exception as e:
        logging.error(e)

def load_audio():
    '''
    This function is Used to Load the audiobook stored in the Media Folder
    This function does not require any argument to be passed during the call
    It does not return anything
    :return: NONE
    '''
    try:
        list_of_files_present_in_media = os.listdir(location)
        list_of_files_Displaying = book_box.get(0,END)
        for i in list_of_files_present_in_media:
            if ".wav" in i and i not in list_of_files_Displaying:
                book_box.insert(END,i)
    except Exception as e:
        logging.error(e)

def mongo_conn():
    '''
    This Function is used to connect the Program to MONGODB
    Its only functionality is to create a connection with MONGODB
    It returns the database from the MongoDB in which the audiobooks are stored
    :return:<class 'pymongo.database.Database'>
    '''
    try:
        conn = pymongo.MongoClient( 'mongodb://localhost:27017')
        logging.info("MongoDB is connected")
        return conn['pyaudio']
    except Exception as e:
        logging.error(e)

def save_audio(audio_file):
    '''
    This Function is Used to save the Audiobook
    The Audiobooks are stored in the MONGODB
    It takes the help of GRIDFS to store the audio file
    :param audio_file: <class 'str'> Name and Location of the File
    :return: NONE
    '''
    try:
        db = mongo_conn()
        file_data = open(audio_file, "rb")
        data = file_data.read()
        fs = gridfs.GridFS(db)
        fs.put(data, filename = audio_file)
        logging.info("data saved in the data base")
    except Exception as e:
        logging.error(e)

def play_book():
    '''
    This function is Used to provide functionality to the Play button
    This is done with the help of pygame module
    :return: NONE
    '''
    try:
        os.chdir(location)
        book = book_box.get(ACTIVE)
        pygame.mixer.music.load(book)
        pygame.mixer.music.play(loops = 0)
        logging.info(f"the Play function is used and {book} is played")


    except Exception as e:
        logging.error(e)
def stop_book():
    '''
    This function is Used to provide functionality to the STOP button
    This is done with the help of pygame module
    :return: NONE
    '''
    try:
        pygame.mixer.music.stop()
        book_box.selection_clear(ACTIVE)
        logging.info(f"the Stop is called")
    except EXCEPTION as e:
        logging.error(e)

global paused
paused =False

def pause(is_paused):
    '''
    This function is Used to provide functionality to the STOP button
    This is done with the help of pygame module
    :param is_paused: <class 'bool'>
    :return: NONE
    '''
    global paused
    paused = is_paused
    try:
        if paused:
            pygame.mixer.music.unpause()
            paused = False
            logging.info("The audio is paused")
        else:
            pygame.mixer.music.pause()
            paused = True
            logging.info("The audio is continued")
    except Exception as e:
        logging.error(e)

def Text_to_speech(file_content, open_file):
    '''
    This Function is used to convert the PDF file to an audio File
    The Pyttsx3 module is used to convert text to speech
    the converted speech is then saved in media folder
    :param file_content: <class 'str'> text present in the File
    :param open_file:<class 'str'> file name with location
    :return: NONE
    '''
    try:
        engine = pyttsx3.init()
        file_name = open_file.split("/")[-1]
        book_name = file_name.replace('.pdf', '.wav')
        logging.info("the pdf is converted")
        os.chdir(location)
        engine.save_to_file(file_content,book_name)
        engine.runAndWait()
        logging.info("the audiobook is saved")
        book_box.insert(END,book_name)
        save_audio(book_name)
    except Exception as e:
        logging.error(e)

def open_pdf():
    '''
    This function is used to open and extract the text from the PDF file
    The PYPDF2 module is used in this function
    :return: NONE
    '''
    try:
        open_file = filedialog.askopenfilename(
            initialdir="E:\\Downloads\\",
            title = "Open PDF File",
            filetypes=([('PDF Files', '*.pdf')]))
        page_text =''
        list_of_book_display = book_box.get(0, END)
        if open_file:
            n = open_file.split("/")[-1].replace(".pdf", '.wav')
            if n not in list_of_book_display:
                pdf_file = PyPDF2.PdfFileReader(open_file)
                num_page = pdf_file.numPages
                for i in range(num_page):
                    page = pdf_file.getPage(i)
                    page_text += page.extractText()
                logging.info(f"The PDF is opened {open_file}")
                Text_to_speech(page_text,open_file)

    except Exception as e:
        logging.error(e)
try:
    # creation of a menu
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # adding drop downs
    file_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Open', command=open_pdf)

    file_menu.add_separator()
    file_menu.add_command(label='Delete', command=delete_audio)

    file_menu.add_separator()
    file_menu.add_command(label='Load From DB', command=load_database)

    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=root.quit)

    pygame.mixer.init()

    book_box = Listbox(root, bg="black", fg='white', width=60)
    book_box.pack(pady=20)



    play_btn_img = PhotoImage(file='audio button images/play50.png')
    pause_btn_img = PhotoImage(file='audio button images/pause50.png')
    stop_btn_img = PhotoImage(file='audio button images/stop50.png')

    control_frame = Frame(root)
    control_frame.pack()
    load_audio()
    play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_book)
    pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
    stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop_book)

    play_btn.grid(row=0, column=2, padx=10)
    pause_btn.grid(row=0, column=3, padx=10)
    stop_btn.grid(row=0, column=4, padx=10)
    logging.info("The application is created")

    root.mainloop()
except Exception as e:
    logging.error(e)