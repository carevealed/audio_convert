import os

__author__ = 'California Audio Visual Preservation Project'
import sys


if sys.version_info >= (3, 0):
    from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilenames
    from tkinter.messagebox import showerror, askyesno, showinfo
    import configparser
    from tkinter import *
    from tkinter import ttk
else:
    from tkFileDialog import askdirectory, asksaveasfilename, askopenfilenames
    from tkMessageBox import showerror, askyesno, showinfo
    import ConfigParser as configparser
    from Tkinter import *
    import ttk

# settingsFile = 'settings.ini'
class SettingsWindow(object):
    def __init__(self, master, input_file):
        if not os.path.exists(input_file):
            raise IOError(input_file + " not found")
        self.master = master
        self.settingsFile = input_file
        # self.master.title("Settings")
        # self.master.grab_set()
        self.background = ttk.Frame(self.master, padding=(5,5))
        self.background.pack(fill=BOTH, expand=True)

        self.config = configparser.RawConfigParser()
        self.config.read([self.settingsFile])
        # for n in config:
        #     print(n)
        # print(config.get('EXTERNAL_PROGRAMS', 'LAME'))
        self.sections = []

        row = 0
        for section in self.config.sections():
            options = []
            label_section = ttk.Label(self.background, text=section)
            label_section.grid(row=row, column=0)
            row += 1
            for option in self.config.options(section):
                label_option = ttk.Label(self.background, text=option)
                line_option = ttk.Entry(self.background)
                line_option.insert(0, self.config.get(section, option))
                label_option.grid(row=row, column=0, sticky=W)
                line_option.grid(row=row, column=1)
                options.append((label_option, line_option))
                row += 1
            self.sections.append((section,options))
        self.ok_button = ttk.Button(self.background, text="OK", command=self.save)
        self.ok_button.grid(row=row, column=0)
        self.cancel_button = ttk.Button(self.background, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=row, column=1)

    def save(self):
        for section in self.sections:
            for option in section[1]:
                dataSec = section[0]
                dataOpt = option[0].cget("text")
                dataValue = option[1].get()
                self.config.set(dataSec,dataOpt,dataValue)
        with open(self.settingsFile, 'w', encoding='UTF-8') as configfile:
            self.config.write(configfile)
        self.master.destroy()
    # def on_closing(self):
    #     self.master.destory()

    def cancel(self):
        self.master.destroy()




def main():

    root = Tk()
    app = SettingsWindow(root)
    root.mainloop()
    pass


if __name__ == '__main__':
    main()