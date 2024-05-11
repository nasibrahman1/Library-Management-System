from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):
  username = StringField("User Name", validators=[DataRequired(), Length(min=2, max=20)])
  first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=20)])
  last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
  date_of_birth = DateField("Date Of Birth", format='%Y-%m-%d')
  user_profile = FileField("Add Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
  contact_number = IntegerField("Contact Number", validators=[DataRequired()])
  submit = SubmitField("Sgin Up")


class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit_login = SubmitField("Login")
    
class AdminForm(FlaskForm):
  username = StringField("User Name", validators=[DataRequired(), Length(min=2, max=20)])
  f_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=20)])
  last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  user_profile = FileField("Add Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
  password = PasswordField("Password", validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
  date_of_birth = DateField("Date Of Birth", format='%Y-%m-%d')
  contact_number = IntegerField("Contact Number", validators=[DataRequired()])
  submit = SubmitField("Sgin Up")
  
class AdminLoginForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit_login = SubmitField("Login")
    
class BookForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired(), Length(min=3, max=50)])
  publisher = StringField("Publisher", validators=[DataRequired()])
  published_date = DateField("Published Date")
  date_created = DateField('Date Created')
  category = StringField("Category", validators=[DataRequired()])
  cover_photo = FileField("Add Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
  isbn = StringField("Isbn")
  author = StringField("author")
  status = StringField("status")
  publish = SubmitField("Publish")
  submit_book = SubmitField("Save Book")
  
class AuthorForm(FlaskForm):
  first_name = StringField("First Name", validators=[DataRequired()])
  last_name = StringField("Last Name")
  date_of_brith = DateField("Date Of Birth")
  
  
class MemberForm(FlaskForm):
  first_name = StringField("First Name", validators=[DataRequired()])
  last_name = StringField("Last Name")
  date_of_brith = DateField("Date Of Birth")
  
class IssuedBookForm(FlaskForm):
  issued_date = DateField("Issued Date")
  returned_date = DateField("Returned Date")





# featured_books = []

# f_books = []
# for book in featured_books:
#   cover_pic = str(book.cover_photo).replace("\\", "/")
#   cover_pic = cover_pic.replace("static", "")
#   cover_pic = url_for("static", filename=cover_pic)
#   book.cover_photo = cover_pic
#   f_books.append(book)
  
  
  
  
  