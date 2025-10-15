import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Room, Batch, Faculty, Subject
from scheduler_v2 import run_scheduler

# --- 1. CREATE THE FLASK APP INSTANCE ---
app = Flask(__name__)

# --- 2. CONFIGURE THE APP (MUST HAPPEN BEFORE INITIALIZATION) ---
# Set a secret key for session management. You should change this to a random string.
app.config['SECRET_KEY'] = 'a-very-secure-and-random-secret-key-for-production'
# Define the database file path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'scheduler.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 3. INITIALIZE THE DATABASE EXTENSION WITH THE CONFIGURED APP ---
db.init_app(app)


# ======================================================================
# --- AUTHENTICATION & CORE PAGE ROUTES ---
# ======================================================================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Username and password are required.", 400

        user = User.query.filter_by(username=username).first()
        if user:
            return "Username already exists. Please choose another.", 409

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        return redirect(url_for('dashboard'))
    else:
        return "Invalid username or password", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/manage')
def manage():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    # Pass all data to the manage page for selection dropdowns
    subjects = Subject.query.all()
    faculties = Faculty.query.all()
    return render_template('manage.html', subjects=subjects, faculties=faculties)

# ======================================================================
# --- API FOR DATA MANAGEMENT (CRUD OPERATIONS) ---
# ======================================================================

def check_auth():
    """Helper function to check if a user is logged in."""
    return 'user_id' in session

# --- Rooms API ---
@app.route('/api/rooms', methods=['GET', 'POST'])
def handle_rooms():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    
    if request.method == 'POST':
        data = request.json
        new_room = Room(name=data['name'])
        db.session.add(new_room)
        db.session.commit()
        return jsonify({"id": new_room.id, "name": new_room.name}), 201

    rooms = Room.query.all()
    return jsonify([{"id": room.id, "name": room.name} for room in rooms])

@app.route('/api/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"success": True})

# --- Batches API ---
@app.route('/api/batches', methods=['GET', 'POST'])
def handle_batches():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    
    if request.method == 'POST':
        data = request.json
        new_batch = Batch(name=data['name'])
        db.session.add(new_batch)
        db.session.commit()
        return jsonify({"id": new_batch.id, "name": new_batch.name}), 201

    batches = Batch.query.all()
    return jsonify([{"id": batch.id, "name": batch.name} for batch in batches])

@app.route('/api/batches/<int:batch_id>', methods=['DELETE'])
def delete_batch(batch_id):
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    batch = Batch.query.get_or_404(batch_id)
    db.session.delete(batch)
    db.session.commit()
    return jsonify({"success": True})

# --- Subjects API ---
@app.route('/api/subjects', methods=['GET', 'POST'])
def handle_subjects():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    
    if request.method == 'POST':
        data = request.json
        new_subject = Subject(name=data['name'], code=data['code'], hours_per_week=data['hours_per_week'])
        db.session.add(new_subject)
        db.session.commit()
        return jsonify({"id": new_subject.id, "name": new_subject.name, "code": new_subject.code, "hours_per_week": new_subject.hours_per_week}), 201

    subjects = Subject.query.all()
    return jsonify([{"id": s.id, "name": s.name, "code": s.code, "hours_per_week": s.hours_per_week} for s in subjects])

@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({"success": True})

# --- Faculty API ---
@app.route('/api/faculties', methods=['GET', 'POST'])
def handle_faculties():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    
    if request.method == 'POST':
        data = request.json
        new_faculty = Faculty(name=data['name'])
        db.session.add(new_faculty)
        db.session.commit()
        return jsonify({"id": new_faculty.id, "name": new_faculty.name, "subjects": []}), 201

    faculties = Faculty.query.all()
    return jsonify([{"id": f.id, "name": f.name, "subjects": [{"id": s.id, "code": s.code} for s in f.subjects]} for f in faculties])

@app.route('/api/faculties/<int:faculty_id>', methods=['DELETE'])
def delete_faculty(faculty_id):
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    faculty = Faculty.query.get_or_404(faculty_id)
    db.session.delete(faculty)
    db.session.commit()
    return jsonify({"success": True})

# --- Association API (Linking Subjects to Faculty) ---
@app.route('/api/faculties/<int:faculty_id>/subjects', methods=['POST'])
def add_subject_to_faculty(faculty_id):
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    faculty = Faculty.query.get_or_404(faculty_id)
    subject = Subject.query.get_or_404(data['subject_id'])
    
    if subject not in faculty.subjects:
        faculty.subjects.append(subject)
        db.session.commit()

    return jsonify({"success": True, "faculty_name": faculty.name, "subject_code": subject.code})


# ======================================================================
# --- SCHEDULER API ---
# ======================================================================
# app.py -> Replace ONLY the generate_timetable function with this

# ======================================================================
# --- SCHEDULER API ---
# ======================================================================

@app.route('/api/generate', methods=['POST'])
def generate_timetable():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # Step 1: Fetch all data from the database
        db_rooms = Room.query.all()
        db_batches = Batch.query.all()
        db_faculty = Faculty.query.all()
        db_subjects = Subject.query.all()

        # --- NEW: DETAILED DEBUG REPORT ---
        print("\n--- DATA VALIDATION REPORT ---")
        print(f"Rooms found: {len(db_rooms)}")
        print(f"Batches found: {len(db_batches)}")
        print(f"Subjects found: {len(db_subjects)}")
        print(f"Faculty found: {len(db_faculty)}")
        
        is_any_faculty_assigned = any(f.subjects for f in db_faculty)
        print(f"Is at least one faculty assigned a subject? {is_any_faculty_assigned}")
        print("--------------------------------\n")
        # --- END OF REPORT ---

        # --- PRE-GENERATION VALIDATION ---
        if not db_rooms:
            return jsonify({"status": "error", "message": "No rooms found. Please add at least one room."}), 400
        if not db_batches:
            return jsonify({"status": "error", "message": "No batches found. Please add at least one batch."}), 400
        if not db_subjects:
            return jsonify({"status": "error", "message": "No subjects found. Please add at least one subject."}), 400
        if not db_faculty:
            return jsonify({"status": "error", "message": "No faculty found. Please add at least one faculty member."}), 400

        if not is_any_faculty_assigned:
            return jsonify({"status": "error", "message": "Faculty members have not been assigned any subjects. Please assign subjects on the 'Manage Data' page."}), 400
        # --- END OF VALIDATION ---

        # Step 2: Convert database objects into the simple dict format the algorithm expects
        input_data = {
            "rooms": [r.name for r in db_rooms],
            "batches": [b.name for b in db_batches],
            "faculty": {f.name: {"subjects": [s.code for s in f.subjects]} for f in db_faculty},
            "subjects": {s.code: {"name": s.name, "hours_per_week": s.hours_per_week, "batches": [b.name for b in db_batches]} for s in db_subjects},
            "timeslots": ["9-10", "10-11", "11-12", "1-2", "2-3"],
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri"]
        }

        # Step 3: Run the scheduler algorithm multiple times to get options
        best_timetables = []
        for i in range(3):
            print(f"--- Running scheduler: Pass {i+1} ---")
            timetable = run_scheduler(input_data)
            best_timetables.append(timetable)
        
        best_timetables.sort(key=lambda t: t.fitness)

        # Step 4: Format the results for the frontend
        results_json = []
        for i, tt in enumerate(best_timetables):
            timetable_json = []
            for gene in tt.genes:
                timetable_json.append({
                    "day": gene.day, "timeslot": gene.timeslot, "room": gene.room,
                    "batch": gene.batch, "subject": gene.subject, "faculty": gene.faculty
                })
            results_json.append({"option": i + 1, "fitness": tt.fitness, "timetable": timetable_json})

        return jsonify({"status": "success", "results": results_json})
    
    except Exception as e:
        print(f"Error during generation: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # This block allows you to run 'python app.py' from the terminal
    app.run(debug=True)
