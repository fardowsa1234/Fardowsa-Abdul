import argparse
from datetime import datetime

from sqlalchemy import text
from models import initialize_database, session, Member, Book

def add_member(args):
    if not args.membertype:
        args.membertype = input("Enter member type: ")
    if not args.prnno:
        args.prnno = input("Enter PRN number: ")
    if not args.idno:
        args.idno = input("Enter ID number: ")
    if not args.firstname:
        args.firstname = input("Enter first name: ")
    if not args.lastname:
        args.lastname = input("Enter last name: ")
    if not args.address1:
        args.address1 = input("Enter address line 1: ")
    if not args.address2:
        args.address2 = input("Enter address line 2: ")
    if not args.postcode:
        args.postcode = input("Enter postcode: ")
    if not args.mobile:
        args.mobile = input("Enter mobile number: ")

    member = Member(
        membertype=args.membertype,
        prnno=args.prnno,
        idno=args.idno,
        firstname=args.firstname,
        lastname=args.lastname,
        address1=args.address1,
        address2=args.address2,
        postcode=args.postcode,
        mobile=args.mobile
    )
    session.add(member)
    session.commit()
    print(f"Added member: {member.firstname} {member.lastname}")

def add_book(args):
    if not args.bookid:
        args.bookid = input("Enter book ID: ")
    if not args.title:
        args.title = input("Enter title: ")
    if not args.author:
        args.author = input("Enter author: ")
    if not args.dateborrowed:
        args.dateborrowed = input("Enter date borrowed (YYYY-MM-DD): ")
    if not args.daysonbook:
        args.daysonbook = int(input("Enter days on book: "))
    if not args.dateoverdue:
        args.dateoverdue = input("Enter date overdue (YYYY-MM-DD): ")
    if not args.latereturnfine:
        args.latereturnfine = float(input("Enter late return fine: "))
    if not args.member_id:
        args.member_id = int(input("Enter member ID: "))

    try:
        date_borrowed = datetime.strptime(args.dateborrowed, "%Y-%m-%d").date()
        date_overdue = datetime.strptime(args.dateoverdue, "%Y-%m-%d").date()

        book = Book(
            bookid=args.bookid,
            title=args.title,
            author=args.author,
            dateborrowed=date_borrowed,
            daysonbook=args.daysonbook,
            dateoverdue=date_overdue,
            latereturnfine=args.latereturnfine,
            member_id=args.member_id
        )

        session.add(book)
        session.commit()
        print(f"Added book: {book.title}, Author: {book.author}")
    except ValueError as ve:
        print(f"Error parsing date: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_members(args):
    members = session.query(Member).all()
    for member in members:
        print(f"ID: {member.id}, Name: {member.firstname} {member.lastname}, Type: {member.membertype}")

def view_books(args):
    books = session.query(Book).all()
    for book in books:
        print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}")

def delete_member(args):
    member = session.query(Member).get(args.member_id)
    if member:
        session.delete(member)
        session.commit()
        print(f"Deleted member with ID {args.member_id}")
    else:
        print(f"No member found with ID {args.member_id}")

def reset_auto_increment(args):
    session.execute(text('DELETE FROM books'))
    session.execute(text('DELETE FROM sqlite_sequence WHERE name="books"'))
    session.execute(text('DELETE FROM members'))
    session.execute(text('DELETE FROM sqlite_sequence WHERE name="members"'))
    session.commit()
    print("Auto-incrementing IDs have been reset.")

def main():
    initialize_database()
    
    parser = argparse.ArgumentParser(description="Library Management CLI")
    subparsers = parser.add_subparsers()

    # Add member subcommand
    parser_add_member = subparsers.add_parser('add_member', help='Add a new member')
    parser_add_member.add_argument('membertype', type=str, nargs='?', help='Type of the member')
    parser_add_member.add_argument('prnno', type=str, nargs='?', help='PRN number of the member')
    parser_add_member.add_argument('idno', type=str, nargs='?', help='ID number of the member')
    parser_add_member.add_argument('firstname', type=str, nargs='?', help='First name of the member')
    parser_add_member.add_argument('lastname', type=str, nargs='?', help='Last name of the member')
    parser_add_member.add_argument('address1', type=str, nargs='?', help='Address line 1')
    parser_add_member.add_argument('address2', type=str, nargs='?', help='Address line 2')
    parser_add_member.add_argument('postcode', type=str, nargs='?', help='Postcode')
    parser_add_member.add_argument('mobile', type=str, nargs='?', help='Mobile number')
    parser_add_member.set_defaults(func=add_member)

    # Add book subcommand
    parser_add_book = subparsers.add_parser('add_book', help='Add a new book')
    parser_add_book.add_argument('bookid', type=str, nargs='?', help='ID of the book')
    parser_add_book.add_argument('title', type=str, nargs='?', help='Title of the book')
    parser_add_book.add_argument('author', type=str, nargs='?', help='Author of the book')
    parser_add_book.add_argument('dateborrowed', type=str, nargs='?', help='Date borrowed (YYYY-MM-DD)')
    parser_add_book.add_argument('daysonbook', type=int, nargs='?', help='Number of days the book can be borrowed')
    parser_add_book.add_argument('dateoverdue', type=str, nargs='?', help='Date overdue (YYYY-MM-DD)')
    parser_add_book.add_argument('latereturnfine', type=float, nargs='?', help='Fine for late return')
    parser_add_book.add_argument('member_id', type=int, nargs='?', help='ID of the member borrowing the book')
    parser_add_book.set_defaults(func=add_book)

    # View members
    parser_view_members = subparsers.add_parser('view_members', help='View all members')
    parser_view_members.set_defaults(func=view_members)

    # View books 
    parser_view_books = subparsers.add_parser('view_books', help='View all books')
    parser_view_books.set_defaults(func=view_books)

    # Delete member
    parser_delete_member = subparsers.add_parser('delete_member', help='Delete a member by ID')
    parser_delete_member.add_argument('member_id', type=int, help='ID of the member to delete')
    parser_delete_member.set_defaults(func=delete_member)

    # Reset IDs
    parser_reset_ids = subparsers.add_parser('reset_ids', help='Reset auto-incrementing IDs for Member and Book tables')
    parser_reset_ids.set_defaults(func=reset_auto_increment)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
