import os
import json
import calendar
from datetime import date, timedelta
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from pywebpush import webpush, WebPushException
from sqlalchemy import or_

# Import task list
try:
    from tasks_config import CHORES_LIST
except ImportError:
    CHORES_LIST = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fisi_household_2025_eda_melih'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- WEB PUSH CONFIGURATION ---
VAPID_PRIVATE_KEY = 'GHJmR13gRLLDo20Dva7JS0gEWt1Ouh6zxdE40WCn-MI'
VAPID_PUBLIC_KEY = 'BHwZKcVFY444SFryBOpayC7nYlfLzSrY-sA_A9XbNr6yH-DeLdWqwfwST1tvaPl2IY32iZhZu2m3Rjnmr2Av8l4'
VAPID_CLAIMS = {"sub": "mailto:eda_melih@example.com"}

# --- DATABASE MODELS ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)

class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    is_personal = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='room', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    interval_value = db.Column(db.Integer, default=1)
    interval_type = db.Column(db.String(10), default='days')
    points_worth = db.Column(db.Integer, default=10)
    last_done = db.Column(db.Date, default=lambda: date.today() - timedelta(days=1))
    list_id = db.Column(db.Integer, db.ForeignKey('task_list.id'))
    is_personal = db.Column(db.Boolean, default=False)
    for_user = db.Column(db.String(20), default='Both')

class TaskLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_done = db.Column(db.Date, default=date.today)

# --- HELPER FUNCTIONS ---

def get_next_due(task):
    return task.last_done + timedelta(days=task.interval_value)

# --- ROUTES ---

@app.route('/')
def index():
    today = date.today()
    
    # 1. Daten laden (Nur Haushalt!)
    # Wir filtern direkt in der Datenbank nach is_personal=False
    all_tasks = Task.query.filter_by(is_personal=False).all()
    users = User.query.all()
    
    # NUR Räume laden, die NICHT als personal markiert sind
    # (Das behebt dein Dropdown-Problem)
    filtered_rooms_db = TaskList.query.filter_by(is_personal=False).all()
    
    # 2. Raum-Reihenfolge definieren und sortieren
    room_order = ["General", "Kitchen", "Living Room", "Bedroom", "Bathroom", "Hallway", "Office"]
    rooms = sorted(filtered_rooms_db, key=lambda r: room_order.index(r.name) if r.name in room_order else 999)
    
    # 3. Aktiven User bestimmen
    active_user_id = session.get('user_id')
    active_user = User.query.get(active_user_id) if active_user_id else User.query.first()
    
    # 4. Filter: Nur fällige Aufgaben (Personal ist durch Schritt 1 schon weg)
    todo_tasks = [t for t in all_tasks if get_next_due(t) <= today]
    
    return render_template('index.html', 
                           tasks=todo_tasks, 
                           rooms=rooms, 
                           users=users, 
                           active_user=active_user)

@app.route('/switch_user/<int:user_id>')
def switch_user(user_id):
    session['user_id'] = user_id
    return redirect(url_for('index'))

# --- ANPASSUNG COMPLETE ROUTE ---
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    from_page = request.args.get('from_page', 'index')
    active_user_id = session.get('user_id')
    user = User.query.get(active_user_id) if active_user_id else User.query.first()
    
    if user:
        # Haushalt-Punkte nur bei Nicht-Personal Aufgaben
        if not task.is_personal:
            user.points += task.points_worth
        
        db.session.add(TaskLog(task_id=task.id, user_id=user.id, date_done=date.today()))
        task.last_done = date.today()
        db.session.commit()
    
    return redirect(url_for(from_page))

@app.route('/scoreboard')
def scoreboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template('scoreboard.html', users=users)

@app.route('/history')
def history():
    today = date.today()
    
    view_mode = request.args.get('view_mode', 'monthly')
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))
    selected_room_id = request.args.get('room_id')
    selected_task_id = request.args.get('task_id')
    
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    rooms = TaskList.query.all()
    current_room_tasks = []
    query = TaskLog.query
    
    if selected_task_id and selected_task_id != "all":
        task = Task.query.get(selected_task_id)
        if task:
            query = query.filter_by(task_id=task.id)
            current_room_tasks = Task.query.filter_by(list_id=task.list_id).all()
    elif selected_room_id:
        room = TaskList.query.get(selected_room_id)
        if room:
            current_room_tasks = room.tasks
            task_ids = [t.id for t in room.tasks]
            query = query.filter(TaskLog.task_id.in_(task_ids))

    all_logs = query.all()
    log_dates = [log.date_done for log in all_logs]

    history_data = []
    
    if view_mode == 'yearly':
        for m in range(1, 13):
            num_days = calendar.monthrange(year, m)[1]
            days = []
            for d in range(1, num_days + 1):
                d_obj = date(year, m, d)
                # Speichere Datum und Wochentag (0=Mo, 6=So)
                days.append({'date': d_obj, 'weekday': d_obj.weekday()})
                
            history_data.append({
                'month_name': f"{month_names[m-1]} {year}",
                'days': days
            })
        view_title = f"Yearly Overview {year}"
    else:
        num_days = calendar.monthrange(year, month)[1]
        days = []
        for d in range(1, num_days + 1):
            d_obj = date(year, month, d)
            days.append({'date': d_obj, 'weekday': d_obj.weekday()})
            
        history_data.append({
            'month_name': f"{month_names[month-1]} {year}",
            'days': days
        })
        view_title = f"Monthly View: {month_names[month-1]} {year}"

    total_count = len([d for d in log_dates if d.year == year])

    return render_template('calendar.html', 
                           history_data=history_data,
                           view_mode=view_mode,
                           year=year,
                           month=month,
                           month_names=month_names,
                           rooms=rooms, 
                           current_room_tasks=current_room_tasks,
                           logs=log_dates, 
                           selected_task_id=selected_task_id, 
                           selected_room_id=selected_room_id,
                           view_title=view_title,
                           total_count=total_count)

# --- NEUE ROUTE: PERSONAL TASKS ---
@app.route('/personal')
def personal_tasks():
    from sqlalchemy import extract, or_
    import calendar
    
    today = date.today()
    active_user_id = session.get('user_id')
    user = User.query.get(active_user_id) if active_user_id else User.query.first()
    
    # Filter aus der URL holen
    selected_filter = request.args.get('filter', 'all')
    
    # NEU: Monat und Jahr für den Kalender-Filter (Standard: Aktueller Monat)
    view_month = int(request.args.get('month', today.month))
    view_year = int(request.args.get('year', today.year))
    
    # 1. Aufgaben-Abfrage
    query = Task.query.filter(
        Task.is_personal == True,
        or_(Task.for_user == user.username, Task.for_user == 'Both')
    )
    all_personal_tasks = query.all()
    personal_task_ids = [t.id for t in all_personal_tasks]

    # 2. Aufgaben filtern (Daily, Weekly, etc.)
    if selected_filter == 'daily':
        display_tasks = [t for t in all_personal_tasks if t.interval_value == 1]
    elif selected_filter == 'weekly':
        display_tasks = [t for t in all_personal_tasks if 1 < t.interval_value <= 7]
    elif selected_filter == 'longer':
        display_tasks = [t for t in all_personal_tasks if t.interval_value > 7]
    elif selected_filter == 'bonus':
        display_tasks = [t for t in all_personal_tasks if t.interval_value == 0]
    else:
        display_tasks = all_personal_tasks

    # 3. Kalender-Logs für den GEWÄHLTEN Monat laden
    logs = TaskLog.query.filter(
        TaskLog.user_id == user.id,
        TaskLog.task_id.in_(personal_task_ids),
        extract('month', TaskLog.date_done) == view_month,
        extract('year', TaskLog.date_done) == view_year
    ).all()
    log_dates = [log.date_done for log in logs]

    # Tage für den gewählten Monat generieren
    num_days = calendar.monthrange(view_year, view_month)[1]
    days_in_month = []
    for d in range(1, num_days + 1):
        curr = date(view_year, view_month, d)
        days_in_month.append({'date': curr, 'weekday': curr.weekday()})

    # Stats berechnen
    personal_points = db.session.query(func.sum(Task.points_worth)).join(TaskLog).filter(
        TaskLog.user_id == user.id, Task.is_personal == True
    ).scalar() or 0

    return render_template('personal.html', 
                           tasks=display_tasks, user=user, points=personal_points,
                           days=days_in_month, logs=log_dates, 
                           selected_filter=selected_filter, today=today,
                           view_month=view_month, view_year=view_year,
                           month_names=list(calendar.month_name)[1:])

@app.route('/profile/<username>')
def profile(username):
    from sqlalchemy import extract, or_
    import calendar
    
    user = User.query.filter_by(username=username).first_or_404()
    today = date.today()
    
    # Filter aus der URL holen
    view_month = int(request.args.get('month', today.month))
    view_year = int(request.args.get('year', today.year))
    selected_room_id = request.args.get('room_id', 'all') # 'all', 'personal' oder die ID eines Raums

    # 1. Basis-Punkte berechnen
    h_pts = user.points
    p_pts = db.session.query(func.sum(Task.points_worth)).join(TaskLog).filter(
        TaskLog.user_id == user.id, Task.is_personal == True
    ).scalar() or 0

    # 2. Kalender-Logs filtern
    query = TaskLog.query.filter(
        TaskLog.user_id == user.id,
        extract('month', TaskLog.date_done) == view_month,
        extract('year', TaskLog.date_done) == view_year
    )

    # Filter nach Raum oder Personal anwenden
    if selected_room_id == 'personal':
        query = query.join(Task).filter(Task.is_personal == True)
    elif selected_room_id != 'all':
        query = query.join(Task).filter(Task.list_id == int(selected_room_id), Task.is_personal == False)

    logs = query.all()
    log_dates = [log.date_done for log in logs]

    # 3. Kalender-Tage generieren
    num_days = calendar.monthrange(view_year, view_month)[1]
    days = [{'date': date(view_year, view_month, d), 'weekday': date(view_year, view_month, d).weekday()} for d in range(1, num_days + 1)]

    # 4. Räume für das Dropdown laden (nur Haushalt)
    household_rooms = TaskList.query.filter_by(is_personal=False).all()

    return render_template('profile.html', 
                           user=user, h_pts=h_pts, p_pts=p_pts,
                           days=days, logs=log_dates, today=today,
                           view_month=view_month, view_year=view_year,
                           month_names=list(calendar.month_name)[1:],
                           rooms=household_rooms,
                           selected_room_id=selected_room_id)

# --- WEB PUSH ROUTES ---

@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription_info = request.get_json()
    with open('subscription.json', 'w') as f:
        json.dump(subscription_info, f)
    return '', 204

@app.route('/send_test_push')
def send_test_push():
    try:
        if not os.path.exists('subscription.json'):
            return "Error: No subscription found. Open localhost:5000 on PC!", 400
        with open('subscription.json', 'r') as f:
            sub_info = json.load(f)
        webpush(subscription_info=sub_info, data="Time for the household check! 🧹",
                vapid_private_key=VAPID_PRIVATE_KEY, vapid_claims=VAPID_CLAIMS)
        return "Push sent!"
    except Exception as e:
        return f"Error: {e}", 500

# --- INITIALIZATION ---

def setup_database():
    with app.app_context():
        db.create_all()
        
        # 1. User anlegen
        if User.query.count() == 0:
            db.session.add(User(username="Eda"))
            db.session.add(User(username="Melih"))
            db.session.commit()

        # 2. Haushalt-Aufgaben (CHORES_LIST) einpflegen
        for task_data in CHORES_LIST:
            title = task_data[0]
            room_name = task_data[1]
            days = task_data[2]
            pts = task_data[3]
            
            room = TaskList.query.filter_by(name=room_name).first()
            if not room:
                # WICHTIG: is_personal=False markiert dies als Haushalts-Raum
                room = TaskList(name=room_name, is_personal=False)
                db.session.add(room)
                db.session.commit()
            
            if not Task.query.filter_by(title=title, list_id=room.id, is_personal=False).first():
                new_task = Task(
                    title=title, 
                    list_id=room.id, 
                    interval_value=days, 
                    points_worth=pts, 
                    last_done=date.today() - timedelta(days=days),
                    is_personal=False,
                    for_user='Both'
                )
                db.session.add(new_task)

        # 3. Personal-Aufgaben (PERSONAL_CHORES) einpflegen
        from tasks_config import PERSONAL_CHORES
        for title, cat_name, days, pts, is_pers, for_usr in PERSONAL_CHORES:
            category = TaskList.query.filter_by(name=cat_name).first()
            if not category:
                # WICHTIG: is_personal=True markiert dies als Personal-Kategorie
                category = TaskList(name=cat_name, is_personal=True)
                db.session.add(category)
                db.session.commit()

            if not Task.query.filter_by(title=title, is_personal=True, for_user=for_usr).first():
                new_personal_task = Task(
                    title=title,
                    list_id=category.id,
                    interval_value=days,
                    points_worth=pts,
                    last_done=date.today() - timedelta(days=max(1, days)),
                    is_personal=is_pers,
                    for_user=for_usr
                )
                db.session.add(new_personal_task)

        db.session.commit()

@app.template_filter('slugify')
def slugify_filter(s):
    return s.lower().replace(' ', '-')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)