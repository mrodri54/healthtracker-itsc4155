from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def create_initial_user():
    # Create a user if the table is empty
    if User.query.count() == 0:  # Check if there are existing users
        new_user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(new_user)
        db.session.commit()



class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime)
    weight = db.Column(db.Float, nullable=False)  # Weight
    steps = db.Column(db.Integer, nullable=True)  # Steps walked
    calories_burned = db.Column(db.Integer, nullable=True)  # Calories burned

    # Relationship with the User model
    user = db.relationship('User', backref=db.backref('health_data', lazy=True))

    def __repr__(self):
        return f'<HealthData for {self.user.username} on {self.date}>'
    

def create_initial_health_data():
    # Checks if users and health data exists
    # user = User.query.first()
    user = User.query.get(1)
    if user and HealthData.query.count() == 0:  # Checks if health data is empty
        initial_data = HealthData(
            user_id=user.id,
            weight=145, 
            steps=8000,
            calories_burned=300
        )
        db.session.add(initial_data)
        db.session.commit()
        print("Initial health data created!")
    else:
        print("Health data already exists or no users found.")