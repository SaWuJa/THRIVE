from flask import render_template, redirect, url_for, flash
from thrive import app, db
from thrive.models import Project, User  # Updated import to include Project instead of Item
from thrive.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required
from thrive.forms import ProjectForm
from flask_login import current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/projects')  # Renamed from /thrive to /projects
@login_required
def projects_page():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)  # Updated template name and variable

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)  # Assume you have a method to hash the password
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash("Account created successfully! You are now able to log in.", category='success')
        return redirect(url_for('projects_page'))  # Redirect to the projects page after registration
    if form.errors != {}:
        for err_msgs in form.errors.values():
            for err_msg in err_msgs:
                flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('projects_page'))  # Redirect to the projects page after login
        else:
            flash('Username and password do not match! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home_page'))


@app.route('/add_project', methods=['GET', 'POST'])
@login_required  # Ensure only authenticated users can add projects
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Project(
        project_name=form.project_name.data,
        description=form.description.data,
        user_id=current_user.id  # Assign the current logged-in user's ID
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('projects_page'))
    return render_template('add_project.html', title='New Project', form=form)
