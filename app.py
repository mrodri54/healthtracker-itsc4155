import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI plotting
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User, create_initial_user, HealthData, create_initial_health_data
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import time
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  


#Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysqlpassword1@localhost/healthtracker'

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
    # This function will make 'logged_in' available in all pages
    return {'logged_in': 'user_id' in session}

# Create tables and an initial user in the database
with app.app_context():
    db.create_all()  # Create all tables
    create_initial_user() 
    create_initial_health_data()

@app.route('/')
def home():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        health_data_list = user.health_data if user else []
        today_date = datetime.now().strftime('%Y-%m-%d')
        return render_template('index.html', health_data_list=health_data_list, today_date=today_date)
    return redirect(url_for('userlogin'))

@app.route('/userlogin')
def userlogin():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Fetch the user from the database
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password matches
    if user and check_password_hash(user.password, password) or user and user.password == password: 
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

        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')


        # Update the user's information in the database
        if new_username:
            current_user.username = new_username
        
        if new_password:
            current_user.password = hashed_password  

        db.session.commit()  # Save changes to the database
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))  # Redirect to the profile page after update
    
    # Render the profile page and pass the current user info
    return render_template('profile.html', user=current_user)


@app.route('/add_health_data', methods=['POST'])
@login_required
def add_health_data():
    # Get form data including date
    date_str = request.form.get('date')
    print(f"Received date from form: {date_str}")  # Debug print
    
    date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.now()
    print(f"Parsed date: {date}")  # Debug print
    
    weight = request.form.get('weight', type=float)
    steps = request.form.get('steps', type=int)
    calories_intake = request.form.get('calories_intake', type=int)
    workouts = request.form.get('workouts', type=int)
    sleep_hours = request.form.get('sleep_hours', type=float)
    screen_time = request.form.get('screen_time', type=float)

    # Create a new record with the specified date
    new_data = HealthData(
        user_id=current_user.id,
        date=date,  # Use the date from the form
        weight=weight,
        steps=steps,
        calories_intake=calories_intake,
        workouts=workouts,
        sleep_hours=sleep_hours,
        screen_time=screen_time
    )
    db.session.add(new_data)
    db.session.commit()

    return redirect(url_for('home'))  # Redirect to a dashboard or another page


@app.route('/habit')
@login_required
def habit_tracking():
    # Fetch the health data for the logged-in user
    user = current_user
    health_data = HealthData.query.filter_by(user_id=user.id).all()

    # Extract dates, sleep hours, and screen time data
    dates = [data.date.strftime('%Y-%m-%d') for data in health_data]
    sleep_hours = [data.sleep_hours for data in health_data if data.sleep_hours is not None]
    screen_time = [data.screen_time for data in health_data if data.screen_time is not None]

    # Check if data is available
    if not sleep_hours or not screen_time:
        return render_template('habit.html', msg="No data available.")

    # Create the first graph (Sleep Hours)
    fig, (ax1) = plt.subplots(figsize=(10, 5))
    ax1.plot(dates, sleep_hours, color='b', marker='o', linestyle='-', label='Sleep Hours')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sleep Hours')
    ax1.set_title(f'Sleep Log for {user.username}')
    plt.xticks(rotation=45)

    # Save the Sleep Log graph to a BytesIO object and encode in base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    sleep_graph_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the first plot

    # Create the second graph (Screen Time)
    fig, (ax2) = plt.subplots(figsize=(10, 5))
    ax2.plot(dates, screen_time, color='r', marker='s', linestyle='-', label='Screen Time')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Screen Time (hours)')
    ax2.set_title(f'Screen Time Tracker for {user.username}')
    plt.xticks(rotation=45)

    # Save the Screen Time graph to a BytesIO object and encode in base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    screen_time_graph_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the second plot

    # Render the 'habit.html' template with the encoded graphs
    return render_template('habit.html', 
                           sleep_graph=sleep_graph_base64, 
                           screen_time_graph=screen_time_graph_base64)


@app.route('/nutrition')
@login_required  # Ensure the user is logged in
def nutrition_tracking():
    # Get the current user from Flask-Login
    user = current_user
    
    # Query the HealthData model to get the calories intake for this user
    health_data = HealthData.query.filter_by(user_id=user.id).all()
    
    # Extract dates and calories data
    dates = [data.date.strftime('%Y-%m-%d') for data in health_data]
    calories = [data.calories_intake for data in health_data]

    # If no data is found, return an empty plot
    if not health_data:
        return render_template('nutrition.html', img_base64=None, message="No data available for this user.")

    # Create the bar plot
    fig, ax = plt.subplots()
    ax.bar(dates, calories, color='skyblue')

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Calories Consumed')
    ax.set_title(f'Calories Intake for {user.username}')

    # Rotate date labels for better readability
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image in base64 to display it in the HTML
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # Pass the base64 encoded image and any other necessary data to the template
    return render_template('nutrition.html', img_base64=img_base64)


@app.route('/fitnesstracking')
@login_required  # Ensure the user is logged in
def fitness_tracking():
    # Get the current user from Flask-Login
    user = current_user

    # Query the HealthData model to get the steps and workout performance data for this user
    health_data = HealthData.query.filter_by(user_id=user.id).all()

    # Extract dates, steps, and workouts data
    dates = [data.date.strftime('%Y-%m-%d') for data in health_data]
    steps = [data.steps for data in health_data]
    workouts = [data.workouts for data in health_data]

    # If no data is found, return empty plots
    if not health_data:
        return render_template('fitnesstracking.html', steps_img_base64=None, workouts_img_base64=None, message="No data available for this user.")

    # Step Tracker Graph (Steps over time)
    fig1, ax1 = plt.subplots()
    ax1.plot(dates, steps, marker='o', color='skyblue', label='Steps', linestyle='-', linewidth=2)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Steps')
    ax1.set_title(f'Step Tracker for {user.username}')
    ax1.set_xticklabels(dates, rotation=45)
    ax1.legend()

    # Workout Performance Graph (Workouts over time)
    fig2, ax2 = plt.subplots()
    ax2.plot(dates, workouts, marker='s', color='orange', label='Workouts', linestyle='-', linewidth=2)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Workouts')
    ax2.set_title(f'Workout Performance for {user.username}')
    ax2.set_xticklabels(dates, rotation=45)
    ax2.legend()

    # Save the plots to BytesIO objects
    img1 = io.BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    steps_img_base64 = base64.b64encode(img1.getvalue()).decode('utf-8')

    img2 = io.BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    workouts_img_base64 = base64.b64encode(img2.getvalue()).decode('utf-8')

    # Pass the base64 encoded images to the template
    return render_template('fitnesstracking.html', 
                           steps_img_base64=steps_img_base64,
                           workouts_img_base64=workouts_img_base64)

@app.route('/fitnessguide')
def fitness_guide():
    return render_template('fitnessguide.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('userlogin'))
        
        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Create a new user, including the username
        new_user = User(username=username, email=email, password=hashed_password, 
                        first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('userlogin'))

    return render_template('signup.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/update_habit_graph')
@login_required
def update_habit_graph():
    graph_type = request.args.get('type')
    timeframe = request.args.get('timeframe')
    
    # Get data with proper date filtering
    end_date = datetime.now()
    if timeframe == 'daily':
        # Set start_date to the beginning of today (midnight)
        start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        # Set end_date to the end of today
        end_date = start_date + timedelta(days=1)
    elif timeframe == 'weekly':
        start_date = end_date - timedelta(weeks=1)
    else:  # monthly
        start_date = end_date - timedelta(days=30)

    data = HealthData.query.filter(
        HealthData.user_id == current_user.id,
        HealthData.date.between(start_date, end_date)
    ).order_by(HealthData.date).all()

    try:
        # Query data based on graph type
        dates = [d.date for d in data]
        if graph_type == 'sleep':
            values = [d.sleep_hours for d in data if d.sleep_hours is not None]
            title = 'Sleep Log - Today' if timeframe == 'daily' else f'Sleep Log ({timeframe.capitalize()} View)'
            ylabel = 'Sleep Hours'
            color = 'b'
            marker = 'o'
        elif graph_type == 'screen':
            values = [d.screen_time for d in data if d.screen_time is not None]
            title = 'Screen Time - Today' if timeframe == 'daily' else f'Screen Time ({timeframe.capitalize()} View)'
            ylabel = 'Screen Time (hours)'
            color = 'r'
            marker = 's'
        else:
            return jsonify({'success': False, 'error': 'Invalid graph type'})

        if not values:
            return jsonify({'success': False, 'error': 'No data available for today'})

        # Create the plot
        plt.figure(figsize=(10, 5))
        if timeframe == 'daily':
            # For daily view, use a single bar
            plt.bar(['Today'], values[-1], color=color, alpha=0.7)  # Just show the latest value
            plt.ylim(0, max(values[-1] * 1.2, 1))  # Set y-axis limit with some padding
        else:
            plt.plot(dates, values, color=color, marker=marker, linestyle='-')
            plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)

        # Add labels and title
        plt.title(title)
        plt.xlabel('Date' if timeframe != 'daily' else 'Time')
        plt.ylabel(ylabel)
        plt.grid(True)

        # Save plot to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Convert to base64
        graph_base64 = base64.b64encode(buf.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'graph': graph_base64
        })

    except Exception as e:
        print(f"Error generating graph: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/update_fitness_graph')
@login_required
def update_fitness_graph():
    graph_type = request.args.get('type')
    timeframe = request.args.get('timeframe')
    
    # Get data with proper date filtering
    end_date = datetime.now()
    if timeframe == 'daily':
        start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif timeframe == 'weekly':
        start_date = end_date - timedelta(weeks=1)
    else:  # monthly
        start_date = end_date - timedelta(days=30)

    data = HealthData.query.filter(
        HealthData.user_id == current_user.id,
        HealthData.date.between(start_date, end_date)
    ).order_by(HealthData.date).all()

    try:
        dates = [d.date for d in data]
        if graph_type == 'steps':
            values = [d.steps for d in data if d.steps is not None]
            title = 'Step Tracker - Today' if timeframe == 'daily' else f'Step Tracker ({timeframe.capitalize()} View)'
            ylabel = 'Steps'
            color = 'skyblue'
            marker = 'o'
        elif graph_type == 'workouts':
            values = [d.workouts for d in data if d.workouts is not None]
            title = 'Workout Performance - Today' if timeframe == 'daily' else f'Workout Performance ({timeframe.capitalize()} View)'
            ylabel = 'Number of Workouts'
            color = 'orange'
            marker = 's'
        else:
            return jsonify({'success': False, 'error': 'Invalid graph type'})

        if not values:
            return jsonify({'success': False, 'error': 'No data available'})

        plt.figure(figsize=(10, 5))
        if timeframe == 'daily':
            plt.bar(['Today'], values[-1], color=color, alpha=0.7)
            plt.ylim(0, max(values[-1] * 1.2, 1))
        else:
            plt.plot(dates, values, color=color, marker=marker, linestyle='-')
            plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)

        plt.title(title)
        plt.xlabel('Date' if timeframe != 'daily' else '')
        plt.ylabel(ylabel)
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        graph_base64 = base64.b64encode(buf.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'graph': graph_base64
        })

    except Exception as e:
        print(f"Error generating graph: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5001, debug=True, threaded=False)
