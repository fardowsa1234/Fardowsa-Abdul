from tkinter import *
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, validates
import datetime

# SQLAlchemy setup
Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    membertype = Column(String, nullable=False)
    prnno = Column(String, nullable=False)
    idno = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    mobile = Column(String, nullable=False)

    books = relationship('Book', backref='member', cascade='all, delete-orphan')

    @validates('postcode')
    def validate_postcode(self, key, postcode):
        if len(postcode) != 5 or not postcode.isdigit():
            raise ValueError("Postcode must be a 5-digit number")
        return postcode

    @validates('mobile')
    def validate_mobile(self, key, mobile):
        if not mobile.isdigit() or len(mobile) < 10:
            raise ValueError("Invalid mobile number")
        return mobile

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    bookid = Column(String, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    dateborrowed = Column(Date, nullable=False)
    daysonbook = Column(Integer, nullable=False)
    dateoverdue = Column(Date, nullable=False)
    latereturnfine = Column(String, nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'))

# Database setup
engine = create_engine('sqlite:///library.db')

# Drop the existing books table if it exists
meta = MetaData()
meta.reflect(bind=engine)
if 'books' in meta.tables:
    books_table = meta.tables['books']
    books_table.drop(engine)

# Create tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# GUI setup
class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1350x750+0+0")

        # Variables
        self.membertype = StringVar()
        self.prnno = StringVar()
        self.idno = StringVar()
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.address1 = StringVar()
        self.address2 = StringVar()
        self.postcode = StringVar()
        self.mobile = StringVar()
        self.bookid = StringVar()
        self.title = StringVar()
        self.author = StringVar()
        self.dateborrowed = StringVar()
        self.daysonbook = StringVar()
        self.dateoverdue = StringVar()
        self.latereturnfine = StringVar()
        self.dateborrowed_var = StringVar()

        # GUI Design
        self.title_frame = Frame(self.root, bd=10, relief=RIDGE, padx=20, bg="powder blue")
        self.title_frame.pack(side=TOP, fill=X)
        self.lbl_title = Label(self.title_frame, text="Library Management System", font=("arial", 40, "bold"), bg="powder blue")
        self.lbl_title.grid(row=0, column=0, padx=200)

        self.member_frame = LabelFrame(self.root, text="Member Information", bd=10, relief=RIDGE, padx=20, font=("arial", 12, "bold"))
        self.member_frame.place(x=0, y=130, width=400, height=620)

        self.book_frame = LabelFrame(self.root, text="Book Details", bd=10, relief=RIDGE, padx=20, font=("arial", 12, "bold"))
        self.book_frame.place(x=400, y=130, width=450, height=620)

        self.button_frame = Frame(self.root, bd=10, relief=RIDGE, padx=20)
        self.button_frame.place(x=850, y=130, width=500, height=620)

        self.display_frame = Frame(self.root, bd=10, relief=RIDGE, padx=20)
        self.display_frame.place(x=0, y=750, width=1350, height=250)

        # Member Information Widgets
        self.lbl_membertype = Label(self.member_frame, text="Member Type", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_membertype.grid(row=0, column=0, sticky=W)
        self.cbo_membertype = ttk.Combobox(self.member_frame, textvariable=self.membertype, state='readonly', font=("arial", 12, "bold"), width=23)
        self.cbo_membertype['value'] = ('Student', 'Lecturer', 'Admin', 'Staff')
        self.cbo_membertype.current(0)
        self.cbo_membertype.grid(row=0, column=1)

        self.lbl_prnno = Label(self.member_frame, text="PRN No.", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_prnno.grid(row=1, column=0, sticky=W)
        self.txt_prnno = Entry(self.member_frame, textvariable=self.prnno, font=("arial", 12, "bold"), width=25)
        self.txt_prnno.grid(row=1, column=1)

        self.lbl_idno = Label(self.member_frame, text="ID No.", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_idno.grid(row=2, column=0, sticky=W)
        self.txt_idno = Entry(self.member_frame, textvariable=self.idno, font=("arial", 12, "bold"), width=25)
        self.txt_idno.grid(row=2, column=1)

        self.lbl_firstname = Label(self.member_frame, text="First Name", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_firstname.grid(row=3, column=0, sticky=W)
        self.txt_firstname = Entry(self.member_frame, textvariable=self.firstname, font=("arial", 12, "bold"), width=25)
        self.txt_firstname.grid(row=3, column=1)

        self.lbl_lastname = Label(self.member_frame, text="Last Name", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_lastname.grid(row=4, column=0, sticky=W)
        self.txt_lastname = Entry(self.member_frame, textvariable=self.lastname, font=("arial", 12, "bold"), width=25)
        self.txt_lastname.grid(row=4, column=1)

        self.lbl_address1 = Label(self.member_frame, text="Address 1", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_address1.grid(row=5, column=0, sticky=W)
        self.txt_address1 = Entry(self.member_frame, textvariable=self.address1, font=("arial", 12, "bold"), width=25)
        self.txt_address1.grid(row=5, column=1)

        self.lbl_address2 = Label(self.member_frame, text="Address 2", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_address2.grid(row=6, column=0, sticky=W)
        self.txt_address2 = Entry(self.member_frame, textvariable=self.address2, font=("arial", 12, "bold"), width=25)
        self.txt_address2.grid(row=6, column=1)

        self.lbl_postcode = Label(self.member_frame, text="Postcode", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_postcode.grid(row=7, column=0, sticky=W)
        self.txt_postcode = Entry(self.member_frame, textvariable=self.postcode, font=("arial", 12, "bold"), width=25)
        self.txt_postcode.grid(row=7, column=1)

        self.lbl_mobile = Label(self.member_frame, text="Mobile", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_mobile.grid(row=8, column=0, sticky=W)
        self.txt_mobile = Entry(self.member_frame, textvariable=self.mobile, font=("arial", 12, "bold"), width=25)
        self.txt_mobile.grid(row=8, column=1)

        # Book Details Widgets
        self.lbl_bookid = Label(self.book_frame, text="Book ID", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_bookid.grid(row=0, column=0, sticky=W)
        self.txt_bookid = Entry(self.book_frame, textvariable=self.bookid, font=("arial", 12, "bold"), width=25)
        self.txt_bookid.grid(row=0, column=1)

        self.lbl_title = Label(self.book_frame, text="Title", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_title.grid(row=1, column=0, sticky=W)
        self.txt_title = Entry(self.book_frame, textvariable=self.title, font=("arial", 12, "bold"), width=25)
        self.txt_title.grid(row=1, column=1)

        self.lbl_author = Label(self.book_frame, text="Author", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_author.grid(row=2, column=0, sticky=W)
        self.txt_author = Entry(self.book_frame, textvariable=self.author, font=("arial", 12, "bold"), width=25)
        self.txt_author.grid(row=2, column=1)

        self.lbl_dateborrowed = Label(self.book_frame, text="Date Borrowed", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_dateborrowed.grid(row=3, column=0, sticky=W)
        self.txt_dateborrowed = Entry(self.book_frame, textvariable=self.dateborrowed, font=("arial", 12, "bold"), width=25)
        self.txt_dateborrowed.grid(row=3, column=1)

        self.lbl_daysonbook = Label(self.book_frame, text="Days On Book", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_daysonbook.grid(row=4, column=0, sticky=W)
        self.txt_daysonbook = Entry(self.book_frame, textvariable=self.daysonbook, font=("arial", 12, "bold"), width=25)
        self.txt_daysonbook.grid(row=4, column=1)

        self.lbl_dateoverdue = Label(self.book_frame, text="Date Overdue", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_dateoverdue.grid(row=5, column=0, sticky=W)
        self.txt_dateoverdue = Entry(self.book_frame, textvariable=self.dateoverdue, font=("arial", 12, "bold"), width=25)
        self.txt_dateoverdue.grid(row=5, column=1)

        self.lbl_latereturnfine = Label(self.book_frame, text="Late Return Fine", font=("arial", 12, "bold"), padx=2, pady=6)
        self.lbl_latereturnfine.grid(row=6, column=0, sticky=W)
        self.txt_latereturnfine = Entry(self.book_frame, textvariable=self.latereturnfine, font=("arial", 12, "bold"), width=25)
        self.txt_latereturnfine.grid(row=6, column=1)

        # Button Frame Widgets
        self.btn_add = Button(self.button_frame, text="Add Data", font=("arial", 12, "bold"), width=20, command=self.add_data)
        self.btn_add.grid(row=0, column=0, padx=10, pady=10)

        self.btn_display = Button(self.button_frame, text="Display Data", font=("arial", 12, "bold"), width=20, command=self.display_data)
        self.btn_display.grid(row=1, column=0, padx=10, pady=10)

        self.btn_clear = Button(self.button_frame, text="Clear Data", font=("arial", 12, "bold"), width=20, command=self.clear_data)
        self.btn_clear.grid(row=2, column=0, padx=10, pady=10)

        self.btn_update = Button(self.button_frame, text="Update Data", font=("arial", 12, "bold"), width=20, command=self.update_data)
        self.btn_update.grid(row=3, column=0, padx=10, pady=10)

        self.btn_delete = Button(self.button_frame, text="Delete Data", font=("arial", 12, "bold"), width=20, command=self.delete_data)
        self.btn_delete.grid(row=4, column=0, padx=10, pady=10)

        self.btn_exit = Button(self.button_frame, text="Exit", font=("arial", 12, "bold"), width=20, command=self.exit_system)
        self.btn_exit.grid(row=5, column=0, padx=10, pady=10)

        # Treeview Widget for Displaying Data
        self.tv = ttk.Treeview(self.display_frame, columns=("MemberType", "PRNNo", "IDNo", "FirstName", "LastName", "Address1", "Address2", "Postcode", "Mobile", "BookID", "Title", "Author", "DateBorrowed", "DaysOnBook", "DateOverdue", "LateReturnFine"), show='headings')
        self.tv.pack(fill=BOTH, expand=1)

        for col in self.tv["columns"]:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=100)

        self.tv.bind("<ButtonRelease-1>", self.get_cursor)

    def add_data(self):
        try:
            new_member = Member(
                membertype=self.membertype.get(),
                prnno=self.prnno.get(),
                idno=self.idno.get(),
                firstname=self.firstname.get(),
                lastname=self.lastname.get(),
                address1=self.address1.get(),
                address2=self.address2.get(),
                postcode=self.postcode.get(),
                mobile=self.mobile.get()
            )
            new_book = Book(
                bookid=self.bookid.get(),
                title=self.title.get(),
                author=self.author.get(),
                dateborrowed=datetime.datetime.strptime(self.dateborrowed.get(), "%d/%m/%Y").date(),
                daysonbook=int(self.daysonbook.get()),
                dateoverdue=datetime.datetime.strptime(self.dateoverdue.get(), "%d/%m/%Y").date(),
                latereturnfine=self.latereturnfine.get(),
                member=new_member
            )

            session.add(new_member)
            session.add(new_book)
            session.commit()

            messagebox.showinfo("Success", "Data added successfully")
            self.display_data()  # Refresh the display
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error adding data: {e}")

    def display_data(self):
        # Clear the Treeview
        for row in self.tv.get_children():
            self.tv.delete(row)

        # Fetch data from the database and insert into the Treeview
        members = session.query(Member).all()
        for member in members:
            for book in member.books:
                self.tv.insert("", "end", values=(
                    member.membertype, member.prnno, member.idno, member.firstname, member.lastname,
                    member.address1, member.address2, member.postcode, member.mobile,
                    book.bookid, book.title, book.author, book.dateborrowed, book.daysonbook,
                    book.dateoverdue, book.latereturnfine
                ))

    def clear_data(self):
        self.membertype.set("")
        self.prnno.set("")
        self.idno.set("")
        self.firstname.set("")
        self.lastname.set("")
        self.address1.set("")
        self.address2.set("")
        self.postcode.set("")
        self.mobile.set("")
        self.bookid.set("")
        self.title.set("")
        self.author.set("")
        self.dateborrowed.set("")
        self.daysonbook.set("")
        self.dateoverdue.set("")
        self.latereturnfine.set("")

    def get_cursor(self, event):
        cursor_row = self.tv.focus()
        content = self.tv.item(cursor_row)
        row = content['values']

        if row:
            self.membertype.set(row[0])
            self.prnno.set(row[1])
            self.idno.set(row[2])
            self.firstname.set(row[3])
            self.lastname.set(row[4])
            self.address1.set(row[5])
            self.address2.set(row[6])
            self.postcode.set(row[7])
            self.mobile.set(row[8])
            self.bookid.set(row[9])
            self.title.set(row[10])
            self.author.set(row[11])
            self.dateborrowed.set(row[12])
            self.daysonbook.set(row[13])
            self.dateoverdue.set(row[14])
            self.latereturnfine.set(row[15])

    def update_data(self):
      try:
        selected_row = self.tv.focus()
        if not selected_row:
            messagebox.showwarning("Warning", "Please select a record to update")
            return

        content = self.tv.item(selected_row)
        row = content['values']

        if len(row) < 16:
            messagebox.showerror("Error", "Selected record does not contain all required data fields")
            return

        member_id = session.query(Member.id).filter(Member.prnno == row[1]).scalar()

        session.query(Member).filter_by(id=member_id).update({
            Member.membertype: self.membertype.get(),
            Member.prnno: self.prnno.get(),
            Member.idno: self.idno.get(),
            Member.firstname: self.firstname.get(),
            Member.lastname: self.lastname.get(),
            Member.address1: self.address1.get(),
            Member.address2: self.address2.get(),
            Member.postcode: self.postcode.get(),
            Member.mobile: self.mobile.get()
        })

        session.query(Book).filter_by(member_id=member_id).update({
            Book.bookid: self.bookid.get(),
            Book.title: self.title.get(),
            Book.author: self.author.get(),
            Book.dateborrowed: datetime.datetime.strptime(self.dateborrowed.get(), "%d/%m/%Y").date(),
            Book.daysonbook: int(self.daysonbook.get()),
            Book.dateoverdue: datetime.datetime.strptime(self.dateoverdue.get(), "%d/%m/%Y").date(),
            Book.latereturnfine: self.latereturnfine.get()
        })

        session.commit()
        messagebox.showinfo("Success", "Data updated successfully")
        self.display_data()  # Refresh the display
      except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Error updating data: {e}")


    def delete_data(self):
        try:
            selected_row = self.tv.focus()
            content = self.tv.item(selected_row)
            row = content['values']
            member_id = session.query(Member.id).filter(Member.prnno == row[1]).scalar()

            member = session.query(Member).filter_by(id=member_id).first()
            if member:
                session.delete(member)
                session.commit()
                messagebox.showinfo("Success", "Data deleted successfully")
                self.display_data()  # Refresh the display
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error deleting data: {e}")

    def exit_system(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    application = LibraryManagementSystem(root)
    root.mainloop()
