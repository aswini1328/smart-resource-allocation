from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('impact.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS needs (
                      id INTEGER PRIMARY KEY,
                      area TEXT NOT NULL,
                      category TEXT NOT NULL,
                      urgency INTEGER NOT NULL,
                      score REAL NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS volunteers (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      skills TEXT,
                      skill TEXT,
                      location TEXT NOT NULL,
                      ngo TEXT
                      )''')

    cols = [r[1] for r in cursor.execute("PRAGMA table_info(volunteers)").fetchall()]
    if 'skills' not in cols and 'skill' in cols:
        cursor.execute('ALTER TABLE volunteers ADD COLUMN skills TEXT')
        cursor.execute('UPDATE volunteers SET skills = skill')

    if 'skill' not in cols:
        cursor.execute('ALTER TABLE volunteers ADD COLUMN skill TEXT')

    if 'ngo' not in cols:
        cursor.execute('ALTER TABLE volunteers ADD COLUMN ngo TEXT')

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('impact.db')
    conn.row_factory = sqlite3.Row
    return conn

def estimate_distance(a, b):
    a_norm = a.strip().lower()
    b_norm = b.strip().lower()
    if a_norm == b_norm:
        return 0.3
    if a_norm in b_norm or b_norm in a_norm:
        return 1.4
    return 5.2

def skill_relevance(need_category, volunteer_skills):
    need_cat = need_category.lower().strip()
    skills = [x.strip().lower() for x in volunteer_skills.split(',') if x.strip()]
    if need_cat in skills:
        return 0
    if any(need_cat in s or s in need_cat for s in skills):
        return 1
    return 2

@app.route('/')
def index():
    conn = get_db_connection()
    needs = conn.execute('SELECT * FROM needs ORDER BY score DESC').fetchall()
    volunteers = conn.execute('SELECT * FROM volunteers').fetchall()
    conn.close()

    matches = {}

    for need in needs:
        need_category = need['category']
        need_area = need['area']

        candidate_list = []
        for v in volunteers:
            volunteer_skills = ''
            if 'skills' in v.keys():
                volunteer_skills = v['skills'] or ''
            elif 'skill' in v.keys():
                volunteer_skills = v['skill'] or ''

            volunteer_location = v['location'] if 'location' in v.keys() else ''

            rel = skill_relevance(need_category, volunteer_skills)
            dist = estimate_distance(need_area, volunteer_location)
            candidate_list.append((rel, dist, v))

        candidate_list.sort(key=lambda t: (t[0], t[1], t[2]['name'].lower()))

        assigned = None
        for rel, dist, v in candidate_list:
            if rel >= 2:
                continue
            volunteer_skills = v['skills'] if 'skills' in v.keys() else (v['skill'] if 'skill' in v.keys() else '')
            volunteer_location = v['location'] if 'location' in v.keys() else 'n/a'
            volunteer_ngo = v['ngo'] if 'ngo' in v.keys() and v['ngo'] else 'n/a'
            assigned = f"{v['name']} ({volunteer_skills} @ {volunteer_location} | NGO: {volunteer_ngo})"
            break

        matches[need['id']] = assigned or 'No suitable volunteer'

    return render_template('index.html', needs=needs, volunteers=volunteers, matches=matches)

@app.route('/add', methods=['GET', 'POST'])
def add_need():
    if request.method == 'POST':
        area = request.form['area'].strip()
        category = request.form['category'].strip()
        urgency = int(request.form['urgency'])
        score = round(urgency * 1.5, 1)

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO needs (area, category, urgency, score) VALUES (?, ?, ?, ?)',
            (area, category, urgency, score)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_need.html')

@app.route('/add_volunteer', methods=['GET', 'POST'])
def add_volunteer():
    if request.method == 'POST':
        name = request.form['name'].strip()
        skills = request.form['skills'].strip()
        location = request.form['location'].strip()
        ngo = request.form['ngo'].strip()

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO volunteers (name, skills, skill, location, ngo) VALUES (?, ?, ?, ?, ?)',
            (name, skills, skills, location, ngo)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_volunteer.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

