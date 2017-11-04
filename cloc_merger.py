from tkinter import Tk, Label, Button, Entry, filedialog, StringVar
import csv


class FileData:  # Used for a database
    def __init__(self, lang, filename, blank, comment, code):
        self.lang = lang
        self.filename = filename
        self.blank = blank
        self.comment = comment
        self.code = code

    def as_list(self):
        return [self.lang, self.filename, self.blank, self.comment, self.code]

    def same_file(self, rhs):
        return self.filename == rhs.filename

def read_csv(filename):
    file_list = []
    with open(filename, 'r') as file:
        orig_csv = csv.reader(file, delimiter=",")
        next(orig_csv, None)  # Skip header
        for row in orig_csv:
            file_list.append(FileData(*(row[0:5])))  # HACK Might work
    return file_list

def write_csv(datalist, filename):
    with open(filename, 'w') as file:
        out_csv = csv.writer(file, delimiter=",", lineterminator='\n')
        out_csv.writerow(["language", "filename", "blank", "comment", "code", "Using CLOC Merger by Louis Hong @loolo78"]) # header
        for data in datalist:
            out_csv.writerow(data.as_list())

def merge(orig, modified):
    #N^2 algorithm
    # Note, two loops so we keep original's ordering, that's the whole point of this program
    final = []
    for o in orig: # Merge existing
        found = False
        for m in modified:
            if (o.filename == m.filename):
                final.append(m)
                found = True
                break
        if not found:
            final.append(o)

    for m in modified: # Union non-existing
        found = False
        for o in orig:
            if (m.filename == o.filename):
                found = True
                break
        if not found:
            final.append(m)
    return final


class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        self.master.minsize(width=400, height=250)
        master.title("CLOC Merger")

        self.label = Label(master, text="CLOC Merger by Louis Hong @loolo78")
        self.label.pack()

        #Original Files
        ####################
        self.original_entry_label = Label(master, text="Old/Previous CLOC file")
        self.original_entry_label.pack()

        self.original_cloc_filename = StringVar()
        self.original_entry = Entry(master, textvariable=self.original_cloc_filename)
        self.original_entry.pack()

        self.original_open_button = Button(master, text="Open File", command=self.open_original)
        self.original_open_button.pack()
        ####################

        #Modified Files
        ####################
        self.modified_label = Label(master, text="New CLOC file")
        self.modified_label.pack()

        self.modified_entry_filename = StringVar()
        self.modified_entry = Entry(master, textvariable=self.modified_entry_filename)
        self.modified_entry.pack()

        self.modified_open_button = Button(master, text="Open File", command=self.open_modified)
        self.modified_open_button.pack()
        ####################

        self.merge_button = Button(master, text="Merge", command=self.merge)
        self.merge_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def open_original(self):
        self.original_cloc_filename.set(filedialog.askopenfilename())
        pass

    def open_modified(self):
        self.modified_entry_filename.set(filedialog.askopenfilename())
        pass

    def merge(self):
        print("Start merge!")
        orig = read_csv(self.original_cloc_filename.get())
        modified = read_csv(self.modified_entry_filename.get())
        final = merge(orig,modified)
        write_csv(final, "merged_cloc_out.csv")
        print("Merged!")

root = Tk()
my_gui = ApplicationGUI(root)
root.mainloop()
