from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)
@views.route('/')
def base():
    return render_template('presentation.html')

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        datecita = request.form.get('datetecita')

        if len(note) < 5:
            flash('Mensaje para la cita es muy corto!', category='error')
        else:
            new_note = Note(data=note, date=datecita, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Cita Agregada!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
