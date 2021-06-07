from tkinter import *
from tkinter import filedialog
import os
from selenium import webdriver
import requests


def changedir():
    folder.set(filedialog.askdirectory())
    if(len(folder.get()) != 0):
        curdir.config(text="Current directory : " + folder.get())
    else:
        curdir.config(text="Current directory : " + os.getcwd())


def download():
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe")
    driver.get(url.get())
    playbutton = driver.find_element_by_class_name("playbutton")
    playbutton.click()
    playbutton.click()
    r = requests.get(driver.find_element_by_tag_name(
        'audio').get_attribute("src"), allow_redirects=True)
    open(folder.get()+"\\" +
         driver.title[:driver.title.find('|')-1]+".mp3", 'wb').write(r.content)
    driver.close()
    url.delete(0, END)
    url.insert(0, "")


gui = Tk(className="Download music from Bandcamp")
gui.geometry("600x125")

folder = StringVar()

Label(gui, text="URL : ").place(x=5, y=20)
url = Entry(gui, width=85)
url.place(x=50, y=20)

curdir = Label(gui, text="Current directory : " + os.getcwd())
curdir.place(x=5, y=50)

dl = Button(gui, text="Download", width=10, height=1,
            command=download).place(x=250, y=75)
chdir = Button(gui, text="Change Directory", command=changedir,
               width=20, height=1).place(x=425, y=50)

gui.mainloop()
