from flask import Flask, redirect, url_for, flash,render_template,request
from model import db, Student
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///namdapha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = "Namdapha_website"

db.init_app(app)
with app.app_context():
    db.create_all()

# Path to the Excel file
EXCEL_FILE_PATH = '/Volumes/Seagate/Namdapha Website/for website .xlsx'

def load_data_from_excel():
    """Load data from the Excel file and insert it into the database."""
    try:
        if os.path.exists(EXCEL_FILE_PATH):
            print(f"Excel file found at: {EXCEL_FILE_PATH}")
            
            df = pd.read_excel(EXCEL_FILE_PATH)
            print("Excel file read successfully. Here are the first few rows:")
            print(df.head())

            
            for index, row in df.iterrows():
                try:
                    print(f"Processing row {index + 1}: {row}")
                    # Create a new entry mapping Excel columns to model fields
                    new_entry = Student(
                        email=row['Student_Email'],       
                        group_number=row['GroupId'],      
                        city=row['ExamCity'],             
                        House=row['House'],               
                        
                    )
                    db.session.add(new_entry)

                except Exception as e:
                    print(f"Error adding row {index + 1}: {str(e)}")
                    continue  
            
            db.session.commit()
            print(f"Data from {EXCEL_FILE_PATH} successfully loaded into the database.")
        else:
            print(f"Excel file {EXCEL_FILE_PATH} not found.")
    
    except Exception as e:
        print(f"An error occurred while loading data from Excel: {str(e)}")

@app.route("/load-data")
def load_data():
    try:
        load_data_from_excel()
        flash('Data successfully loaded from Excel file into the database.')
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
    return redirect(url_for('home'))

@app.route("/")
def home():
    return render_template('namdapha_home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        # Debug: Print email and password received
        print(f"Received email: {email}, password: {password}")
        
        # Validate the email format
        valid_domains = ['ds.study.iitm.ac.in', 'es.study.iitm.ac.in']
        if '@' not in email:
            flash('Invalid email format')
            print('Invalid email format')
            return redirect(url_for('login'))
        
        local_part, domain = email.split('@')
        
        # Debug: Check split email parts
        print(f"Local part: {local_part}, Domain: {domain}")
        
        # Validate domain
        if domain not in valid_domains:
            flash('Invalid username or domain')
            print('Invalid username or domain')
            return redirect(url_for('login'))

        # Validate local part (assuming the format is letters followed by digits)
        if not local_part[0].isdigit() or not local_part[1:].isalnum():
            flash('Invalid username format')
            print('Invalid username format')
            return redirect(url_for('login'))
        
        # Validate that the password matches the local part of the email
        if password == local_part:
            # Check if the user exists in the database
            student = Student.query.filter_by(email=email).first()
            
            # Debug: Print if student found or not
            if student:
                print(f"Student found: {student.email}")
                flash('Login successful')
                return redirect(url_for('namdapha_home'))
            else:
                flash('User not found')
                print('User not found')
                return redirect(url_for('login'))
        else:
            flash('Invalid password')
            print('Invalid password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        group_number = request.form.get('group_number')  # Optional field
        city = request.form.get('city')  # Optional field
        house = request.form['House']

        # Create a new user entry in the database
        new_user = Student(name=name, email=email, group_number=group_number, city=city, House=house)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))  # Redirect after successful signup

    return render_template('signup.html')


# @app.route('/namdapha_home')
# def namdapha_home():
#     return render_template('namdapha_home.html')


@app.route('/council')
def council():
    return render_template('council.html')

@app.route('/art_gallery')
def art_gallery():
    return render_template('art_gallery.html')

@app.route('/photography')
def photography():
    return render_template('photography.html')


@app.route('/announcement')
def announcement():
    return render_template('announcement.html')


@app.route('/club')
def club():
    return render_template('sahyog.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)

