import os
from flask import Flask, redirect, url_for, render_template, flash, request
from flask_dance.contrib.github import make_github_blueprint, github
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_session import Session
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
# Use SQLite for development, PostgreSQL for production
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///processlens.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize extensions
db = SQLAlchemy(app)
Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# GitHub OAuth configuration
github_blueprint = make_github_blueprint(
    client_id=os.environ.get('GITHUB_CLIENT_ID'),
    client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
    scope='read:user'
)
app.register_blueprint(github_blueprint, url_prefix='/login')

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    github_username = db.Column(db.String(80), unique=True, nullable=False)
    github_id = db.Column(db.Integer, unique=True, nullable=False)
    access_token = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.github_username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('github.login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/login/authorized')
def github_authorized():
    if not github.authorized:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ), 'error')
        return redirect(url_for('index'))
    
    resp = github.get('/user')
    if resp.ok:
        user_info = resp.json()
        
        # Check if user exists in database
        user = User.query.filter_by(github_id=user_info['id']).first()
        
        if not user:
            # Create new user
            user = User(
                github_username=user_info['login'],
                github_id=user_info['id'],
                access_token=github_blueprint.session['oauth_token']['access_token']
            )
            db.session.add(user)
            db.session.commit()
            flash('Welcome! Your account has been created.', 'success')
        else:
            # Update existing user's access token
            user.access_token = github_blueprint.session['oauth_token']['access_token']
            user.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Welcome back!', 'success')
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    flash('Failed to get user info from GitHub.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 