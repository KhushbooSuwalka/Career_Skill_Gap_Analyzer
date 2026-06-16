from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-career-pathfinder'
DATABASE_FILE = 'careers.db'

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
    return redirect(url_for('index'))

@app.route('/remove_skill', methods=['POST'])
def remove_skill():
    skill = request.form.get('skill')
    user_skills = session.get('user_skills', [])
    if skill in user_skills:
        user_skills.remove(skill)
        session['user_skills'] = user_skills
        session.modified = True
    return redirect(url_for('index'))

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
            cursor.execute(
                "INSERT INTO skill_checks (career_id, career_title, readiness_score, user_skills) VALUES (?, ?, ?, ?)",
                (career_id, career_meta['title'], readiness_score, json.dumps(user_skills))
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, career_id, career_title, readiness_score, user_skills, timestamp FROM skill_checks ORDER BY timestamp DESC")
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skill_checks WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Delete history error:", e)
    return redirect(url_for('history'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skill_checks")
        conn.commit()
        conn.close()
    except Exception as e:
        print("Clear history error:", e)
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
