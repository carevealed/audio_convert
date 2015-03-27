from tkFileDialog import askopenfilename, askdirectory

__author__ = 'California Audio Visual Preservation Project'
__copyright__ = "California Audiovisual Preservation Project. 2015"
__credits__ = ["Henry Borchers"]
__version__ = '0.1.0'
__license__ = 'TBD'


from Tkinter import *
import ttk
# sys.path.insert(0, os.path.abspath('..'))
from source.audio_convert.scripts.modules.Audio_factory import *
IDLE = 0
WORKING = 1



class MainWindow(object):
    def __init__(self, master):
        self.master = master
        self.background = ttk.Frame(self.master, padding=(10,10))
        self.background.pack(fill=BOTH, expand=True)
        self.mp3_engine = AudioFactory(verbose=False)
        self.status = IDLE


        #---------------- Menus ----------------
        self.master.option_add('*tearOff', False)
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)
        self.fileMenu = Menu(self.menu_bar)
        self.helpMenu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.fileMenu, label="File")
        self.menu_bar.add_cascade(menu=self.helpMenu, label="Help")
        self.fileMenu.add_command(label="Quit", command=self.quit)
        self.helpMenu.add_command(label="About", command=self.load_about_window)

        #---------------- Title ----------------
        self.frame_title = ttk.Frame(self.background, padding=(20,10))
        self.frame_title.pack()
        self.title = ttk.Label(self.frame_title,
                               text="CAVPP Audio Converter",
                               font=('TkDefaultFont', 30, 'bold'))
        self.title.pack()

        #--------------------------------------------
        #-                Main Frame                -
        #--------------------------------------------

        self.frame_main = ttk.Frame(self.background, padding=(20,10))
        self.frame_main.pack(fill=BOTH, expand=True)
        self.label_queue = ttk.Label(self.frame_main, text="Queue")
        self.label_queue.pack(fill=BOTH, expand=True)

        #---------------- Queue frame ----------------

        self.frame_queue = ttk.Frame(self.frame_main, relief=SUNKEN)
        self.frame_queue.columnconfigure(0, weight=1)
        self.frame_queue.columnconfigure(1, weight=1)
        self.frame_queue.rowconfigure(0, weight=0)
        self.frame_queue.rowconfigure(1, weight=1)

        # self.frame_queue.columnconfigure(2, weight=1)
        self.frame_queue.pack(fill=BOTH, expand=True)
        self.frame_file_tree = ttk.Frame(self.frame_queue, padding=(10,10), relief=SUNKEN)
        self.frame_file_tree.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
        self.tree_files = ttk.Treeview(self.frame_file_tree, columns=('source', 'size', 'destination'))
        self.tree_files.heading('source', text='Source')
        self.tree_files.heading('size', text='Size')
        self.tree_files.heading('destination', text='Save As')
        self.tree_files['show'] = 'headings'
        self.tree_files.column('source', width=200)
        self.tree_files.column('size', width=100)
        self.tree_files.column('destination', width=200)
        self.tree_files.pack(fill=BOTH, expand=True)
        self.button_add_file = ttk.Button(self.frame_queue, text="Add File", command=self.add_file)
        self.button_add_file.grid(row=2, column=0, sticky=W+E)
        self.button_add_folder = ttk.Button(self.frame_queue, text="Add Folder", command=self.add_folder)
        self.button_add_folder.grid(row=2, column=1, sticky=W+E)



        #---------------- Progress frame ----------------

        self.frame_progress = ttk.Frame(self.frame_main, padding=(20,10))
        self.frame_progress.columnconfigure(0, weight=0)
        self.frame_progress.columnconfigure(1, weight=0)
        self.frame_progress.pack(fill=X, expand=True)
        # self.label_progress_title = ttk.Label(self.frame_progress, text="Progress")
        # self.label_progress_title.grid(row=0, column=0, sticky=E)
        # self.label_progress_working_file = ttk.Label(self.frame_progress, text="")
        # self.label_progress_working_file.grid(row=0, column=1, columnspan=2, sticky=E)
        self.label_progress_total = ttk.Label(self.frame_progress, text="Total:")
        self.label_progress_total.grid(row=1, column=0, sticky=E)
        self.pbar_progress_total = ttk.Progressbar(self.frame_progress, orient=HORIZONTAL, length=300, maximum=100, mode='determinate')
        self.pbar_progress_total.grid(row=1, column=2)

        self.label_progress_current = ttk.Label(self.frame_progress, text="Current:")
        self.label_progress_current.grid(row=2, column=0, sticky=E)
        self.pbar_progress_current = ttk.Progressbar(self.frame_progress, orient=HORIZONTAL, length=300, maximum=100, mode='determinate')
        self.pbar_progress_current.grid(row=2, column=2)

        self.button_start = ttk.Button(self.frame_main, text="Start", command=self.start_encoding)
        self.button_start.pack(fill=X, expand=True)

    # --------------------  status bar --------------------
        self.statusBar = Label(self.master, text="Status: Idle", bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)

    def set_status(self, new_status):
        self.statusBar.config(text="Status: " +new_status)

    def add_file(self):
        new_file = askopenfilename(filetypes=[("Wave", "*.wav")])
        if new_file:
            self.mp3_engine.add_audio_file(new_file)
        self.flush_tree()


    def add_folder(self):
        new_folder = askdirectory()
        if new_folder:
            # print "Adding folder: " + str(new_folder)
            for root, dir, files in os.walk(new_folder):
                for file in files:
                    if ".wav" in file:
                        # print "Adding \"" + path.join(root, file) + "\" to the queue."
                        self.mp3_engine.add_audio_file(os.path.join(root, file))
        self.flush_tree()

    def start_encoding(self):
        # print "Starting encoding"
        if self.status == IDLE:
            self.button_start.config(state=DISABLED)
            # self.working_thread = threading.Thread(target=self.mp3_engine.encode_next)
            working_thread = threading.Thread(target=self.mp3_engine.run)
            working_thread.daemon = True
            working_thread.start()
            # self.set_status("Working :"+ str(self.mp3_engine.status_percentage))
            self.status = WORKING

                # print "alive"

        # self.mp3_engine.encode_next()
        self.update_progress()

    def flush_tree(self):
        for i in self.tree_files.get_children():
            self.tree_files.delete(i)
        for item in self.mp3_engine.preview_queues():
            source = item[1]['source']
            destination = item[1]['destination']
            i = item[0] + 1
            self.tree_files.insert('', i, i)
            self.tree_files.set(i, 'source', source)
            self.tree_files.set(i, 'destination', destination)


    def load_about_window(self):
        aboutRoot = Toplevel(self.master)
        aboutRoot.wm_title("About")
        aboutRoot.resizable(FALSE,FALSE)
        about = AboutWindow(aboutRoot)

    def quit(self):
        quit()

    def update_progress_data(self, percentage, part, total):
        self.pbar_progress_total.config(maximum=total, value=part)
        self.pbar_progress_current.config(value=percentage)

    def update_progress(self):

        if self.mp3_engine.current_status == "Encoding":
            self.flush_tree()
            percent = self.mp3_engine.status_percentage
            part = self.mp3_engine.status_part
            total = self.mp3_engine.status_total
            # self.label_progress_working_file.config(text=self.mp3_engine.currentFile)
            self.update_progress_data(percent, part, total)
            self.set_status("Converting: " + self.mp3_engine.currentFile + ". " + str(percent) + "%")
            self.master.after(100, self.update_progress)
        else:
        # self.working_thread.join()
        #     print self.mp3_engine.current_status
            self.update_progress_data(self.mp3_engine.status_percentage,
                                      self.mp3_engine.status_part+1,
                                      self.mp3_engine.status_total)
            self.set_status("Idle")
            self.status = IDLE
            self.flush_tree()
            self.button_start.config(state=NORMAL)


class AboutWindow():
    def __init__(self, master):
        self.master = master
        self.master.resizable(width=None, height=None)
        self.background = ttk.Frame(self.master, width=20, padding=10)
        self.background.pack(fill=BOTH, expand=True)

# ----------------- Title
        self.titleFrame = ttk.Frame(self.background, width=20, padding=10, relief=RIDGE)
        self.titleFrame.pack()
        self.titleLabel = ttk.Label(self.titleFrame, text="CAVPP Audio Converter")
        self.titleLabel.pack()
        self.versionLabel = ttk.Label(self.titleFrame, text="Version: " + __version__)
        self.versionLabel.pack()

# ----------------- More info
        self.moreInfoframe = ttk.Labelframe(self.background, text="Info")
        self.moreInfoframe.pack(fill=BOTH, expand=True)

        self.copyrightTitleLabel = ttk.Label(self.moreInfoframe, text="Copyright:")
        self.copyrightTitleLabel.grid(column=0, row=0, sticky=W+N)
        self.copyrightDataLabel = ttk.Label(self.moreInfoframe, text=__copyright__)
        self.copyrightDataLabel.grid(column=1, row=0, sticky=W)

        self.LicenseTitleLabel = ttk.Label(self.moreInfoframe, text="License:")
        self.LicenseTitleLabel.grid(column=0, row=1, sticky=W+N)
        self.LicenseDataLabel = ttk.Label(self.moreInfoframe, text=__license__)
        self.LicenseDataLabel.grid(column=1, row=1, sticky=W)

        self.creditsTitleLabel = ttk.Label(self.moreInfoframe, text="Credits:")
        self.creditsTitleLabel.grid(column=0, row=2, sticky=W+N)
        names = ""
        for credit in __credits__:
            names = names + credit + "\n"
        self.creditsdataLabel = ttk.Label(self.moreInfoframe, text=names)
        self.creditsdataLabel.grid(column=1, row=2, sticky=W)

        self.closeButton = ttk.Button(self.background, text="Close", command=lambda: self.master.destroy())
        self.closeButton.pack()

# class communicator(threading.Thread):
#     def __init__(self):
def startup():
    root = Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    # main()
    pass