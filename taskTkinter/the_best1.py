import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
import sys
from urllib.request import urlopen
import re



def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html'):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_filename + "'")

    # Return the downloaded document to the caller
    return web_page_contents

def restart():
    result = tk.messagebox.askokcancel("Download complete...", "The data was downloaded. Would you like to reload with new data?")
    if result:
        python = sys.executable
        os.execl(python, python, * sys.argv)

def exportPage(filePath):
    file = open(filePath, 'r')
    content = file.read()

    table = re.findall(r'<table(.*?)</table>', content, re.M | re.I | re.S)[0]
    header = re.findall(r'<\s*h1[^>]*>(.*?)<\s*/\s*h1>', content, re.M | re.I | re.S)[0]
    image = re.findall(r'<img([^>]*[^/])>', table, re.M | re.I | re.S)[0]
    date = re.findall(r'<option(.*?)</option>', content, re.M | re.I | re.S)[0]

    style = '<style>img { height: 50px; width: auto; }</style>'

    tb = '<table border="1" class="dataframe"' + table + '</table>'
    h1 = '<h1>' + header + '</h1>'
    dateSplit = date.split('>')
    resultDate = dateSplit[1].replace(" ", "-")

    # if filePath == filePath1 or filePath == filePath2:
    #     tableHtml = df[0].drop(["Image","Change"], axis=1).to_html(index=False)
    # else:
    #     tableHtml = df[0].drop(["Image"], axis=1).to_html(index=False)
    outputFilename = filePath.replace(".html", resultDate + ".html")

    html = """%s<div style="width: 80%%; margin: 0 auto;"> %s %s The data was sourced from: <a href=%s>%s</a></div> """ % (
    style, h1, tb, outputFilename.replace("Archive/", ""), outputFilename)
    f = open(outputFilename, 'w')
    f.write(html)
    f.close()
    webbrowser.open('file://' + os.path.realpath(outputFilename))


LARGE_FONT = ("Verdana", 12)

urlOne = "https://newzoo.com/insights/rankings/top-20-core-pc-games/"
#urlTwo = "http://top10songs.com/weekly/2018.html"
urlTwo = "https://newzoo.com/insights/rankings/top-25-companies-game-revenues/"
urlThree = "https://newzoo.com/insights/rankings/top-100-countries-by-game-revenues/" ## PLACEHOLDER

targetFolder = "Archive/"
target_filename1 = targetFolder + "List1"
target_filename2 = targetFolder + "List2"
target_filename3 = targetFolder + "List3"

filePath1 = target_filename1 + ".html"
filePath2 = target_filename2 + ".html"
filePath3 = target_filename3 + ".html"



class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.geometry('500x300+800+400')
        self.resizable(width=False, height=False)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        self.regenerate(container)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def regenerate(self, container):
        for F in (StartPage, PageListOneCurrent, PageListOnePrevious, PageListTwoCurrent, PageListTwoPrevious, PageListThreeCurrent, PageListThreePrevious):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        leftFrame = tk.Frame(self, bg='white')
        rightFrame = tk.Frame(self, bg='white')

        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.RIGHT)

        def buttonRefresh():
            if os.path.isfile(filePath1):
                gamesPreviousButton['state'] = 'normal'
                gamesExportButton['state'] = 'normal'
            if os.path.isfile(filePath2):
                musicPrevButton['state'] = 'normal'
                musicExportButton['state'] = 'normal'
            if os.path.isfile(filePath3):
                countryPrevButton['state'] = 'normal'
                countryExportButton['state'] = 'normal'



        gamesLabelFrame = tk.LabelFrame(rightFrame, text="Games top 10", bg='white')
        musicLabelFrame = tk.LabelFrame(rightFrame, text="Game companies top 10", bg='white')
        countryLabelFrame = tk.LabelFrame(rightFrame, text="Gaming countries top 10", bg='white')


        # photo
        self.image = tk.PhotoImage(file='star.gif')
        self.game = tk.Label(leftFrame, image=self.image)
        self.game.config(borderwidth=0, highlightthickness=0)
        self.game.pack(padx=15, pady=30)

        gamesLabelFrame.pack(side=tk.TOP, padx=0, pady=0)
        musicLabelFrame.pack(side=tk.TOP, padx=10, pady=10)
        countryLabelFrame.pack(side=tk.TOP, padx=10, pady=10)

        # Buttons for Frame 1
        tk.Button(gamesLabelFrame, text=" Current", bg='white', fg='green', command=lambda: controller.show_frame(PageListOneCurrent)).grid(row=0, column=0)
        gamesPreviousButton = tk.Button(gamesLabelFrame, text=" Previous", bg='white', fg='red', state='disabled', command=lambda: controller.show_frame(PageListOnePrevious))
        gamesPreviousButton.grid(row=0, column=1, padx=3, pady=3)
        tk.Button(gamesLabelFrame, text=" Download", bg='white', command=lambda:[download(url=urlOne,
                 target_filename=target_filename1,
                 filename_extension="html"), restart()]).grid(row=1, column=0, padx=3, pady=3)

        gamesExportButton = tk.Button(gamesLabelFrame, text=" Export", bg='white', state='disabled', command=lambda: exportPage(filePath1))
        gamesExportButton.grid(row=1, column=1, padx=3, pady=3)

        # Buttons for Frame 2

        tk.Button(musicLabelFrame, text=" Current", bg='white', fg='green', command=lambda: controller.show_frame(PageListTwoCurrent)).grid(row=0, column=0)
        musicPrevButton = tk.Button(musicLabelFrame, text=" Previous", bg='white', fg='red', state='disabled' , command=lambda: controller.show_frame(PageListTwoPrevious))
        musicPrevButton.grid(row=0, column=1, padx=3, pady=3)

        tk.Button(musicLabelFrame, text=" Download", bg='white', command=lambda: [download(url=urlTwo,
                 target_filename=target_filename2,
                 filename_extension="html"), restart()]).grid(row=1, column=0, padx=3, pady=3)

        musicExportButton = tk.Button(musicLabelFrame, text=" Export", bg='white', state='disabled', command=lambda: exportPage(filePath2))
        musicExportButton.grid(row=1, column=1, padx=3, pady=3)

        # Buttons for Frame 3

        tk.Button(countryLabelFrame, text=" Current", bg='white', fg='green', command=lambda: controller.show_frame(PageListThreeCurrent)).grid(row=0, column=0)
        countryPrevButton = tk.Button(countryLabelFrame, text=" Previous", bg='white', fg='red', state='disabled' , command=lambda: controller.show_frame(PageListThreePrevious))
        countryPrevButton.grid(row=0, column=1, padx=3, pady=3)

        tk.Button(countryLabelFrame, text=" Download", bg='white', command=lambda: [download(url=urlThree,
                 target_filename=target_filename3,
                 filename_extension="html"), restart()]).grid(row=1, column=0, padx=3, pady=3)

        countryExportButton = tk.Button(countryLabelFrame, text=" Export", bg='white', state='disabled', command=lambda: exportPage(filePath3))
        countryExportButton.grid(row=1, column=1, padx=3, pady=3)

        buttonRefresh()


class PageListOneCurrent(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        #Frames
        leftFrame = tk.Frame(self, bg='white')
        rightFrame = tk.Frame(self, bg='white')
        topFrame = tk.Frame(self, bg='white')

        res = urlopen(urlOne).read().decode('utf-8')


        tableTest = re.findall(r'<table(.*?)</table>', res, re.M | re.I | re.S)[0]
        tdTest = re.findall(r'<td(.*?)</td>', tableTest, re.M | re.I | re.S)

        list = []
        for index, item in enumerate(tdTest):
            x = item.replace("\t", "")
            x1 = x.replace("\n", "")
            x2 = x1.replace(">", "")

            if x2.isdigit():
                itemToAdd = tdTest[index + 1]
                removeTab = itemToAdd.replace("\t", "")
                removeNewL = removeTab.replace("\n", "")
                cleanedItem = removeNewL.replace(">", "")
                list.append(cleanedItem)

        topFrame.pack(side=tk.TOP)
        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.RIGHT)

        #Main Label
        label = tk.Label(topFrame, text="Current Top Games", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        # photo
        self.image = tk.PhotoImage(file='game.gif')
        self.game = tk.Label(leftFrame, image=self.image)
        self.game.config(borderwidth=0, highlightthickness=0)
        self.game.pack(padx=25, pady=8)
        # frames with photo and list of items
        listBox = tk.Listbox(rightFrame, borderwidth=0, highlightthickness=0, width=35)
        listBox.configure(bg='white')
        for index, item in enumerate(list):
            listBox.insert(index, str(index+1) + ". " + item)
            index += 1


        listBox.pack(side=tk.TOP, padx=6, pady=8)

        button1 = tk.Button(rightFrame, text="Home",
                            command=lambda: controller.show_frame(StartPage), padx=6, pady=4)

        button1.pack(side=tk.LEFT)




class PageListOnePrevious(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='white')
        # Frames
        leftFrame = tk.Frame(self, bg='white')
        rightFrame = tk.Frame(self, bg='white')
        topFrame = tk.Frame(self, bg='white')

        topFrame.pack(side=tk.TOP)
        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.RIGHT)

        if os.path.isfile(filePath1):
            file = open(filePath1, 'r')
            content = file.read()

            tableTest = re.findall(r'<table(.*?)</table>', content, re.M | re.I | re.S)[0]
            tdTest = re.findall(r'<td(.*?)</td>', tableTest, re.M | re.I | re.S)

            list = []
            for index, item in enumerate(tdTest):
                x = item.replace("\t", "")
                x1 = x.replace("\n", "")
                x2 = x1.replace(">", "")

                if x2.isdigit():
                    itemToAdd = tdTest[index + 1]
                    removeTab = itemToAdd.replace("\t", "")
                    removeNewL = removeTab.replace("\n", "")
                    cleanedItem = removeNewL.replace(">", "")
                    list.append(cleanedItem)

            # Main Label
            label = tk.Label(topFrame, text="Previous Top Games", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            # photo
            self.image = tk.PhotoImage(file='game.gif')
            self.game = tk.Label(leftFrame, image=self.image)
            self.game.config(borderwidth=0, highlightthickness=0)
            self.game.pack(padx=15, pady=8)
            # frames with photo and list of items

            listBox = tk.Listbox(rightFrame, borderwidth=0, highlightthickness=0, width=40)
            listBox.configure(bg='white')
            for index, item in enumerate(list):
                listBox.insert(index, str(index+1) + ". " + item)
                index += 1

            listBox.pack(side=tk.TOP, padx=6, pady=8)

        button1 = tk.Button(rightFrame, text="Home",
                            command=lambda: controller.show_frame(StartPage), padx=6, pady=4)

        button1.pack(side=tk.LEFT)

class PageListTwoCurrent(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        # Frames
        leftFrame = tk.Frame(self, bg='white')
        rightFrame = tk.Frame(self, bg='white')
        topFrame = tk.Frame(self, bg='white')

        topFrame.pack(side=tk.TOP)
        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.RIGHT)

        res2 = urlopen(urlTwo).read().decode('utf-8')

        tableTest = re.findall(r'<table(.*?)</table>', res2, re.M | re.I | re.S)[0]
        tdTest = re.findall(r'<td(.*?)</td>', tableTest, re.M | re.I | re.S)

        list = []
        for index, item in enumerate(tdTest):
            x = item.replace("\t", "")
            x1 = x.replace("\n", "")
            x2 = x1.replace(">", "")

            if len(x2) == 1:
                itemToAdd = tdTest[index + 1]
                removeTab = itemToAdd.replace("\t", "")
                removeNewL = removeTab.replace("\n", "")
                cleanedLg = removeNewL.replace(">", "")
                cleanedItem = cleanedLg.replace("*", "")
                list.append(cleanedItem)


        # Main Label
        label = tk.Label(topFrame, text="Current Top Game Companies", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        # photo
        self.image = tk.PhotoImage(file='company.gif')
        self.game = tk.Label(leftFrame, image=self.image)
        self.game.config(borderwidth=0, highlightthickness=0)
        self.game.pack(padx=40, pady=10)
        # frames with photo and list of items
        listBox = tk.Listbox(rightFrame, borderwidth=0, highlightthickness=0, width=30)
        listBox.configure(bg='white')
        for index, item in enumerate(list):
            listBox.insert(index, str(index+1) + ". " + item)
            index += 1

        listBox.pack(side=tk.TOP, padx=6, pady=8)

        button1 = tk.Button(rightFrame, text="Home",
                            command=lambda: controller.show_frame(StartPage), padx=6, pady=4)
        button1.pack(side=tk.LEFT)

class PageListTwoPrevious(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='white')
        # Frames
        leftFrame = tk.Frame(self, bg='white')
        rightFrame = tk.Frame(self, bg='white')
        topFrame = tk.Frame(self, bg='white')

        topFrame.pack(side=tk.TOP)
        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.RIGHT)

        if os.path.isfile(filePath2):
            file = open(filePath2, 'r')
            content = file.read()

            tableTest = re.findall(r'<table(.*?)</table>', content, re.M | re.I | re.S)[0]
            tdTest = re.findall(r'<td(.*?)</td>', tableTest, re.M | re.I | re.S)

            list = []
            for index, item in enumerate(tdTest):
                x = item.replace("\t", "")
                x1 = x.replace("\n", "")
                x2 = x1.replace(">", "")
                if len(x2) == 1:
                    itemToAdd = tdTest[index + 1]
                    removeTab = itemToAdd.replace("\t", "")
                    removeNewL = removeTab.replace("\n", "")
                    cleanedLg = removeNewL.replace(">", "")
                    cleanedItem = cleanedLg.replace("*", "")
                    list.append(cleanedItem)

            # Main Label
            label = tk.Label(topFrame, text="Previous Top Songs", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            # photo
            self.image = tk.PhotoImage(file='company.gif')
            self.game = tk.Label(leftFrame, image=self.image)
            self.game.config(borderwidth=0, highlightthickness=0)
            self.game.pack(padx=40, pady=8)
            # frames with photo and list of items

            listBox = tk.Listbox(rightFrame, borderwidth=0, highlightthickness=0, width=30)
            listBox.configure(bg='white')
            for index, item in enumerate(list):
                listBox.insert(index, str(index+1) + ". " + item)
                index += 1
            listBox.pack(side=tk.TOP, padx=6, pady=8)

        button1 = tk.Button(rightFrame, text="Home",
                            command=lambda: controller.show_frame(StartPage), padx=6, pady=4)
        button1.pack(side=tk.LEFT)


class PageListThreeCurrent(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='white')
        # Frames
        leftFrame = tk.Frame(self, bg='white')
        rightFrame = tk.Frame(self, bg='white')
        topFrame = tk.Frame(self, bg='white')

        res = urlopen(urlThree).read().decode('utf-8')

        tableTest = re.findall(r'<table(.*?)</table>', res, re.M | re.I | re.S)[0]
        tdTest = re.findall(r'<td(.*?)</td>', tableTest, re.M | re.I | re.S)

        list = []
        for index, item in enumerate(tdTest):
            x = item.replace("\t", "")
            x1 = x.replace("\n", "")
            x2 = x1.replace(">", "")

            if x2.isdigit():
                itemToAdd = tdTest[index + 1]
                removeTab = itemToAdd.replace("\t", "")
                removeNewL = removeTab.replace("\n", "")
                cleanedItem = removeNewL.replace(">", "")
                list.append(cleanedItem)

        topFrame.pack(side=tk.TOP)
        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.RIGHT)

        #Main Label
        label = tk.Label(topFrame, text="Current Top Gaming Countries", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        # photo
        self.image = tk.PhotoImage(file='earth.gif')
        self.game = tk.Label(leftFrame, image=self.image)
        self.game.config(borderwidth=0, highlightthickness=0)
        self.game.pack(padx=20, pady=26)
        # frames with photo and list of items

        listBox = tk.Listbox(rightFrame, borderwidth=0, highlightthickness=0, width=35)
        listBox.configure(bg='white')
        for index, item in enumerate(list):
            listBox.insert(index, str(index+1) + ". " + item)
            index += 1


        listBox.pack(side=tk.TOP, padx=6, pady=8)

        button1 = tk.Button(rightFrame, text="Home",
                            command=lambda: controller.show_frame(StartPage), padx=6, pady=4)

        button1.pack(side=tk.LEFT)


class PageListThreePrevious(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='white')
        # Frames
        leftFrame = tk.Frame(self, bg='white')
        rightFrame = tk.Frame(self, bg='white')
        topFrame = tk.Frame(self, bg='white')

        topFrame.pack(side=tk.TOP)
        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.RIGHT)

        if os.path.isfile(filePath3):
            file = open(filePath3, 'r')
            content = file.read()

            tableTest = re.findall(r'<table(.*?)</table>', content, re.M | re.I | re.S)[0]
            tdTest = re.findall(r'<td(.*?)</td>', tableTest, re.M | re.I | re.S)

            list = []
            for index, item in enumerate(tdTest):
                x = item.replace("\t", "")
                x1 = x.replace("\n", "")
                x2 = x1.replace(">", "")

                if x2.isdigit():
                    itemToAdd = tdTest[index + 1]
                    removeTab = itemToAdd.replace("\t", "")
                    removeNewL = removeTab.replace("\n", "")
                    cleanedItem = removeNewL.replace(">", "")
                    list.append(cleanedItem)

            # Main Label
            label = tk.Label(topFrame, text="Previous Top Gaming Countries", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            # photo
            self.image = tk.PhotoImage(file='earth.gif')
            self.game = tk.Label(leftFrame, image=self.image)
            self.game.config(borderwidth=0, highlightthickness=0)
            self.game.pack(padx=20, pady=26)
            # frames with photo and list of items

            listBox = tk.Listbox(rightFrame, borderwidth=0, highlightthickness=0, width=40)
            listBox.configure(bg='white')
            for index, item in enumerate(list):
                listBox.insert(index, str(index+1) + ". " + item)
                index += 1

            listBox.pack(side=tk.TOP, padx=6, pady=8)

        button1 = tk.Button(rightFrame, text="Home",
                            command=lambda: controller.show_frame(StartPage), padx=6, pady=4)

        button1.pack(side=tk.LEFT)

app = SeaofBTCapp()
app.title("Simply The Best ... Previous and Current")
app.mainloop()