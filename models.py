from sqlalchemy import Column, String, Integer, Date, ForeignKey, Float, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    membertype = Column(String, nullable=False)
    prnno = Column(String, unique=True, nullable=False)
    idno = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    mobile = Column(String, nullable=False)

    books = relationship('Book', back_populates='member')

    def __repr__(self):
        return f"<Member(id={self.id}, prnno={self.prnno}, firstname={self.firstname}, lastname={self.lastname})>"

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bookid = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    dateborrowed = Column(Date, nullable=False)
    daysonbook = Column(Integer, nullable=False)
    dateoverdue = Column(Date, nullable=False)
    latereturnfine = Column(Float, nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)

    member = relationship('Member', back_populates='books')

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"

# Database configuration
DATABASE_URL = 'sqlite:///library.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def initialize_database():
    Base.metadata.create_all(engine)
