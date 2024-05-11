from enum import Enum
from datetime import datetime

import datetime
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import String, Boolean, DateTime, Column, Integer, ForeignKey, Float, Table
from flask_login import UserMixin

BOOK_STATUS = ["AVAILABLE", "BORROWED"]


class BookStatus(Enum):
  UNAVAILABLE = 0
  AVAILABLE = 1
  BORROWED = 2

class BookCategory(Enum):
  FICTION = "FICTION"
  NON_FICTION = "NON FICTION"
  NOVEL = "NOBEL"
  SCIENCE = "SCIENCE"
  ARTS = "ARTS"
  PROGRAMMING = "PROGRAMMING"
  LITERATURE = "LITERATURE"
  

# base model all other db models will inherit from it.
class Base(DeclarativeBase):
  pass


# Association table for the many-to-many relationship between Member and Book for favorites
favorite_books_association = Table(
    'favorite_books',
    Base.metadata,
    Column('member_id', Integer, ForeignKey('members.member_id')),
    Column('book_id', Integer, ForeignKey('books.book_id'))
)

# normal user account
class User(Base, UserMixin):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  username = Column(String(30), unique=True, nullable=False)
  password = Column(String(30), nullable=False)
  email = Column(String)
  contact_number = Column(Integer)
  verified = Column(Boolean, default=False)
  profile = Column(Integer, ForeignKey("members.member_id"), )
  is_blocked = Column(Boolean, default=False)
  role = Column(String, default="MEMBER")
  profile_picture = Column(String, nullable=True)
  date_created = Column(DateTime, default=datetime.datetime.now)
  
  
  def __str__(self) -> str:
    return f"{self.username} {self.email} {self.profile}" 
  
  def __repr__(self) -> str:
    return f"{self.username} {self.email} {self.profile}" 



# admin user 
class AdminUser(Base, UserMixin):
  __tablename__ = "admins"
  id = Column(Integer, primary_key=True)
  username = Column(String(30), nullable=False, unique=True)
  password= Column(String(128), nullable=False)
  email = Column(String(120))
  f_name = Column(String(30), nullable=False)
  last_name = Column(String(30), nullable=False)
  contact_number = Column(Integer)
  is_active = Column(Boolean, default=True)
  profile_picture = Column(String, nullable=True)
  date_created = Column(DateTime, default=datetime.datetime.now)

  
  
# book publisher model corresponding to publishers table in the database
class BookPublisher(Base):
  __tablename__ = "publishers"
  publisher_id = Column(Integer, primary_key=True)
  name = Column(String)
  date_created = Column(DateTime, default=datetime.datetime.now)

    
class Author(Base):
  __tablename__ = "authors"
  author_id = Column(Integer, primary_key=True)
  first_name = Column(String)
  last_name = Column(String)
  date_of_birth = Column(DateTime)
  # books = relationship("Book")
  date_created = Column(DateTime, default=datetime.datetime.now)

  
   
  @property 
  def full_name(self):
    return f"{self.first_name} {self.last_name}"
# book Model corresponding to books table in the database    
class Book(Base):
  __tablename__ = "books"

  book_id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  publisher = Column(String)
  published_date = Column(DateTime, default=datetime.datetime.now)
  date_created = Column(DateTime, default=datetime.datetime.now)
  category = Column(String)
  cover_photo = Column(String(250))
  isbn = Column(String)
  author = Column(String)
  status = Column(String, default=BookStatus.AVAILABLE.name)
  rating = Column(Float, default=1.0)
  views = Column(Integer, default=0)
  


#libary member
class Member(Base):
  __tablename__ = "members" 
  member_id  = Column(Integer, primary_key=True)
  first_name = Column(String)
  last_name = Column(String)
  date_of_birth = Column(DateTime, default=datetime.datetime.now)
  books = Column(Integer, ForeignKey("books.book_id"))
  
  date_created = Column(DateTime, default=datetime.datetime.now)
  
# Define the many-to-many relationship with Book for favorite books
  favorite_books = relationship("Book", secondary=favorite_books_association, backref="favorited_by")
  
  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"
  
  
  def __str__(self) -> str:
    return f"{self.first_name} {self.last_name}"
  
  def __repr__(self) -> str:
   
    return f"{self.first_name} {self.last_name}"
  
 #books that memebers have borrowed 

# borrowed books model corresponding to borrowed books table in the database
class IssuedBook(Base):
    __tablename__ = "issued_books"
    
    id = Column(Integer, primary_key=True)
    date_issued = Column(DateTime, default=datetime.datetime.now)
    return_date = Column(DateTime)
    status = Column(String, default="ISSUED")
    
    book_id = Column(Integer, ForeignKey("books.book_id"))
    member_id = Column(Integer, ForeignKey("members.member_id"))
    
    book = relationship("Book", backref="issued_books")
    member = relationship("Member", backref="issued_books")

    @property
    def due_date(self):
        return self.date_issued + datetime.timedelta(days=14)

    @property
    def formatted_due_date(self):
        return self.due_date.strftime('%Y-%m-%d')

    @property
    def formatted_issued_date(self):
        return self.date_issued.strftime('%Y-%m-%d')

    def __str__(self):
        return f"Book ID {self.book_id} borrowed by {self.member_id}"

    def __repr__(self):
        return f"<IssuedBook(book_id={self.book_id}, member_id={self.member_id})>"


class BookReview(Base):
  __tablename__ = "book_reviews"
  id = Column(Integer, primary_key=True)
  book_id = Column(Integer, ForeignKey("books.book_id"))  
  review = Column(String)
  member_id = Column(Integer, ForeignKey("members.member_id"))
  date_created = Column(DateTime, default=datetime.datetime.now)

  
  
