from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from sklearn.utils import shuffle
from tkinter import simpledialog
import time
import pyodbc
import pandas as pd
import webbrowser
#import pafy
import numpy as np
# Database credentials- To connect it to the Database for accessing the playlist, history and user table
conn = pyodbc.connect('Driver={SQL Server};''Server=LAPTOP-9R5IAN84;''Database=AjithDB;''Trusted_Connection=yes;')


"""
PLAY
1. Asks the user to choose his genre
2. Displays the videos present in that genre on the display frame
3. After user types the title of the video, it opens the video in a new tab in browser.
"""
def play_base():
    playframe = pd.read_sql_query('select * from playlist', conn)
    choice = simpledialog.askstring("Input", "What do u want to see? Sports/News/Music ", parent=epic)
    genre_frame = playframe.loc[(playframe.genre == choice)]
    return genre_frame


"""
REPEAT
1. When we click on repeat, it opens the last played video in a new tab in the browser.
"""
def repeat_base():
    #
    hist = pd.read_sql_query('select * from history', conn)
    playframe = pd.read_sql_query('select * from playlist', conn)

    current_id = (hist.iloc[hist.shape[0]-1]['id'])

    last_played_series = playframe.iloc[current_id - 1]
    webbrowser.open(last_played_series.link)
    messagebox.showinfo('history', "Repeating current song...")


"""
SKIP
1.When the user clicks Skip, it skips the current video and plays the next video in the browser
"""
def skip_base():

    import webbrowser
    hist = pd.read_sql_query('select * from history', conn)
    playframe = pd.read_sql_query('select * from playlist', conn)

    current_id = (hist.iloc[hist.shape[0]-1]['id'])
    nxt = ((current_id+1))
    if nxt > playframe.shape[0]:
        nxt = 1

    next_video_frame = playframe.loc[(playframe.id == nxt)]
    next_video_series = playframe.iloc[nxt - 1]
    webbrowser.open(next_video_series.link)
    cursor = conn.cursor()
    for index, row in next_video_frame.iterrows():
        cursor.execute("INSERT INTO history([id],[title],[link],[genre],[duration]) values(?,?,?,?,?)",
                       (row['id'], row['title'], row['link'], row['genre'], row['duration']))
        cursor.commit()
    messagebox.showinfo('history', "Skipping current song...")


"""
CHANGE
1. It prompts the user to enter his genre and video title.
2. Based on his selection, it plays the new video.
"""
def change_base():
    #
    playframe = pd.read_sql_query('select * from playlist', conn)
    choice = simpledialog.askstring("Input", "What do u want to see? Sports/News/Music ", parent=epic)
    genre_frame = playframe.loc[(playframe.genre == choice)]
    return genre_frame

"""
SHUFFLE
It shuffles the video list and lets the user to pick from the new shuffled list
"""
def shuffle_base():
    playlist = pd.read_sql_query('select * from playlist with (nolock)', conn)
    playlist = shuffle(playlist)
    play = playlist.title
    play = play.to_numpy().tolist()
    return play

"""
DURATION
It shows the duration of the currently playing song in the display frame.
"""
def duration_base():
    playing = pd.read_sql_query('select * from history', conn)
    playframe = pd.read_sql_query('select * from playlist', conn)
    current_id = (playing.iloc[playing.shape[0]-1]['id'])
    current_vid = playframe.loc[(playframe.id == current_id)]
    duration = current_vid.iloc[0]['duration']
    return duration

"""
DISPLAY HISTORY
It displays last 10 viewed videos on the display frame.
"""
def display_history():
    #
    history_list = pd.read_sql_query('select top 10 * from history with (nolock) order by history_id desc', conn)
    history = history_list.title
    hist = history.to_numpy().tolist()
    return hist

"""
ADD
1.It asks the user to enter the link of the Youtube video and its genre.
2. After he presses add, it gets added to the Playlist table in the database.
"""
def add_playlist():
    #
    def add():

        url = entry1.get()
        g = entry2.get()

        a = entry3.get()
        b = url
        c = g
        secs = entry4.get()

        #d = int(secs[0]) * 3600 + int(secs[1]) * 60 + int(secs[2])
        #d = round((d / 60), 2)
        d = float(secs)
        playframe = pd.read_sql_query('select * from playlist', conn)
        current_id = (playframe.iloc[playframe.shape[0]-1]['id'])
        current_id = int(current_id)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.playlist([title],[link],[genre],[duration],[id]) values(?,?,?,?,?)", (a, b, c, d,current_id+1))
        cursor.commit()
        cursor.close()
        sub_root.destroy()

    sub_root = Tk()
    sub_root.geometry('500x300')
    sub_root.title('Add Playlist')
    label3 = Label(sub_root, text='Title', font=customFont)
    label3.grid(row=0, sticky=EW, padx=(10, 20), pady=(5, 0))
    label1 = Label(sub_root, text='YouTube URL', font=customFont)
    label1.grid(row=1, sticky=EW, padx=(10, 20), pady=(5, 0))
    label2 = Label(sub_root, text='Genre', font=customFont)
    label2.grid(row=2, sticky=EW, padx=(10, 20), pady=(5, 0))
    label4 = Label(sub_root, text='Duration', font=customFont)
    label4.grid(row=3, sticky=EW, padx=(10, 20), pady=(5, 0))
    entry3 = Entry(sub_root, width=25, relief="solid")
    entry3.grid(row=0, column=1, pady=(5, 0))
    entry1 = Entry(sub_root, width=25, relief="solid")
    entry1.grid(row=1, column=1, pady=(5, 0))
    entry2 = Entry(sub_root, width=25, relief="solid")
    entry2.grid(row=2, column=1, pady=(5, 0))
    entry4 = Entry(sub_root, width=25, relief="solid")
    entry4.grid(row=3, column=1, pady=(5, 0))
    butt = Button(sub_root, text='Add', font=customFont, command=add)
    butt.grid(row=4, column=1, sticky=EW, padx=(5, 75), pady=(5, 5))
    butt1 = Button(sub_root, text='Cancel', font=customFont, command=sub_root.destroy)
    butt1.grid(row=4, column=1, sticky=E, padx=(0, 5), pady=(5, 5))
    sub_root.mainloop()


"""
DISPLAY PLAYLIST
1. It displays all the videos present in our playlist table in the database.
"""
def display_playlist():
    #
    playlist_list = pd.read_sql_query('select * from playlist with (nolock)', conn)
    play = playlist_list.title.to_numpy().tolist()
    return play


def main_board():
    #
    global epic
    query = 'select * from dbo.users where username = ?'

    q = pd.read_sql_query(query, conn, params=[ent1.get()])

    if q.empty:
        messagebox.showinfo("Error", 'Invalid Credentials')
    elif q.iloc[0, 1] == ent1.get() and q.iloc[0, 4] == ent2.get():

        def d_hist():
            x = display_history()
            t.delete(1.0, END)
            t.insert(END, '\n HISTORY \n')
            for i, j in enumerate(x):
                t.insert(END, str(i+1) + ' ' + j + '\n')

        def d_playlist():
            y = display_playlist()
            t.delete(1.0, END)
            t.insert(END, '\n PLAYLIST \n')
            for i, j in enumerate(y):
                t.insert(END, str(i+1) + ' ' + j + '\n')

        def d_shuffle():
            z = shuffle_base()
            t.delete(1.0, END)
            t.insert(END, '\n Shuffled List \n')
            for i, j in enumerate(z):
                t.insert(END, str(i + 1) + ' ' + j + '\n')

            playframe = pd.read_sql_query('select * from playlist', conn)
            video = simpledialog.askstring("Input", "What do you want to be played? ", parent=epic)
            idx = playframe.index[playframe['title'] == video]

            link = playframe.iloc[idx[0]]['link']
            webbrowser.open(link)
            last_played = playframe.loc[(playframe.title == video)]
            cursor = conn.cursor()
            for index, row in last_played.iterrows():
                cursor.execute("INSERT INTO history([id],[title],[link],[genre],[duration]) values(?,?,?,?,?)",
                               (row['id'], row['title'], row['link'], row['genre'], row['duration']))
                cursor.commit()

        def d_duration():
            a = duration_base()
            t.delete(1.0, END)
            a = np.array2string(a)
            t.insert(END, 'Duration of the current song is ' + str(a) + ' minutes' + '\n')

        def d_play():
            b = play_base()
            play = b.title
            play = play.to_numpy().tolist()
            t.delete(1.0, END)
            t.insert(END, '\n Playlist \n')
            for i, j in enumerate(play):
                t.insert(END, str(i + 1) + ' ' + j + '\n')

            playframe = pd.read_sql_query('select * from playlist', conn)
            video = simpledialog.askstring("Input", "What do you want to be played? ", parent=epic)
            idx = playframe.index[playframe['title'] == video]
            link = playframe.iloc[idx[0]]['link']
            webbrowser.open(link)

            last_played = playframe.loc[(playframe.title == video)]
            cursor = conn.cursor()
            for index, row in last_played.iterrows():
                cursor.execute("INSERT INTO history([id],[title],[link],[genre],[duration]) values(?,?,?,?,?)",
                               (row['id'], row['title'], row['link'], row['genre'], row['duration']))
                cursor.commit()

        def d_change():
            c = change_base()
            play = c.title
            play = play.to_numpy().tolist()
            t.delete(1.0, END)
            t.insert(END, '\n Playlist \n')
            for i, j in enumerate(play):
                t.insert(END, str(i + 1) + ' ' + j + '\n')

            playframe = pd.read_sql_query('select * from playlist', conn)
            video = simpledialog.askstring("Input", "What do you want to be played? ", parent=epic)
            idx = playframe.index[playframe['title'] == video]

            link = playframe.iloc[idx[0]]['link']
            webbrowser.open(link)

            last_played = playframe.loc[(playframe.title == video)]
            cursor = conn.cursor()
            for index, row in last_played.iterrows():
                cursor.execute("INSERT INTO history([id],[title],[link],[genre],[duration]) values(?,?,?,?,?)",
                               (row['id'], row['title'], row['link'], row['genre'], row['duration']))
                cursor.commit()

        epic = Toplevel()
        root.iconify()
        epic.title('Take a Break')
        epic.resizable(0, 0)
        customfont1 = tkFont.Font(family="Helvetica", size=10, weight='bold')
        bg_image1 = PhotoImage(file="D:\\Praxis\\Python\\projectfinal\\new_image.png")
        canvas1 = Canvas(epic, width=400, height=350, relief='raised')
        canvas1.pack()
        canvas1.create_image(0, 0, image=bg_image1, anchor='nw')
        btn1 = Button(epic, height=2, width=20, text="Play", font=customfont1, fg='black', command=d_play)
        canvas1.create_window(100, 35, window=btn1)
        btn2 = Button(epic, height=2, width=20, text="Skip", font=customfont1, fg='black', command=skip_base)
        canvas1.create_window(100, 105, window=btn2)
        btn3 = Button(epic, height=2, width=20, text="Shuffle", font=customfont1, fg='black', command=d_shuffle)
        canvas1.create_window(100, 175, window=btn3)
        btn4 = Button(epic, height=2, width=20, text="History", font=customfont1, fg='black', command=d_hist)
        canvas1.create_window(100, 245, window=btn4)
        btn5 = Button(epic, height=2, width=20, text="Quit", font=customfont1, fg='black', command=epic.destroy)
        canvas1.create_window(100, 315, window=btn5)
        btn6 = Button(epic, height=2, width=20, text="Repeat ", font=customfont1, fg='black', command=repeat_base)
        canvas1.create_window(300, 35, window=btn6)
        btn7 = Button(epic, height=2, width=20, text="Change", font=customfont1, fg='black', command=d_change)
        canvas1.create_window(300, 105, window=btn7)
        btn8 = Button(epic, height=2, width=20, text="Duration", font=customfont1, fg='black', command=d_duration)
        canvas1.create_window(300, 175, window=btn8)
        btn9 = Button(epic, height=2, width=20, text="Add", font=customfont1, fg='black', command=add_playlist)
        canvas1.create_window(300, 245, window=btn9)
        btnx = Button(epic, height=2, width=20, text="Playlist", font=customfont1, fg='black', command=d_playlist)
        canvas1.create_window(300, 315, window=btnx)
        s_bar = Frame(epic)
        s_bar.pack(side='bottom', fill='x', expand=False)
        status_bar1 = Label(epic, text=txt, bd=1, relief=SUNKEN, anchor=W)

        def tkt():
            if minutes < 15:
                status_bar1.config(text=txt)
            status_bar1.after(200, tkt)

        tkt()
        t = Text(epic, bd=2, bg="white", border='5', height="8", width="40", font=customfont1)
        scroll = Scrollbar(epic, orient="vertical", command=t.yview)
        t.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        t.pack(side="left", fill="both", expand=True)
        status_bar1.pack(in_=s_bar, side=LEFT, fill=BOTH, expand=True)
        epic.mainloop()
    else:
        messagebox.showinfo("Error", 'Invalid Credentials')


def create_new():
    # Creating new user for the Signup
    def signup():

        a = e3.get()
        b = e1.get()
        c = e2.get()
        d = e4.get()
        cursor = conn.cursor()
        if len(a) != 0 and len(b) != 0 and len(c) != 0 and len(d) != 0:
            q1 = "insert into dbo.users(username, fullname, email, password) values (?,?,?,?)"
            try:
                cursor.execute(q1, (a, b, c, d))
                conn.commit()

                if cursor.rowcount == 1:
                    messagebox.showinfo("Successful", 'New User Created')
                    new.destroy()
                else:
                    messagebox.showinfo("Failed", 'Action Failed')
                    new.destroy()
            except pyodbc.IntegrityError:
                messagebox.showinfo("Error", 'User Already Exist')
                new.destroy()
            finally:
                cursor.close()
        else:
            messagebox.showinfo("Error", 'One or more fields are empty')
            new.destroy()

    new = Tk()
    new.resizable(0, 0)
    new.title('Signup')

    Label(new, text='Full Name', width=15, font=customFont).grid(row=0, sticky=E)
    Label(new, text='E-mail ID', width=15, font=customFont).grid(row=1, sticky=E)
    Label(new, text='User ID', width=15, font=customFont).grid(row=2, sticky=E)
    Label(new, text='password', width=15, font=customFont).grid(row=3, sticky=E)
    e1 = Entry(new, name='full Name', width=20, relief="solid", font=customFont)
    e1.grid(row=0, column=1, padx=(10, 10))
    e2 = Entry(new, name='e-mail id', width=20, relief="solid", font=customFont)
    e2.grid(row=1, column=1, padx=(10, 10))
    e3 = Entry(new, name='user id', width=20, relief="solid", font=customFont)
    e3.grid(row=2, column=1, padx=(10, 10))
    e4 = Entry(new, name='password', show='*', width=20, relief="solid", font=customFont)
    e4.grid(row=3, column=1, padx=(10, 10))
    b1 = Button(new, text="Sign Up", command=signup, font=customFont)
    b1.grid(row=5, padx=(10, 0), pady=(2, 2), sticky=EW)
    b2 = Button(new, text='Cancel', command=new.destroy, font=customFont)
    b2.grid(row=5, column=1, padx=(30, 10), pady=(2, 2), sticky=EW)

    new.mainloop()


root = Tk()
root.resizable(0, 0)
customFont = tkFont.Font(family="Helvetica", size=12)
root.title('TAKE A BREAK')
bg_image = PhotoImage(file="D:\\Praxis\\Python\\projectfinal\\16291.png")
# get the width and height of the image
w = bg_image.width()
h = bg_image.height()
h = h + 30
# size the window so the image will fill it
root.geometry("%dx%d+0+0" % (w, h))
cv = Canvas(root, width=w, height=h)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0, 0, image=bg_image, anchor='nw')

blank = Label(cv, text='LOGIN REQUIRED', font=customFont, background="black", fg="white")
blank.pack(side='top', pady=60, fill='both')
lab1 = Label(cv, width=16, text='User Name', font=customFont, bg='white', anchor='center').place(x=90, y=370)
ent1 = Entry(cv, name='username', font=customFont, width=15, relief="solid")
ent1.place(x=230, y=370)

lab2 = Label(cv, width=16, text='Password', font=customFont, bg='white', anchor='center').place(x=90, y=400)
ent2 = Entry(cv, name='password', show='*', font=customFont, width=15, relief="solid")
ent2.place(x=230, y=400)
but1 = Button(cv, text='Login', width=10, relief="raised", font=customFont, bg="black", fg="white", command=main_board)
but1.pack(side='bottom', pady=40)
lab3 = Label(cv, text='Create New Account ?', bg='white', fg='blue', cursor='hand2')
lab3.place(x=190, y=470)
lab3.bind('<Button-1>', lambda e: create_new())
status_bar = Frame(root)
status_bar.pack(side='bottom', fill='x', expand=False)
minutes = 0
txt = ''
clock = Label(root, font=customFont, bg='white')
status = Label(root, font=customFont, bg='white', bd=2, relief=FLAT, anchor=W)


def tick():
    global txt
    time1 = time.perf_counter()
    time1 = convert(time1)
    txt = "Application will close in " + str(30-minutes) + " minutes"
    if minutes < 15:
        status.config(text=txt)
        clock.config(text=time1)
    else:
        # status.config(text="Application Closing in 5 seconds")
        # time.sleep(5)
        root.destroy()
    clock.after(200, tick)


def convert(seconds):
    global minutes
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hour, minutes, seconds)


tick()
status.pack(in_=status_bar, side=LEFT, fill=BOTH, expand=True)
clock.pack(in_=status_bar, side=RIGHT, fill=Y, expand=False)
root.mainloop()
