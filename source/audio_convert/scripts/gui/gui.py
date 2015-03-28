from tkFileDialog import askopenfilename, askdirectory, asksaveasfile, asksaveasfilename
from tkMessageBox import showerror, askyesno

__author__ = 'California Audio Visual Preservation Project'
__copyright__ = "California Audiovisual Preservation Project. 2015"
__credits__ = ["Henry Borchers"]
__version__ = '0.1.0'
__license__ = 'TBD'
DEBUG = True

from Tkinter import *
import ttk
# sys.path.insert(0, os.path.abspath('..'))
from modules.Audio_factory import AudioFactory
import threading
import os
IDLE = 0
WORKING = 1
SEARCHING = 2
HALTING = 3



class MainWindow(object):
    # tree_lock = threading.Lock()
    def __init__(self, master, input_file=None):
        self.master = master
        self.background = ttk.Frame(self.master, padding=(1,1))
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
        self.frame_title = ttk.Frame(self.background, padding=(10,5))
        self.frame_title.pack()
        self.title = ttk.Label(self.frame_title,
                               text="CAVPP Audio Converter",
                               font=('TkDefaultFont', 30, 'bold'))
        self.title.pack()

        #--------------------------------------------
        #-                Main Frame                -
        #--------------------------------------------

        self.frame_main = ttk.Frame(self.background, padding=(10,5))
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
        self.frame_queue.pack_propagate(0)
        self.frame_file_tree = ttk.Frame(self.frame_queue, padding=(5,5), relief=SUNKEN)
        self.frame_file_tree.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
        self.tree_files = ttk.Treeview(self.frame_file_tree, columns=('status', 'source', 'size', 'destination'))
        self.tree_files.heading('status', text='Status')
        self.tree_files.heading('source', text='Source')
        self.tree_files.heading('size', text='Size')
        self.tree_files.heading('destination', text='Save As')
        self.tree_files['show'] = 'headings'
        self.tree_files.column('status', width=75)
        self.tree_files.column('source', width=200)
        self.tree_files.column('size', width=100)
        self.tree_files.column('destination', width=200)
        self.tree_files.pack(fill=BOTH, expand=True)
        self.tree_files.pack_propagate(0)
        self.tree_files.bind("<Button-3>", self._popup)

        self.yscroll_files = Scrollbar(self.tree_files,orient=VERTICAL, command=self.tree_files.yview)
        self.yscroll_files.pack(side=RIGHT, fill=Y)
        self.xscroll_files = Scrollbar(self.tree_files, orient=HORIZONTAL, command=self.tree_files.xview)
        self.xscroll_files.pack(side=BOTTOM, fill=X)
        self.tree_files.configure(yscroll=self.yscroll_files.set, xscroll=self.xscroll_files.set)



        # self.button_add_file = ttk.Button(self.frame_queue, text="Add File", command=self.add_file)
        self.button_add_file = ttk.Button(self.frame_file_tree, text="Add File", command=self.add_file)
        # self.button_add_file.grid(row=2, column=0, sticky=W+E)
        # self.button_add_file.grid(row=2, column=0, sticky=W+E)
        self.button_add_file.pack(side=LEFT, fill=X, expand=True)

        self.button_add_folder = ttk.Button(self.frame_file_tree, text="Add Folder", command=self.add_folder)
        self.button_add_folder.pack(side=LEFT, fill=X, expand=True)
        # self.button_add_folder = ttk.Button(self.frame_queue, text="Add Folder", command=self.add_folder)
        # self.button_add_folder.grid(row=2, column=1, sticky=W+E)



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

        self.button_stop = ttk.Button(self.frame_main, text="Stop", command=self.abort, state=DISABLED)
        self.button_stop.pack(fill=X, expand=True)
    # --------------------  show queues --------------------
        if DEBUG:
            self.button_test = ttk.Button(self.frame_main, text="test", command=self.test)
            self.button_test.pack()

    # --------------------  status bar --------------------
        self.statusBar = Label(self.master, text="Status: Idle", bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)


        self.propertyMenu = Menu(self.master, tearoff=0)
        self.propertyMenu.add_command(label="Save As...", command=lambda: self.change_output(self.tree_files.selection()))
        self.propertyMenu.add_command(label="Remove", command=lambda: self.remove_file(self.tree_files.selection()))
    # --------------------  post gui Load --------------------
        if input_file is not None:
            self.load_folder(input_file)
            self.flush_tree()

    def _popup(self, event):
        if self.tree_files.selection():
            if self.mp3_engine.get_status(self.tree_files.selection()[0]) == 'Queued':
                self.propertyMenu.entryconfig(0, state=NORMAL)
            else:
                self.propertyMenu.entryconfig(0, state=DISABLED)
            self.propertyMenu.post(event.x_root, event.y_root)
    def test(self):
        print "JOBS"
        for job in self.mp3_engine.jobs:
            print job
        print "QUEUES"
        for queue in self.mp3_engine.preview_queues():
            print queue

        print "ENGINE STATUS"
        print self.mp3_engine.current_status
        print "tree_files"
        for child in self.tree_files.get_children():
            print child

    def remove_file(self, item):
        self.mp3_engine.remove_audio_file(item[0])
        print "removing " + item[0]
        self.flush_tree()

    def change_output(self, item):
        new_name = asksaveasfilename()
        if new_name:
            # print new_name
            self.mp3_engine.change_output_name(item[0], new_name)
        self.flush_tree()
        pass

    def set_status(self, new_status):
        self.statusBar.config(text="Status: " +new_status)


    def add_file(self):
        new_file = askopenfilename(filetypes=[("Wave", "*.wav")])
        if new_file:
            self.mp3_engine.add_audio_file(new_file)
        self.flush_tree()


    def load_folder(self, new_folder):
        if new_folder:
            # print "Adding folder: " + str(new_folder)
            i = 0
            self.button_start.config(state=DISABLED)
            self.button_add_folder.config(state=DISABLED)
            self.button_add_file.config(state=DISABLED)
            self.button_stop.config(state=NORMAL)
            self.status = SEARCHING
            found_new = False
            for root, dir, files in os.walk(new_folder):
                if self.status == HALTING:
                    break
                i += 1
                if dir:
                    # print dir[0]
                    folder = dir[0][:80]
                    self.set_status("Searching: " + folder)

                for file in files:
                    if self.status == HALTING:
                        break
                    if ".wav" in file:
                        # print "Adding \"" + path.join(root, file) + "\" to the queue."
                        try:
                            found_new = True
                            path = os.path.join(root, file)
                            self.mp3_engine.add_audio_file(path)
                        except RuntimeError:
                            # print "collision"
                            pass
                if i % 100 == 0:
                    if found_new:
                        self.flush_tree()
                        found_new = False
        self.button_start.config(state=NORMAL)
        self.button_add_folder.config(state=NORMAL)
        self.button_add_file.config(state=NORMAL)
        self.button_stop.config(state=DISABLED)
        self.status = IDLE
        self.set_status("Idle")

    def add_folder(self):
        new_folder = askdirectory()
        new_folder = os.path.normcase(new_folder)
        self.t = threading.Thread(target=self.load_folder, args=(new_folder,))
        self.t.daemon = True
        try:
            # self.master.update_idletasks()
            self.set_status("Locating all wav files within " + new_folder)
            self.t.start()

            # self.load_folder(new_folder)
        except RuntimeError:
            showerror("Import Error", "These files are already in your queue.")

        self.flush_tree()

    def start_encoding(self):
        # print "Starting encoding"
        if self.status == IDLE:
            self.button_start.config(state=DISABLED)
            # self.working_thread = threading.Thread(target=self.mp3_engine.encode_next)
            self.working_thread = threading.Thread(target=self.mp3_engine.run)
            self.working_thread.daemon = True
            self.working_thread.start()
            # self.set_status("Working :"+ str(self.mp3_engine.status_percentage))
            self.status = WORKING
            self.button_stop.config(state=NORMAL)
                # print "alive"

        # self.mp3_engine.encode_next()
        self.update_progress()

    def abort(self):
        if askyesno("Are you sure?", "Are you sure you want to stop?"):
            if self.status == WORKING:
                self.mp3_engine.kill_encoding()
                self.working_thread.join()
                self.set_status("Stopped")
            if self.status == SEARCHING:
                self.status = HALTING
                self.t.join()
                self.set_status("Stopped")
            self.flush_tree()
            self.button_stop.config(state=DISABLED)

    def flush_tree(self):
        # with self.tree_lock:
        for i in self.tree_files.get_children():
            self.tree_files.delete(i)
        self.master.after(20)
    # for item in self.mp3_engine.preview_queues():
        for i, item in enumerate(self.mp3_engine.jobs):
            source = item['source']
            destination = item['destination']
            status = item['status']
            size = os.path.getsize(source)/1048576
            i += 1
            if size == 0:
                size = "Less than 1 MB"
            else:
                size = str(size) + " MB"
            self.tree_files.insert('', i, source)
            self.tree_files.set(source, 'status', status)
            self.master.after(10)
            self.tree_files.set(source, 'size', size)
            self.master.after(10)
            self.tree_files.set(source, 'source', source)
            self.master.after(10)
            self.tree_files.set(source, 'destination', destination)

        self.master.after(20)


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
            self.button_start.config(state=DISABLED)
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
def startup(input_file = None):
    root = Tk()
    if input_file:
        app = MainWindow(root, input_file)
    else:
        app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    # main()
    pass