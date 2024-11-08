from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, create_initial_user, HealthData, create_initial_health_data
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import time
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key


#Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Interstellar101_@localhost/healthtracker'

#Initialize the Database
# db = SQLAlchemy(app)
db.init_app(app)  # Initialize db with the app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userlogin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    # This function will make 'logged_in' available in all templates
    return {'logged_in': 'user_id' in session}



# Create tables and an initial user in the database
with app.app_context():
    db.create_all()  # Create all tables
    create_initial_user() 
    create_initial_health_data()


# @app.route('/')
# def home():
#     # Query all health data for the user with id=1
#     user = User.query.get(1)  # Fetch the test user with id=1
    
#     if user:
#         health_data_list = user.health_data  # Get all health data associated with the user
#     else:
#         health_data_list = []  # If no user or no data, send an empty list

#     return render_template('index.html', health_data_list=health_data_list)

@app.route('/')
def home():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        health_data_list = user.health_data if user else []
        return render_template('index.html', health_data_list=health_data_list)
    return redirect(url_for('userlogin'))

@app.route('/userlogin')
def userlogin():
    return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         # Fetch the user from the database
#         user = User.query.filter_by(username=username).first()
        
#         # Check if user exists and password matches
#         if user and user.password == password:  # Ideally, use hashed passwords in production
#             # flash('Login successful!', 'success')
#             # time.sleep(2)
#             return redirect(url_for('home'))  # Redirect to a dashboard or another page after successful login
#         else:
#             flash('Invalid username or password', 'error') 
#             # return redirect(url_for('userlogin'))
#     return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Fetch the user from the database
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password matches
    if user and user.password == password:  # Remember to hash passwords in production
        login_user(user)  # Flask-Login's login_user function
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password', 'error')
    return redirect(url_for('userlogin'))

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logs out the user and clears the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('userlogin'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def profile():
    if request.method == 'POST':
        # Get new username and password from the form
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        # Update the user's information in the database
        if new_username:
            current_user.username = new_username
        
        if new_password:
            current_user.password = new_password  # You might want to hash the password in a real app

        db.session.commit()  # Save changes to the database
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))  # Redirect to the profile page after update
    
    # Render the profile page and pass the current user info
    return render_template('profile.html', user=current_user)

@app.route('/habit')
def habit_tracking():
    return render_template('habit.html')

@app.route('/nutrition')
def nutrition_tracking():
    return render_template('nutrition.html')

@app.route('/fitnesstracking')
def fitness_tracking():
    return render_template('fitnesstracking.html')

@app.route('/fitnessguide')
def fitness_guide():
    return render_template('fitnessguide.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
