from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def create_initial_user():
    # Create a user if the table is empty
    if User.query.count() == 0:  # Check if there are existing users
        new_user = User(username='testuser', email='test@example.com', password='testpassword', first_name="testfirst", last_name="testlast")
        db.session.add(new_user)
        db.session.commit()



class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    weight = db.Column(db.Float, nullable=False)  # Weight
    steps = db.Column(db.Integer, nullable=True)  # Steps walked
    # calories_burned = db.Column(db.Integer, nullable=True)  # Calories burned

    calories_intake = db.Column(db.Integer, nullable=True)  # Calories consumed
    workouts = db.Column(db.Integer, nullable=True)  # Number of workouts in a day
    sleep_hours = db.Column(db.Float, nullable=True)  # Sleep time in hours
    screen_time = db.Column(db.Float, nullable=True)  # Screen time in hours


    # Relationship with the User model
    user = db.relationship('User', backref=db.backref('health_data', lazy=True))

    def __repr__(self):
        return f'<HealthData for {self.user.username} on {self.date}>'
    

# def create_initial_health_data():
#     # Checks if users and health data exists
#     # user = User.query.first()
#     user = User.query.get(1)
#     if user and HealthData.query.count() == 0:  # Checks if health data is empty
#         initial_data = HealthData(
#             user_id=user.id,
#             weight=145, 
#             steps=8000,
#             calories_intake=2200,
#             workouts=2,
#             sleep_hours=7.5,
#             screen_time=5.0
#              # calories_burned=300
#         )
#         db.session.add(initial_data)
#         db.session.commit()
#         print("Initial health data created!")
#     else:
#         print("Health data already exists or no users found.")

def create_initial_health_data():
    user = User.query.get(1)  # Get the first user with ID 1
    if user:
        # Fetch the existing health data for the user
        health_data = HealthData.query.filter_by(user_id=user.id).first()
        
        if health_data:  # If health data exists, update it
            health_data.weight = 145
            health_data.steps = 8000
            health_data.calories_intake = 2200
            health_data.workouts = 2
            health_data.sleep_hours = 7.5
            health_data.screen_time = 5.0
            # Remove or update 'calories_burned' if necessary
            # health_data.calories_burned = 300  # If this column still exists and you want to modify it
            
            db.session.commit()  # Commit the changes
            print("Health data for user updated!")
        else:  # If no health data exists, create it
            initial_data = HealthData(
                user_id=user.id,
                weight=145, 
                steps=8000,
                calories_intake=2200,
                workouts=2,
                sleep_hours=7.5,
                screen_time=5.0
            )
            db.session.add(initial_data)
            db.session.commit()
            print("Initial health data created!")
    else:
        print("No user found.")