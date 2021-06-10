from tkinter import *
from tkinter import filedialog
import os
from selenium import webdriver
import requests
from collections import OrderedDict


def changedir():
    folder.set(filedialog.askdirectory())
    if(len(folder.get()) != 0):
        curdir.config(text="Current directory : " + folder.get())
    else:
        curdir.config(text="Current directory : " + os.getcwd())


def download(link):
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe")
    driver.get(link)
    playbutton = driver.find_element_by_class_name("playbutton")
    playbutton.click()
    playbutton.click()
    r = requests.get(driver.find_element_by_tag_name(
        'audio').get_attribute("src"), allow_redirects=True)
    open(folder.get()+"\\" +
         driver.title[:driver.title.find('|')-1]+".mp3", 'wb').write(r.content)
    driver.close()
    songurl.delete(0, END)
    songurl.insert(0, "")


def down():
    if(download_mode.get()):
        download(songurl.get())
    else:
        driver = webdriver.Chrome(
            executable_path="chromedriver.exe")
        driver.get(albumurl.get())
        els = driver.find_elements_by_xpath('//tr/td/div/a')
        temp = []
        for l in els:
            if(l.get_attribute('href').find('?action=download') == -1 and l.get_attribute('href').find('#lyrics') == -1):
                temp.append(l.get_attribute('href'))
        links = list(OrderedDict.fromkeys(temp))
        driver.close()
        for l in links:
            download(l)
    albumurl.delete(0, END)
    albumurl.insert(0, "")


def song_mode():
    songurl.config(state='normal')
    albumurl.config(state='disabled')


def album_mode():
    songurl.config(state='disabled')
    albumurl.config(state='normal')


gui = Tk(className="Download music from Bandcamp")
gui.geometry("600x150")

folder = StringVar()
download_mode = BooleanVar()

onlysong = Radiobutton(gui, text="Song URL : ",
                       variable=download_mode, value=True, command=song_mode)
onlysong.place(x=5, y=20)
songurl = Entry(gui, width=80)
songurl.place(x=100, y=20)

fullalbum = Radiobutton(gui, text="Album URL : ",
                        variable=download_mode, value=False, command=album_mode)
fullalbum.place(x=5, y=50)
albumurl = Entry(gui, width=80)
albumurl.place(x=100, y=50)

curdir = Label(gui, text="Current directory : " + os.getcwd())
curdir.place(x=5, y=80)

dl = Button(gui, text="Download", width=10, height=1,
            command=down).place(x=250, y=100)
chdir = Button(gui, text="Change Directory", command=changedir,
               width=20, height=1).place(x=425, y=75)

gui.mainloop()
