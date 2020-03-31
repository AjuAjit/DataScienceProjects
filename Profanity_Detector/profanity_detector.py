"""Profanity detector reads pdf and scans them for vulgar words.
It gives us a count of the occurences of these words."""

"""
1.tkinter is used to create GUI.
2.pdfplumber is used to read pdfs.
3.pandas are used to store our results.
4.datetime is used to generate a hashcode for unique file naming purpose
"""

"""
Procedure:
1.User is prompted to browse and select the book pdf.
2.He is then asked to specify the list of words separated by commas.
3.Words and their respective counts are stored in dictionary.
4.It checks for the count of these words in the dictionary.
5.Different forms of the given word are also checked. For eg, play -> plays, playing, played
6.User specified words and their counts are stored in a pandas dataframe.
7.Dataframe results are stored in an .csv file in the same location as our pdf file.
"""

from tkinter import *
from tkinter import filedialog, messagebox
import tkinter.font as tkFont
import pdfplumber
import pandas as pd
import datetime

global filename
global bad_words_list


def find_bad_words():
    global bad_words_list
    bad_words = mystring.get()
    bad_words_list = bad_words.split((','))
    profanity_detector()


def browsefunc():
    global filename
    filename = filedialog.askopenfilename()
    abbreviated_file_name = str(filename)
    abbreviated_file_name = abbreviated_file_name[0:20] + "..."
    pathlabel.config(text=abbreviated_file_name)


def profanity_detector():
    pdf = pdfplumber.open(filename)
    freq = {}
    bad_word_frame = pd.DataFrame()

    for i in range(0, len(pdf.pages)):

        page = pdf.pages[i]
        text = page.extract_text()
        texts = str(text)
        for piece in texts.lower().split():
            # only consider alphabetic characters within this piece
            word = ''.join(c for c in piece if c.isalpha())
            if word:  # require at least one alphabetic character
                freq[word] = 1 + freq.get(word, 0)

    for word in bad_words_list:
        for j in freq.keys():
            if j.__contains__(word):
                a_row = pd.Series([j, freq[j]])
                row_df = pd.DataFrame([a_row])
                bad_word_frame = pd.concat([row_df, bad_word_frame])
    bad_word_frame.columns = ['Word', 'Occurence_count']
    bad_word_frame.drop([0])

    sub_dirs = filename.split('/')
    path = filename[0:filename.find(sub_dirs[-1])]
    filename_without_ext = (sub_dirs[-1]).replace('.pdf', '')
    now = datetime.datetime.now()
    hash = (str(now))
    hash = hash[0:len(hash) - 7]
    special_chars = "- :"
    for char in special_chars:
        hash = hash.replace(char, "")
    final_path = (path) + filename_without_ext + hash + '.csv'
    final_path = final_path.replace('/', '\\')

    bad_word_frame.to_csv(final_path, index=False)
    pdf.close()
    messagebox.showinfo("Success", 'Processed successfully..Please check your generated sheet')


sub_root = Tk()
# creates the tkinter window

mystring = StringVar(sub_root, name="str")
customFont = tkFont.Font(family="Helvetica", size=10, weight='bold')  # initializes font

sub_root.geometry('500x300')  # setting the size of the window
sub_root.title('Profanity detector')  # setting title
label1 = Label(sub_root, text='Path of the book', font=customFont)
label1.grid(row=0, sticky=EW, padx=(10, 20), pady=(5, 0))

pathlabel = Label(sub_root, width=25)
pathlabel.grid(row=0, column=1, pady=(5, 0))

browse_button = Button(sub_root, text="Browse", font=customFont, command=browsefunc)
browse_button.grid(row=0, column=2, sticky=W, padx=(0, 0), pady=(5, 5))

word_label = Label(sub_root, text='Words to check', font=customFont)
word_label.grid(row=1, sticky=EW, padx=(10, 20), pady=(5, 0))

words_entry = Entry(sub_root, width=25, relief="solid", textvariable=mystring)
words_entry.grid(row=1, column=1, pady=(5, 0))

find_button = Button(sub_root, text='Find', font=customFont, command=find_bad_words)
find_button.grid(row=1, column=2, sticky=W, padx=(0, 0), pady=(5, 5))

sub_root.mainloop()
