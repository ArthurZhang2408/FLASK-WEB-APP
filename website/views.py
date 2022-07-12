from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('No text found!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    return render_template("message.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if first_name != current_user.first_name:
            if len(first_name) < 2:
                flash('First name is not valid.', category='error')
            else:
                User.query.get(current_user.id).first_name = first_name
                flash('First name updated!', category='success')
        if last_name != current_user.last_name:
            if len(last_name) < 2:
                flash('Last name is not valid.', category='error')
            else:
                User.query.get(current_user.id).last_name = last_name
                flash('Last name updated!', category='success')
        if check_password_hash(current_user.password, password) and password != password1:
            if len(password1) < 7:
                flash('Password must has at least 7 characters.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            else:
                User.query.get(current_user.id).password = generate_password_hash(password1, method='sha256')
                flash('Password updated!', category='success')
        db.session.commit()

    return render_template("profile.html", user=current_user)
    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    noteId = json.loads(request.data)['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')
            
    return jsonify({})