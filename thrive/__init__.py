from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Create the Flask application instance
app = Flask(__name__)

# Configuration
# Secret key for session management and CSRF protection
app.config['SECRET_KEY'] = '86f8563b28d015866994bb25'
# Database configuration - using SQLite for simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thrive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: reduce overhead if not tracking modifications

# Initialize extensions
db = SQLAlchemy(app)  # Database management
bcrypt = Bcrypt(app)  # Password hashing
login_manager = LoginManager(app)  # User session management
login_manager.login_view = "login_page"  # Specify the view to redirect to for login
login_manager.login_message_category = "info"  # Flash message category for login

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from thrive.models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

# Import routes
# Note: Routes are imported here to avoid circular imports, as routes need access to 'app' and 'db'
from thrive import routes
