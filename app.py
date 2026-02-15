from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database Models
class Poll(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    question = db.Column(db.String(500), nullable=False)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.String(100), db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    votes = db.Column(db.Integer, default=0)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

# This will create poll
@app.route('/create_poll', methods=['POST'])
def create_poll():
    question = request.form.get('question')
    options = request.form.getlist('options')

    if not question or len(options) < 2:
        return "Invalid poll. Need at least 2 options."

    poll_id = str(uuid.uuid4())

    new_poll = Poll(id=poll_id, question=question)
    db.session.add(new_poll)

    for opt in options:
        if opt.strip():
            new_option = Option(poll_id=poll_id, text=opt.strip())
            db.session.add(new_option)

    db.session.commit()
    return redirect(url_for('poll_page', poll_id=poll_id))

# this is poll page
@app.route('/poll/<poll_id>')
def poll_page(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    options = Option.query.filter_by(poll_id=poll_id).all()
    return render_template('poll.html', poll=poll, options=options)

# Join socket room for real-time
@socketio.on('join_poll')
def handle_join(data):
    poll_id = data['poll_id']
    join_room(poll_id)

@app.route('/vote', methods=['POST'])
def vote():
    poll_id = request.form.get('poll_id')
    option_id = request.form.get('option_id')

    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip:
        user_ip = user_ip.split(',')[0].strip()


    existing_vote = Vote.query.filter_by(poll_id=poll_id, ip_address=user_ip).first()
    if existing_vote:
        return "You have already voted on this poll!"

    option = Option.query.get(option_id)
    if option:
        option.votes += 1
        new_vote = Vote(poll_id=poll_id, ip_address=user_ip)
        db.session.add(new_vote)
        db.session.commit()

        options = Option.query.filter_by(poll_id=poll_id).all()
        results = {opt.text: opt.votes for opt in options}
        socketio.emit('update_results', results, room=poll_id)

    return redirect(url_for('poll_page', poll_id=poll_id))

import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)

