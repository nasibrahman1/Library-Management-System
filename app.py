import sys
import os
from sqlalchemy.orm import joinedload
p = "/library/library/backend/"
sys.path.append(p)
sys.path.append("./backend/")
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, redirect, request, flash, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
from flask_login import login_user, LoginManager, logout_user, current_user
from .forms import BookForm, RegisterForm, LoginForm, AdminForm, AdminLoginForm
from .models import  Member, User, Book, IssuedBook, AdminUser

app = Flask(__name__)
app.config['SECRET_KEY'] = '850e893e780d2b552a9cdbe00b91a3b6'

DB_NAME = "sqlite:///main_library.db"  
app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
app.config["UPLOAD_FOLDER"]= "static/profile_pics"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, db)




# try:
#     with app.app_context():
#         print("FETCHING ALL BORROWED BOOKS...", end="")
#         # borrowed_books = db.session.query(IssuedBook).all()
#         print("DONE")
        
#         mmm = db.session.query(Member).all()
        
#         # print("DELETING ALL BORROWED BOOKS")
#         # for book in borrowed_books:
#         #     db.session.delete(book)
#         # print("DONE")
        
#         for m in mmm:
#             db.session.delete(m)
# except Exception as e:
    
#     print("error while trying to clear borrwoed books")
#     print(e)


# use to protect routes
def require_login(redirect_to_url="login"):
     if session.get("current_user", None) == None:
        return redirect(url_for(redirect_to_url))

     else:
         print("user is login")



@login_manager.user_loader
def load_user(user_id):
    db.session.query(User).get(int(user_id))

@app.route('/')
def home():
    return render_template("home/Hero.html", current_user=current_user)

@app.route("/all_books")
# @login_required
def all_books():
    require_login("login")
    featured_books = []
   
   
       
    if session.get("current_user", None):
        username = session["current_user"]["username"]

        user_profile = db.session.query(User).filter(User.username == username).first()
        # profile_pic = url_for("static", profile_pic=user_profile.profile_picture)
        profile_pic = str(user_profile.profile_picture).replace("\\", "/")
        profile_pic = profile_pic.replace("static", "")
        profile_pic=url_for("static", filename=profile_pic)
        
        
        try:
            featured_books = db.session.query(Book).all()
            
            f_books = []
            for book in featured_books:
                cover_pic = str(book.cover_photo).replace("\\", "/")
                cover_pic = cover_pic.replace("static", "")
                cover_pic = url_for("static", filename=cover_pic)
                book.cover_photo = cover_pic
                f_books.append(book)
                
        except:
            print("Error while trying to fetch books")
        return render_template("home/home.html", featured_books=f_books, profile_pic=profile_pic)

    return redirect(url_for("login"))
@app.route('/about')
def about():
    return render_template("about/about.html")




def save_picture(user_profile):
    success = False
    filepath = None
    try:
        filename = secure_filename(user_profile.filename)  
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        user_profile.save(filepath)
        success = True
    except Exception as e:
        print("Unable to save pci")
        print(e)
        
    
    if success:
        print("Image saved successfully....")
    return filepath
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        print("USER PROFILE",form.user_profile.data)
        
        if form.validate_on_submit():
          
            # check if username or email already exist
            if db.session.query(User).filter_by(email= form.email.data).first() \
            or db.session.query(User).filter_by(username= form.username.data).first():
                flash(f"Email or username already exists!")
            else:
                hash_and_salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
                member = Member(first_name=form.first_name.data, 
                                last_name=form.email.data, 
                                date_of_birth=form.date_of_birth.data)
                user = User(username=form.username.data, 
                            email=form.email.data, 
                            password=hash_and_salted_password, 
                            profile=member.member_id,
                            contact_number=form.contact_number.data,
                            profile_picture=save_picture(form.user_profile.data))
                db.session.add_all([member])
                db.session.commit()
                user.profile = member.member_id
                
                db.session.add(user)
                db.session.commit()
                flash(f'Account Created for {form.username.data}! successfully!', 'success')
                return redirect(url_for('login'))
        else:
            print(form.errors)    
    return render_template("/register/register.html", title='Register', form=form, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.username == form.username.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash(f"That username does not exist, please try again.", "danger")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash(f'Password incorrect, please try again.', "danger")
            return redirect(url_for('login'))
        else:
            login_user(user,remember=True )
            session["current_user"] = {"username":current_user.username, "email":current_user.email }
            return redirect(url_for('all_books'))
        
    return render_template("login.html", title='Login', form=form)



@app.route('/home/user-profile')
def user_profile():
    if session["current_user"]["username"]:
        # Accessing email only if the user is authenticated
        username = session["current_user"]["username"]

        user_profile = db.session.query(User).filter(User.username == username).first()
        # profile_pic = url_for("static", profile_pic=user_profile.profile_picture)
        profile_pic = str(user_profile.profile_picture).replace("\\", "/")
        profile_pic = profile_pic.replace("static", "")
        profile_pic=url_for("static", filename=profile_pic)

        borrowed_books = []
       
        try:
           
           borrowed_books = db.session.query(IssuedBook).filter(IssuedBook.member_id == user_profile.profile).all()
           # Retrieve favorite books for a member
           favorite_books = db.session.query(Book).join(Book.favorited_by).filter(Member.member_id == user_profile.profile).all()

           print("borrowed books: ",borrowed_books)
           print("Favorite books: ",favorite_books)
           
        except Exception as e:
            print(f"Error while trying to find borrowed book for {username}")
            print(e)
        
        return render_template('/user_profile/user-profile.html', 
                               user_profile=user_profile, 
                               profile_pic=profile_pic,
                               borrowed_books=borrowed_books, 
                               favorite_books=favorite_books)
    else:
        # Handle case where user is not authenticated
        return "User is not authenticated"
    
@app.route('/logout')
def logout():
    session.clear()
    
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    form = AdminForm()
    if request.method == "POST":
        
        if form.validate_on_submit():
            
            # check if username or email already exist
            if db.session.query(AdminUser).filter_by(email= form.email.data).first() \
            or db.session.query(AdminUser).filter_by(username= form.username.data).first():
                flash(f"Email or username already exists!")
            else:
                hash_and_salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        
                user = AdminUser(username=form.username.data,
                                f_name = form.f_name.data,
                                last_name = form.last_name.data,
                                email=form.email.data, 
                                password=hash_and_salted_password,
                                contact_number=form.contact_number.data,
                                profile_picture=save_picture(form.user_profile.data))
                db.session.add(user)
                db.session.commit()
                flash(f'Account Created for {form.username.data}! successfully!', 'success')
                return redirect(url_for('admin_login'))
    return render_template("/admin/signup.html",form=form, current_user=current_user)

@app.route('/admin-login', methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = None
        user = None
        try:
            result = db.session.execute(db.select(AdminUser).where(AdminUser.username == form.username.data))
        # Note, email in db is unique so will only have one result.
            user = result.scalar()
        except:
            print("Something went")
            
       
        # Email doesn't exist
        if not user:
            flash(f"That username does not exist, please try again.", "danger")
            return redirect(url_for('admin_login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash(f'Password incorrect, please try again.', "danger")
            return redirect(url_for('dashboard'))
        else:
            login_user(user,remember=True )
            session["current_user"] = {"username":current_user.username, "email":current_user.email }
            return redirect(url_for('dashboard'))

    return render_template("/admin/signin.html", form=form)


@app.route('/dashboard/admin-profile')
def amin_profile():
    if session["current_user"]["username"]:
        # Accessing email only if the user is authenticated
        username = session["current_user"]["username"]

        user_profile = db.session.query(AdminUser).filter(AdminUser.username == username).first()
        profile_pic = str(user_profile.profile_picture).replace("\\", "/")
        profile_pic = profile_pic.replace("static", "")
        profile_pic=url_for("static", filename=profile_pic)
        
        return render_template('/admin/profile.html', user_profile=user_profile, profile_pic=profile_pic)
    else:
        # Handle case where user is not authenticated
        return "User is not authenticated"
# delete book with given book id





#------------- DASHBOARD ROUTES -------------




# base dashboard page
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    require_login("admin_login")
    
    new_members = []
    recent_borrowed_books = []
    recent_returned_books = []
    total_books = 0
    total_members = 0
    total_borrowed_books = 0
    returned_this_week = 0
    try:
        total_books = len(db.session.query(Book).all())
        all_members = db.session.query(Member).all()
        total_members = len(all_members)
        new_members = all_members[:10]
        recent_borrowed_books = db.session.query(IssuedBook).all()
        total_borrowed_books = len(recent_borrowed_books)
        recent_returned_books = db.session.query(IssuedBook).filter(IssuedBook.status == "RETURNED").all()
        returned_this_week = len(recent_returned_books)
    except Exception as e:
       print("Error while trying to get data from db")
       print(e)
    
    return render_template("/dashboard/index.html",
                           total_books=total_books,
                           total_members=total_members,
                           total_borrowed_books=total_borrowed_books,
                           returned_this_week=returned_this_week,
                           new_members=new_members,
                           recent_borrowed_books=recent_borrowed_books,
                           recent_returned_books=recent_returned_books
                           )


@app.route("/dashboard/members")
def list_members():
    member_list =[]
    try:
        user_list = db.session.query(User).all()
        member_list = db.session.query(Member).all()
        print("All members", user_list)
    except:
        pass
    return render_template("/dashboard/manage-user.html", member_list=member_list, user_list=user_list)

@app.route("/dashboard/members/add-member")
def add_members():
    return render_template("/dashboard/manage-user.html")


@app.route("/dashboard/members/approve")
def approve_members():
    return render_template("/dashboard/members-approve.html")

@app.route("/dashboard/members/delete/<int:member_id>")
def delete_member(member_id):
   try:
       print(f"Trying to delete member with id: {member_id}", end="")
       member_to_delete = db.session.query(Member).filter(Member.member_id==member_id).first()
       if member_to_delete:
           db.session.delete(member_to_delete)
           db.session.commit()
           print(" ....DONE")
   except:
       print("FAILED")
    
   return redirect(url_for("list_members"))    


# manage books route
@app.route("/dashboard/books/")
def list_books():
    require_login("admin_login")

    books = []
   
    try:
       books = db.session.query(Book).all()
    except:
        print("error while trying to fetch books")
      
    
    return render_template("/dashboard/all-books.html", book_list=books)

# add new book to library
@app.route("/dashboard/books/add-book/", methods=["GET", "POST"])
def add_book():
    require_login("admin_login")


    form = BookForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # print("Form DATA: ", form.data)
                # print("Book Form DATA", form.data)
                book = Book(title=form.title.data,
                            author=form.author.data, 
                            publisher=form.publisher.data,
                            category=form.category.data,
                            isbn=form.isbn.data,
                            cover_photo=save_picture(form.cover_photo.data)
                            )
                db.session.add(book)
                db.session.commit()
                print("Book Saved Successfully")
                flash("Book added successfully", "success")
                return redirect(url_for("list_books"))
            except Exception as e:
                print("ADD BOOK: error while trying to add book to db")
                print(e)
        else:
            print("Form data is not valid")
            print(form.errors)
            flash("There are errors in the form", "error")        
        
    return render_template("/dashboard/add-book.html", form=form)

# edit book details
@app.route("/dashboardbooks/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = None
    form = BookForm()
    if request.method == "POST":
        try:
           updated_book = db.session.get(Book, book_id)
           if updated_book:
               updated_book.title = form.title.data
               updated_book.author = form.author.data
               updated_book.publisher = form.publisher.data
               updated_book.isbn = form.isbn.data
               updated_book.category = form.category.data
               updated_book.cover_photo = save_picture(form.cover_photo.data)
               
               db.session.add(updated_book)
               db.session.commit()
               print("Book details updated successfully")
               flash("Book details updated successfully", "success")
               return redirect(url_for("list_books"))
       
           else:
               print(f"Could not find book with given id {book_id}")
        except Exception as e:
            print("Error while trying to update book details")
            print(e)
        return render_template("/dashboard/edit-book.html", form=form)


    try:
       book = db.session.get(Book, book_id)
       form = BookForm(     title=book.title,
                            author=book.author, 
                            publisher=book.publisher,
                            category=book.category,
                            isbn=book.isbn,
                            cover_photo=book.cover_photo,
                       )
       print("Prepopulated form", form)
    except:
        print(f"EDIT BOOK: Soemthing went wrong while fetching book with id {book_id}")

    return render_template("/dashboard/edit-book.html", form=form)

# view details of a given book
@app.route("/dashboard/books/view/<int:book_id>")
def view_book(book_id):
    book = None
    try:
        book = db.session.get(Book, book_id)
    except:
        print(f"VIEW BOOK: Soemthing went wrong while fetching book with id {book_id}")
        
    return render_template("/dashboard/book-detail.html", book=book)

# delete book with given book id
@app.route("/dashboard/books/delete/<int:book_id>")
def delete_book(book_id):
    book_to_delete = None
    
    try:
        book_to_delete = db.session.get(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        print("Book deleted successfully")
        flash(f"Book with id {book_id} deleted successfully")
    except:
        print(f"DELETE BOOK: Soemthing went wrong while fetching book with id {book_id}")
        
    return redirect(url_for("list_books"))



# list borrowed books
@app.route("/dashboard/borrowed-books")
def borrowed_book():
    issued_books_query = [
        
    ]
    
    try:
        # fetch all borrowed books
        issued_books_query = db.session.query(IssuedBook).options(joinedload(IssuedBook.book), joinedload(IssuedBook.member)).all()
        # print("borrowed books: ", issued_books_query[0].book.title)
    except Exception as e:
        print("error while feching borrowed books", e)
    
    return render_template("/dashboard/borrowed-books.html", borrowed_books=issued_books_query)

@app.route("/dashboard/borrowed-books/delete/<int:book_id>", methods=["GET", "POST"])
def delete_borrowed_book(book_id):
    try:
        book_to_delete = db.session.get(IssuedBook, book_id)
        if book_to_delete:
            db.session.delete(book_to_delete)
            db.session.commit()
            
            return redirect(url_for("borrowed_book"))
    except:
        pass
    
    return redirect(url_for("borrowed_book"))


# list borrowed books
@app.route("/dashboard/returned-books")
def returned_book():
    returned_books = [
         {
        "book_id":1,
        "title":"Soul",
        "due_date":"12-12-2024",
        "date_issued":"11-12-2024",
        "member":"Awet Thon"
    }
    ]
    try:
        returned_books = db.session.query(IssuedBook).all() 
    except:
        pass
    
    return render_template("/dashboard/returned-books.html", returned_books=returned_books)

@app.route("/dashboard/mange-book")
def manage_book():
    return "Manage book"


#borrow book
@app.route("/books/borrow/<int:book_id>", methods=["POST", "GET"])
def borrow_book(book_id):
    success= False
    try:
        book = db.session.get(Book,book_id)
        username = session["current_user"]["username"] or ""
        user = db.session.query(User).filter(User.username == username).first()
        if user:
           
            member = db.session.query(Member).filter(Member.member_id == user.profile).first()
            
            if member:
                print(f"Found member profile for {username}")
                issue_book = IssuedBook(book_id=book.book_id, member_id=member.member_id)
                
                db.session.add(issue_book)
                db.session.commit()
                print(f"Book Issued to {username} successfully")
                success = True
    except Exception as e:
        print(f"Failed to issue book to {username}")
        print(e)
        success = False
    
    return redirect(url_for("all_books"))
  
  
@app.route("/borrowed-books/return/<int:book_id>")    
def return_borrowed_book(book_id):
    success = False
    try:
       username = session["current_user"]["username"]
       
       if username:
           user = db.session.query(User).filter(User.username==username).first()
           
           if user:
               book_to_return = db.session.query(IssuedBook).filter(Book.book_id==book_id).first()
               
               if book_to_return:
                   
                  
                   db.session.delete(book_to_return)
                   print(f" Book titled {book_to_return.book.title} has been returned by {username}")
                   db.session.commit()
    except:
        print("Unable to return book")
    
    return redirect(url_for("all_books"))



@app.route("/favourite/<int:book_id>")
def mark_book_favourite(book_id):
    success = False
    try:
        username = session["current_user"]["username"]
        user = db.session.query(User).filter(User.username == username).first()
        
        print(user)
        if user: 
            
            member = db.session.query(Member).filter(Member.member_id == user.profile).first()
            print("USER PROFILE ID: ", user.profile)
            if member:
                
                book = db.session.get(Book, book_id)
                if book:
                    
                    member.favorite_books.append(book)
                    db.session.add(member)
                    db.session.commit()
                    success = True
                    print(f"{username} marked {book.title} as favourite")
                else:
                    print("Could not find book")    
            else:
                print("could not find member")    
        else:
            print(f"Failed to fetch user with {username}")    
    except Exception as e:
        print("Failed to mark book as favourite")
        print(e)
    
    
    return redirect(url_for("all_books"))  
    

@app.route("/unfavourite/<int:book_id>", methods=["GET", "POST"])
def remove_book_from_favourite(book_id):
    success = False
    try:
        username = session["current_user"]["username"]
        user = db.session.query(User).filter(User.username == username).first()
        
        print(user)
        if user: 
            
            member = db.session.query(Member).filter(Member.member_id == user.profile).first()
            print("USER PROFILE ID: ", user.profile)
            if member:
                
                book = db.session.get(Book, book_id)
                if book:
                    
                    member.favorite_books.remove(book)
                    db.session.add(member)
                    db.session.commit()
                    success = True
                    print(f"{username} marked {book.title} as favourite")
                else:
                    print("Could not find book")    
            else:
                print("could not find member")    
        else:
            print(f"Failed to fetch user with {username}")    
    except Exception as e:
        print("Failed to remove book from favourite")
        print(e)
    
    
    return redirect(url_for("user_profile")) 



@app.route("/books/view/<int:book_id>")
def show_book_details(book_id):
    book = None
    try:
        book = db.session.get(Book, book_id)
        cover_photo = str(book.cover_photo).replace("\\", "/")
        cover_photo = cover_photo.replace("static", "")
        cover_photo=url_for("static", filename=cover_photo)
        book.cover_photo = cover_photo

        
    except:
        print(f"VIEW BOOK: Soemthing went wrong while fetching book with id {book_id}")
        
    return render_template("book-detail.html", book=book)


# run this function only once to create all db tables
def create_all_tables():
    from .models import Base
    
    try:
        with app.app_context():
            print("tyring to create tables...", end="")
            Base.metadata.create_all(db.engine)
            print("DONE")
    except Exception as e:
        print("FAILED")
        print("Error: ==", e)


create_all_tables()
with app.app_context():
    print("initializing db...", end="")
    db.create_all()
    print("DONE")
if __name__ == "__main__":
    app.run(debug=True)



