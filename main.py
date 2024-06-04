from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1550x800+0+0")

        lbtitle = Label(self.root, text="LIBRARY MANAGEMENT SYSTEM", bg="powder blue", fg="green", bd=20, relief=RIDGE,
                        font=("times new roman", 50, "bold"), padx=2, pady=6)
        lbtitle.pack(side=TOP, fill=X)

        frame = Frame(self.root, bd=12, relief=RIDGE, padx=20, bg="powder blue")
        frame.place(x=0, y=130, width=1530, height=400)

        # Database connection and table creation
        self.conn = sqlite3.connect('library.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS members (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                membertype TEXT,
                                prnno TEXT,
                                idno TEXT,
                                firstname TEXT,
                                lastname TEXT,
                                address1 TEXT,
                                address2 TEXT,
                                postcode TEXT,
                                mobile TEXT,
                                bookid TEXT,
                                booktitle TEXT,
                                author TEXT,
                                dateborrowed TEXT,
                                daysonbook TEXT,
                                dateoverdue TEXT,
                                latereturnfine TEXT)''')
        self.conn.commit()

        self.selected_id = None  # Initialize selected_id

        # Data Frame Left
        DataFrameLeft = LabelFrame(frame, text="Library Members details", bg="powder blue", fg="green", bd=12, relief=RIDGE,
                                   font=("times new roman", 12, "bold"), padx=2, pady=6)
        DataFrameLeft.place(x=0, y=5, width=900, height=350)

        lblmember = Label(DataFrameLeft, bg="powder blue", text="Member Type", font=("times new roman", 15, "bold"), padx=2, pady=6)
        lblmember.grid(row=0, column=0, sticky=W)

        self.comMember = ttk.Combobox(DataFrameLeft, state="readonly", font=("arial", 12, "bold"), width=27)
        self.comMember["value"] = ("Admin", "Staff", "Student", "Lecturer")
        self.comMember.grid(row=0, column=1)

        labels_and_entries = [
            ("Prn no", 1, 0, "prnno"),
            ("ID No", 2, 0, "idno"),
            ("First Name", 3, 0, "firstname"),
            ("Last Name", 4, 0, "lastname"),
            ("Address1", 5, 0, "address1"),
            ("Address2", 6, 0, "address2"),
            ("Post Code", 7, 0, "postcode"),
            ("Mobile", 8, 0, "mobile"),
            ("Book Title", 1, 2, "booktitle"),
            ("Book Id", 0, 2, "bookid"),
            ("Author Name", 2, 2, "author"),
            ("Date Borrowed", 3, 2, "dateborrowed"),
            ("Days On Book", 4, 2, "daysonbook"),
            ("Date Over Due", 7, 2, "dateoverdue"),
            ("Late Return Fine", 6, 2, "latereturnfine"),
        ]

        self.entries = {}

        for text, row, col, var in labels_and_entries:
            label = Label(DataFrameLeft, bg="powder blue", text=text, font=("times new roman", 12, "bold"), padx=2, pady=6)
            label.grid(row=row, column=col, sticky=W)
            entry = Entry(DataFrameLeft, font=("times new roman", 13, "bold"), width=29)
            entry.grid(row=row, column=col+1)
            self.entries[var] = entry

        # Data Frame Right
        DataFrameRight = LabelFrame(frame, text="Book Details", bg="powder blue", fg="green", bd=12, relief=RIDGE,
                                    font=("times new roman", 12, "bold"), padx=20, pady=6)
        DataFrameRight.place(x=870, y=5, width=500, height=350)

        self.textBox = Text(DataFrameRight, font=("arial", 12, "bold"), width=32, height=16, padx=2, pady=6)
        self.textBox.grid(row=0, column=2)

        listScrollbar = Scrollbar(DataFrameRight)
        listScrollbar.grid(row=0, column=1, sticky="ns")

        listBooks = ['Head First Book', 'Learn Python The Hard Way', 'Python Programming', "Secret Rahshy", "Python CookBook",
                     'Into Machine Learning', "Fluent Python", 'Machine Techno', 'My Python', 'Joss Ellif Guru',
                     'Elite Jungle Python', 'Jungli Python', 'Pune Python', 'Machine Python', 'Advanced Python',
                     'Into Python', 'RedChill Python', 'Ishq Python']

        listbox = Listbox(DataFrameRight, font=("arial", 12, "bold"), width=20, height=16, yscrollcommand=listScrollbar.set)
        listbox.grid(row=0, column=0, padx=0, pady=4)
        listScrollbar.config(command=listbox.yview)

        for item in listBooks:
            listbox.insert(END, item)

        # Buttons Frame
        framebutton = Frame(self.root, bd=12, relief=RIDGE, padx=20, bg="powder blue")
        framebutton.place(x=0, y=540, width=1530, height=70)

        button_texts = ["Add Data", "Show Data", "Update", "Delete", "Reset", "Exit"]
        button_commands = [self.add_data, self.show_data, self.update_data, self.delete_data, self.reset_data, self.exit_app]
        
        for i, (text, command) in enumerate(zip(button_texts, button_commands)):
            btn = Button(framebutton, text=text, font=("arial", 12, "bold"), width=23, bg="blue", fg="white", command=command)
            btn.grid(row=0, column=i)

        # Information Frame
        FrameDetails = Frame(self.root, bd=12, relief=RIDGE, padx=20, bg="powder blue")
        FrameDetails.place(x=0, y=610, width=1530, height=150)

        Table_frame = Frame(FrameDetails, bd=12, relief=RIDGE, bg="powder blue")
        Table_frame.place(x=0, y=2, width=1460, height=190)

        xscroll = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        yscroll = ttk.Scrollbar(Table_frame, orient=VERTICAL)

        self.library_table = ttk.Treeview(Table_frame, column=("id", "membertype", "prnno", "idno", "firstname", "lastname", "address1",
                                                              "address2", "postcode", "mobile", "bookid", "booktitle", "author",
                                                              "dateborrowed", "daysonbook", "dateoverdue", "latereturnfine"), 
                                          xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)

        xscroll.config(command=self.library_table.xview)
        yscroll.config(command=self.library_table.yview)

        self.library_table.heading("id", text="ID")
        self.library_table.heading("membertype", text="Member Type")
        self.library_table.heading("prnno", text="PRN No")
        self.library_table.heading("idno", text="ID No")
        self.library_table.heading("firstname", text="First Name")
        self.library_table.heading("lastname", text="Last Name")
        self.library_table.heading("address1", text="Address1")
        self.library_table.heading("address2", text="Address2")
        self.library_table.heading("postcode", text="Post Code")
        self.library_table.heading("mobile", text="Mobile")
        self.library_table.heading("bookid", text="Book ID")
        self.library_table.heading("booktitle", text="Book Title")
        self.library_table.heading("author", text="Author")
        self.library_table.heading("dateborrowed", text="Date Borrowed")
        self.library_table.heading("daysonbook", text="Days On Book")
        self.library_table.heading("dateoverdue", text="Date Over Due")
        self.library_table.heading("latereturnfine", text="Late Return Fine")

        self.library_table["show"] = "headings"
        self.library_table.pack(fill=BOTH, expand=1)
        
        self.library_table.column("id", width=50)
        self.library_table.column("membertype", width=150) 
        self.library_table.column("prnno", width=150)   
        self.library_table.column("idno", width=150)
        self.library_table.column("firstname", width=150) 
        self.library_table.column("lastname", width=150)
        self.library_table.column("address1", width=150)
        self.library_table.column("address2", width=150)
        self.library_table.column("postcode", width=150)
        self.library_table.column("mobile", width=150)
        self.library_table.column("bookid", width=150)
        self.library_table.column("booktitle", width=150)
        self.library_table.column("author", width=100)
        self.library_table.column("dateborrowed", width=150)
        self.library_table.column("daysonbook", width=150)
        self.library_table.column("dateoverdue", width=150)
        self.library_table.column("latereturnfine", width=150)

        self.library_table.bind("<ButtonRelease-1>", self.get_cursor)

    def add_data(self):
        try:
            self.cur.execute('''INSERT INTO members (membertype, prnno, idno, firstname, lastname, address1, address2, postcode,
                            mobile, bookid, booktitle, author, dateborrowed, daysonbook, dateoverdue, latereturnfine)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (self.comMember.get(),
                              self.entries['prnno'].get(),
                              self.entries['idno'].get(),
                              self.entries['firstname'].get(),
                              self.entries['lastname'].get(),
                              self.entries['address1'].get(),
                              self.entries['address2'].get(),
                              self.entries['postcode'].get(),
                              self.entries['mobile'].get(),
                              self.entries['bookid'].get(),
                              self.entries['booktitle'].get(),
                              self.entries['author'].get(),
                              self.entries['dateborrowed'].get(),
                              self.entries['daysonbook'].get(),
                              self.entries['dateoverdue'].get(),
                              self.entries['latereturnfine'].get()))
            self.conn.commit()
            self.show_data()
            messagebox.showinfo("Success", "Record added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_data(self):
        self.cur.execute("SELECT * FROM members")
        rows = self.cur.fetchall()
        if len(rows) != 0:
            self.library_table.delete(*self.library_table.get_children())
            for row in rows:
                self.library_table.insert('', END, values=row)
            self.conn.commit()

    def update_data(self):
        try:
            self.cur.execute('''UPDATE members SET membertype=?, prnno=?, idno=?, firstname=?, lastname=?, address1=?, address2=?,
                            postcode=?, mobile=?, bookid=?, booktitle=?, author=?, dateborrowed=?, daysonbook=?, dateoverdue=?,
                            latereturnfine=? WHERE id=?''',
                             (self.comMember.get(),
                              self.entries['prnno'].get(),
                              self.entries['idno'].get(),
                              self.entries['firstname'].get(),
                              self.entries['lastname'].get(),
                              self.entries['address1'].get(),
                              self.entries['address2'].get(),
                              self.entries['postcode'].get(),
                              self.entries['mobile'].get(),
                              self.entries['bookid'].get(),
                              self.entries['booktitle'].get(),
                              self.entries['author'].get(),
                              self.entries['dateborrowed'].get(),
                              self.entries['daysonbook'].get(),
                              self.entries['dateoverdue'].get(),
                              self.entries['latereturnfine'].get(),
                              self.selected_id))
            self.conn.commit()
            self.show_data()
            messagebox.showinfo("Success", "Record updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_data(self):
        if self.selected_id is None:
            messagebox.showerror("Error", "No record selected")
            return

        try:
            self.cur.execute('DELETE FROM members WHERE id=?', (self.selected_id,))
            self.conn.commit()
            self.show_data()
            messagebox.showinfo("Success", "Record deleted successfully")
            self.selected_id = None  # Clear the selected_id after deletion
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_data(self):
        for entry in self.entries.values():
            entry.delete(0, END)
        self.comMember.set('')

    def get_cursor(self, event=""):
        cursor_row = self.library_table.focus()
        contents = self.library_table.item(cursor_row)
        row = contents['values']
        if row:
            self.selected_id = row[0]
            self.comMember.set(row[1])
            self.entries['prnno'].delete(0, END)
            self.entries['prnno'].insert(END, row[2])
            self.entries['idno'].delete(0, END)
            self.entries['idno'].insert(END, row[3])
            self.entries['firstname'].delete(0, END)
            self.entries['firstname'].insert(END, row[4])
            self.entries['lastname'].delete(0, END)
            self.entries['lastname'].insert(END, row[5])
            self.entries['address1'].delete(0, END)
            self.entries['address1'].insert(END, row[6])
            self.entries['address2'].delete(0, END)
            self.entries['address2'].insert(END, row[7])
            self.entries['postcode'].delete(0, END)
            self.entries['postcode'].insert(END, row[8])
            self.entries['mobile'].delete(0, END)
            self.entries['mobile'].insert(END, row[9])
            self.entries['bookid'].delete(0, END)
            self.entries['bookid'].insert(END, row[10])
            self.entries['booktitle'].delete(0, END)
            self.entries['booktitle'].insert(END, row[11])
            self.entries['author'].delete(0, END)
            self.entries['author'].insert(END, row[12])
            self.entries['dateborrowed'].delete(0, END)
            self.entries['dateborrowed'].insert(END, row[13])
            self.entries['daysonbook'].delete(0, END)
            self.entries['daysonbook'].insert(END, row[14])
            self.entries['dateoverdue'].delete(0, END)
            self.entries['dateoverdue'].insert(END, row[15])
            self.entries['latereturnfine'].delete(0, END)
            self.entries['latereturnfine'].insert(END, row[16])

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
