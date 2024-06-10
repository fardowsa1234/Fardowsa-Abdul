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
        self.root.title("LIBRARY MANAGEMENT SYSTEM")
        self.root.geometry("1350x750+0+0")
        self.root.configure(bg="light gray")

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
        self.lbl_title = Label(self.title_frame, text="LIBRARY MANAGEMENT SYSTEM", font=("arial", 40, "bold"), bg="powder blue", fg="navy")
        self.lbl_title.grid(row=0, column=0, padx=200)

        self.member_frame = LabelFrame(self.root, text="Member Information", bd=10, relief=RIDGE, padx=20, font=("arial", 12, "bold"), bg="light blue", fg="black")
        self.member_frame.place(x=0, y=130, width=400, height=620)

        self.book_frame = LabelFrame(self.root, text="Book Details", bd=10, relief=RIDGE, padx=20, font=("arial", 12, "bold"), bg="light green", fg="black")
        self.book_frame.place(x=400, y=130, width=450, height=620)

        self.button_frame = Frame(self.root, bd=10, relief=RIDGE, padx=20, bg="light gray")
        self.button_frame.place(x=850, y=130, width=500, height=620)

        self.display_frame = Frame(self.root, bd=10, relief=RIDGE, padx=20, bg="light gray")
        self.display_frame.place(x=0, y=750, width=1350, height=250)

        # Member Information Widgets
        self.create_label_entry(self.member_frame, "Member Type", self.membertype, row=0)
        self.create_label_entry(self.member_frame, "PRN No.", self.prnno, row=1)
        self.create_label_entry(self.member_frame, "ID No.", self.idno, row=2)
        self.create_label_entry(self.member_frame, "First Name", self.firstname, row=3)
        self.create_label_entry(self.member_frame, "Last Name", self.lastname, row=4)
        self.create_label_entry(self.member_frame, "Address 1", self.address1, row=5)
        self.create_label_entry(self.member_frame, "Address 2", self.address2, row=6)
        self.create_label_entry(self.member_frame, "Postcode", self.postcode, row=7)
        self.create_label_entry(self.member_frame, "Mobile", self.mobile, row=8)

        # Book Details Widgets
        self.create_label_entry(self.book_frame, "Book ID", self.bookid, row=0)
        self.create_label_entry(self.book_frame, "Title", self.title, row=1)
        self.create_label_entry(self.book_frame, "Author", self.author, row=2)
        self.create_label_entry(self.book_frame, "Date Borrowed", self.dateborrowed, row=3)
        self.create_label_entry(self.book_frame, "Days On Book", self.daysonbook, row=4)
        self.create_label_entry(self.book_frame, "Date Overdue", self.dateoverdue, row=5)
        self.create_label_entry(self.book_frame, "Late Return Fine", self.latereturnfine, row=6)

        # Button Frame Widgets
        self.create_button(self.button_frame, "Add Data", self.add_data, row=0)
        self.create_button(self.button_frame, "Display Data", self.display_data, row=1)
        self.create_button(self.button_frame, "Clear Data", self.clear_data, row=2)
        self.create_button(self.button_frame, "Update Data", self.update_data, row=3)
        self.create_button(self.button_frame, "Delete Data", self.delete_data, row=4)
        self.create_button(self.button_frame, "Exit", self.exit_system, row=5)

        # Treeview Widget for Displaying Data
        self.tv = ttk.Treeview(self.display_frame, columns=(
            "MemberType", "PRNNo", "IDNo", "FirstName", "LastName", "Address1", "Address2", "Postcode", "Mobile", "BookID", "Title", "Author", "DateBorrowed", "DaysOnBook", "DateOverdue", "LateReturnFine"), show='headings')
        self.tv.pack(fill=BOTH, expand=1)

        for col in self.tv["columns"]:
            self.tv.heading(col, text=col)
            self.tv.column(col, width=100)

        self.tv.bind("<ButtonRelease-1>", self.get_cursor)

    def create_label_entry(self, frame, label_text, variable, row):
        lbl = Label(frame, text=label_text, font=("arial", 12, "bold"), padx=2, pady=6, bg=frame.cget("bg"))
        lbl.grid(row=row, column=0, sticky=W)
        entry = Entry(frame, textvariable=variable, font=("arial", 12, "bold"), width=25)
        entry.grid(row=row, column=1, padx=10, pady=2)
        
    def create_button(self, frame, text, command, row):
        button = Button(frame, text=text, font=("arial", 12, "bold"), width=20, command=command, bg="navy", fg="white")
        button.grid(row=row, column=0, padx=10, pady=10)

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
            messagebox.showinfo("Success", "Member and Book data added successfully")
            self.clear_data()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error adding data: {e}")

    def display_data(self):
        self.tv.delete(*self.tv.get_children())
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
        contents = self.tv.item(cursor_row)
        row = contents['values']
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
            cursor_row = self.tv.focus()
            contents = self.tv.item(cursor_row)
            row = contents['values']
            member = session.query(Member).filter_by(idno=row[2]).first()
            if member:
                member.membertype = self.membertype.get()
                member.prnno = self.prnno.get()
                member.firstname = self.firstname.get()
                member.lastname = self.lastname.get()
                member.address1 = self.address1.get()
                member.address2 = self.address2.get()
                member.postcode = self.postcode.get()
                member.mobile = self.mobile.get()
                
                book = session.query(Book).filter_by(bookid=row[9]).first()
                if book:
                    book.title = self.title.get()
                    book.author = self.author.get()
                    book.dateborrowed = datetime.datetime.strptime(self.dateborrowed.get(), "%d/%m/%Y").date()
                    book.daysonbook = int(self.daysonbook.get())
                    book.dateoverdue = datetime.datetime.strptime(self.dateoverdue.get(), "%d/%m/%Y").date()
                    book.latereturnfine = self.latereturnfine.get()

                session.commit()
                messagebox.showinfo("Success", "Data updated successfully")
                self.display_data()
                self.clear_data()
            else:
                messagebox.showerror("Error", "No record found to update")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error updating data: {e}")

    def delete_data(self):
        try:
            cursor_row = self.tv.focus()
            contents = self.tv.item(cursor_row)
            row = contents['values']
            member = session.query(Member).filter_by(idno=row[2]).first()
            if member:
                session.delete(member)
                session.commit()
                messagebox.showinfo("Success", "Data deleted successfully")
                self.display_data()
                self.clear_data()
            else:
                messagebox.showerror("Error", "No record found to delete")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error deleting data: {e}")

    def exit_system(self):
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    application = LibraryManagementSystem(root)
    root.mainloop()
