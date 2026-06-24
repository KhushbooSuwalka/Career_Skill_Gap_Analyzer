from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json

def update_user_skills_in_db(user_id, skills_list):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET skills = ? WHERE id = ?",
            (json.dumps(skills_list), user_id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error updating user skills in DB:", e)

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-career-pathfinder'
DATABASE_FILE = 'careers.db'

def check_db_schema():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'phone' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
            conn.commit()
            print("Added 'phone' column to 'users' table.")
        conn.close()
    except Exception as e:
        print("Error checking/updating db schema:", e)

check_db_schema()

CAREER_ICONS = {
    "frontend-dev": "🌐",
    "data-scientist": "📊",
    "product-manager": "🎯",
    "cybersecurity-analyst": "🛡️",
    "backend-dev": "⚙️",
    "fullstack-dev": "💻",
    "mobile-dev": "📱",
    "devops-engineer": "♾️",
    "cloud-architect": "☁️",
    "ui-ux-designer": "🎨",
    "qa-engineer": "🔍",
    "machine-learning-eng": "🤖",
    "data-engineer": "🗄️",
    "game-developer": "🎮",
    "system-admin": "🖥️",
    "blockchain-developer": "⛓️"
}

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = dict_factory
    return conn

def format_skill_name(skill_name):
    if not skill_name:
        return ""
    uppercase_skills = {"html", "css", "sql", "js", "api", "ux", "siem", "it", "dns", "tcp/ip", "prd"}
    words = skill_name.strip().split()
    formatted_words = []
    for word in words:
        word_lower = word.lower()
        if word_lower in uppercase_skills:
            formatted_words.append(word_lower.upper())
        else:
            formatted_words.append(word.capitalize())
    return " ".join(formatted_words)

@app.route('/auth')
def auth():
    if 'user_id' in session:
        return redirect(url_for('index'))
    next_url = request.args.get('next', '')
    return render_template('auth.html', next_url=next_url)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    phone = request.form.get('phone', '').strip()
    next_url = request.form.get('next', '')
    
    if not username or not password or not phone:
        return redirect(url_for('auth', mode='register', error='Username, password, and phone number are required.'))
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return redirect(url_for('auth', mode='register', error='Username already exists.'))
            
        password_hash = generate_password_hash(password)
        guest_skills = session.get('user_skills', ["HTML", "CSS", "Python"])
        
        cursor.execute(
            "INSERT INTO users (username, password_hash, phone, skills) VALUES (?, ?, ?, ?)",
            (username, password_hash, phone, json.dumps(guest_skills))
        )
        conn.commit()
        
        cursor.execute("SELECT id, username, skills FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['user_skills'] = json.loads(user['skills'])
        session.modified = True
        
        if next_url:
            return redirect(next_url)
        return redirect(url_for('index'))
        
    except Exception as e:
        print("Registration error:", e)
        return redirect(url_for('auth', mode='register', error='An error occurred during registration.'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    next_url = request.form.get('next', '')
    
    if not username or not password:
        return redirect(url_for('auth', mode='login', error='Username and password are required.'))
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, skills FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not check_password_hash(user['password_hash'], password):
            return redirect(url_for('auth', mode='login', error='Invalid username or password.'))
            
        session['user_id'] = user['id']
        session['username'] = user['username']
        
        # Configure session permanence for Remember Me
        if request.form.get('remember'):
            session.permanent = True
        else:
            session.permanent = False
            
        db_skills = json.loads(user['skills']) if user['skills'] else []
        guest_skills = session.get('user_skills', [])
        merged_skills = list(db_skills)
        for skill in guest_skills:
            if skill not in merged_skills:
                merged_skills.append(skill)
                
        session['user_skills'] = merged_skills
        session.modified = True
        
        update_user_skills_in_db(user['id'], merged_skills)
        
        if next_url:
            return redirect(next_url)
        return redirect(url_for('index'))
        
    except Exception as e:
        print("Login error:", e)
        return redirect(url_for('auth', mode='login', error='An error occurred during login.'))

@app.route('/reset-password', methods=['POST'])
def reset_password():
    username = request.form.get('username', '').strip()
    phone = request.form.get('phone', '').strip()
    password = request.form.get('password', '')
    
    if not username or not phone or not password:
        return redirect(url_for('auth', mode='forgot', error='Username, phone number, and new password are required.'))
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND phone = ?", (username, phone))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return redirect(url_for('auth', mode='forgot', error='Username or phone number not found/incorrect.'))
            
        password_hash = generate_password_hash(password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, username))
        conn.commit()
        conn.close()
        
        return redirect(url_for('auth', mode='login', success='Password reset successfully! You can now log in.'))
        
    except Exception as e:
        print("Password reset error:", e)
        return redirect(url_for('auth', mode='forgot', error='An error occurred during password reset.'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'user_skills' not in session:
        session['user_skills'] = ["HTML", "CSS", "Python"]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description FROM careers")
        careers = cursor.fetchall()
        for career in careers:
            cursor.execute(
                "SELECT skill FROM roadmap_steps WHERE career_id = ? ORDER BY sort_order",
                (career['id'],)
            )
            steps = cursor.fetchall()
            career['requiredSkills'] = [step['skill'] for step in steps]
        conn.close()
    except Exception as e:
        careers = []
        print("Database error:", e)
        
    results = session.pop('results', None)
    selected_career_id = session.pop('selected_career_id', None)
        
    return render_template(
        'index.html',
        careers=careers,
        user_skills=session['user_skills'],
        selected_career_id=selected_career_id,
        results=results,
        career_icons=CAREER_ICONS
    )

@app.route('/add_skill', methods=['POST'])
def add_skill():
    skill = request.form.get('skill')
    if skill:
        formatted = format_skill_name(skill)
        user_skills = session.get('user_skills', [])
        if formatted and formatted not in user_skills:
            user_skills.append(formatted)
            session['user_skills'] = user_skills
            session.modified = True
            if 'user_id' in session:
                update_user_skills_in_db(session['user_id'], user_skills)
    return redirect(url_for('index', _anchor='simulator'))

@app.route('/remove_skill', methods=['POST'])
def remove_skill():
    skill = request.form.get('skill')
    user_skills = session.get('user_skills', [])
    if skill in user_skills:
        user_skills.remove(skill)
        session['user_skills'] = user_skills
        session.modified = True
        if 'user_id' in session:
            update_user_skills_in_db(session['user_id'], user_skills)
    return redirect(url_for('index', _anchor='simulator'))

@app.route('/analyze', methods=['POST'])
def analyze():
    career_id = request.form.get('career_id')
    unadded_skill = request.form.get('unadded_skill')
    user_skills = session.get('user_skills', [])
    
    if unadded_skill:
        formatted = format_skill_name(unadded_skill)
        if formatted and formatted not in user_skills:
            user_skills.append(formatted)
            session['user_skills'] = user_skills
            session.modified = True
            if 'user_id' in session:
                update_user_skills_in_db(session['user_id'], user_skills)
            
    user_skills_upper = [s.upper() for s in user_skills]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description FROM careers")
        careers = cursor.fetchall()
        for career in careers:
            cursor.execute(
                "SELECT skill FROM roadmap_steps WHERE career_id = ? ORDER BY sort_order",
                (career['id'],)
            )
            steps = cursor.fetchall()
            career['requiredSkills'] = [step['skill'] for step in steps]
            
        cursor.execute("SELECT title FROM careers WHERE id = ?", (career_id,))
        career_meta = cursor.fetchone()
        
        if not career_meta:
            conn.close()
            return redirect(url_for('index'))
            
        cursor.execute(
            "SELECT skill, phase, topic, sort_order FROM roadmap_steps WHERE career_id = ? ORDER BY sort_order",
            (career_id,)
        )
        roadmap_steps = cursor.fetchall()
        conn.close()
        
        matched_skills = []
        missing_skills = []
        processed_roadmap = []
        
        for step in roadmap_steps:
            skill_name = step['skill']
            skill_name_upper = skill_name.upper()
            is_matched = False
            for u_skill in user_skills_upper:
                if u_skill == skill_name_upper or u_skill in skill_name_upper or skill_name_upper in u_skill:
                    is_matched = True
                    break
            
            if is_matched:
                matched_skills.append(skill_name)
            else:
                missing_skills.append(skill_name)
                
            processed_roadmap.append({
                "skill": skill_name,
                "phase": step['phase'],
                "topic": step['topic'],
                "completed": is_matched
            })
            
        total_skills = len(roadmap_steps)
        readiness_score = 0
        if total_skills > 0:
            readiness_score = round((len(matched_skills) / total_skills) * 100)
            
        results = {
            "career_title": career_meta['title'],
            "readiness_score": readiness_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "roadmap": processed_roadmap
        }
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            import json
            user_id = session.get('user_id')
            cursor.execute(
                "INSERT INTO skill_checks (user_id, career_id, career_title, readiness_score, user_skills) VALUES (?, ?, ?, ?, ?)",
                (user_id, career_id, career_meta['title'], readiness_score, json.dumps(user_skills))
            )
            conn.commit()
            conn.close()
        except Exception as he:
            print("Failed to save history record:", he)
        
    except Exception as e:
        print("Analysis error:", e)
        return redirect(url_for('index'))
        
    session['results'] = results
    session['selected_career_id'] = career_id
    session.modified = True
    return redirect(url_for('index'))

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('auth', next=url_for('history')))
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, career_id, career_title, readiness_score, user_skills, timestamp FROM skill_checks WHERE user_id = ? ORDER BY timestamp DESC",
            (session['user_id'],)
        )
        rows = cursor.fetchall()
        
        import json
        history_records = []
        for row in rows:
            u_skills = json.loads(row['user_skills'])
            cursor.execute(
                "SELECT skill, phase, topic, sort_order FROM roadmap_steps WHERE career_id = ? ORDER BY sort_order",
                (row['career_id'],)
            )
            roadmap_steps = cursor.fetchall()
            
            matched_skills = []
            missing_skills = []
            processed_roadmap = []
            user_skills_upper = [s.upper() for s in u_skills]
            for step in roadmap_steps:
                skill_name = step['skill']
                skill_name_upper = skill_name.upper()
                is_matched = False
                for u_skill in user_skills_upper:
                    if u_skill == skill_name_upper or u_skill in skill_name_upper or skill_name_upper in u_skill:
                        is_matched = True
                        break
                
                if is_matched:
                    matched_skills.append(skill_name)
                else:
                    missing_skills.append(skill_name)
                    
                processed_roadmap.append({
                    "skill": skill_name,
                    "phase": step['phase'],
                    "topic": step['topic'],
                    "completed": is_matched
                })
                
            history_records.append({
                "id": row['id'],
                "career_id": row['career_id'],
                "career_title": row['career_title'],
                "readiness_score": row['readiness_score'],
                "timestamp": row['timestamp'],
                "user_skills": u_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "roadmap": processed_roadmap
            })
        conn.close()
    except Exception as e:
        history_records = []
        print("History fetch error:", e)
        
    return render_template(
        'history.html',
        history_records=history_records,
        career_icons=CAREER_ICONS
    )

@app.route('/delete_history/<int:record_id>', methods=['POST'])
def delete_history(record_id):
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM skill_checks WHERE id = ? AND user_id = ?",
            (record_id, session['user_id'])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Delete history error:", e)
    return redirect(url_for('history'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skill_checks WHERE user_id = ?", (session['user_id'],))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Clear history error:", e)
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
