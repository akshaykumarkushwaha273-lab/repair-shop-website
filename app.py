import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, session
from datetime import datetime
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'techfix_pro_secret_2024')

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'techfix_pro'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"DB connection error: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                service VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reply TEXT,
                replied_at TIMESTAMP
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute("SELECT id FROM admin WHERE username = 'admin'")
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO admin (username, password) VALUES (%s, %s)",
                ('admin', 'admin@123')
            )
        conn.commit()
        cur.close()
        print("✓ Database initialized")
        return True
    except Exception as e:
        print(f"Init error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/admin/login')
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit-message', methods=['POST'])
def submit_message():
    try:
        data = request.json
        if not all([data.get('name'), data.get('email'), data.get('service'), data.get('message')]):
            return jsonify({'success': False, 'error': 'All required fields needed'}), 400
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database error'}), 500
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO messages (name, email, phone, service, message)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        ''', (data['name'], data['email'], data.get('phone',''), data['service'], data['message']))
        msg_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Message sent!', 'message_id': msg_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'DB connection failed'}), 500
        cur = conn.cursor()
        cur.execute("SELECT id FROM admin WHERE username=%s AND password=%s", (data['username'], data['password']))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = data['username']
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    if not conn:
        return redirect('/admin/login')
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT COUNT(*) as count FROM messages WHERE status='pending'")
    pending = cur.fetchone()['count']
    cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
    msgs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_dashboard.html', messages=msgs, pending_count=pending)

@app.route('/admin/message/<int:message_id>')
@login_required
def view_message(message_id):
    conn = get_db_connection()
    if not conn:
        return redirect('/admin/login')
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM messages WHERE id=%s", (message_id,))
    msg = cur.fetchone()
    cur.close()
    conn.close()
    if not msg:
        return redirect('/admin/dashboard')
    return render_template('admin_message_detail.html', message=msg)

@app.route('/api/admin/reply', methods=['POST'])
@login_required
def send_reply():
    data = request.json
    if not data.get('reply'):
        return jsonify({'success': False, 'error': 'Reply cannot be empty'}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'DB error'}), 500
    cur = conn.cursor()
    cur.execute('''
        UPDATE messages SET reply=%s, status='replied', replied_at=CURRENT_TIMESTAMP
        WHERE id=%s
    ''', (data['reply'], data['message_id']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Reply sent'})

@app.route('/api/admin/delete/<int:message_id>', methods=['DELETE'])
@login_required
def delete_message(message_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'DB error'}), 500
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE id=%s", (message_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Deleted'})

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    print("="*50)
    print("Starting TechFix Pro Repair Shop")
    print("="*50)
    if init_db():
        app.run(debug=True, port=5000)
    else:
        print("✗ Failed to initialize database. Check PostgreSQL.")