"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from forms import CreateForm
from models import UserProfile


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/profiles/')
def profiles():
    Users = UserProfile.query.all()
    return render_template("profiles.html", users=Users)


@app.route('/profile/',methods=["GET", "POST"])
@app.route('/profile/<userid>')
def profile(userid=None):
    
    
    form = CreateForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        firstname = form.firstname.data
        lastname = form.lastname.data
        gender = form.gender.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        photo = form.photo.data
        
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        
        photoUrl = url_for('static', filename="uploads/" + filename)
        
        user = UserProfile(
            first_name=firstname,
            last_name=lastname, 
            gender=gender,
            email=email,
            location = location,
            biography=biography,
            pic = photoUrl
            )
            
        db.session.add(user)
        db.session.commit()
        flash('Successfully create profile', 'success')
        return redirect(url_for('profiles'))
        
    

    user = UserProfile.query.filter_by(id=userid).first()
    if user:
        firstname = user.first_name
        lastname = user.last_name
        gender = user.gender
        email = user.email
        location = user.location
        biography = user.biography
        pic = user.pic
        
        return render_template("profile.html", 
            firstname = firstname,
            lastname = lastname,
            gender = gender,
            email = email,
            location = location,
            biography = biography,
            pic = pic,
            userid=userid
            )
    
    
    
    
    return render_template("profile.html",form=form)


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
