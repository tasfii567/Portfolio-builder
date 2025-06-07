from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home route (this was missing)
@app.route('/')
def home():
    return render_template('index.html')  # Or whatever the content should be

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/portfolioweb')
def portfolioweb():
    return render_template('portfolioweb.html')
@app.route('/modern')
def modern_template():
    return render_template('modern.html')
@app.route('/professional')
def professional_template():
    return render_template('professional.html')
@app.route('/creative')
def creative_template():
    return render_template('creative.html')
@app.route('/editportfolio')
def editportfolio():
    return render_template('editportfolio.html')





@app.route('/register')
def register_page():
    return render_template('register.html')
# Register route
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using pbkdf2:sha256 for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Save user to the database
        conn = sqlite3.connect('portfolio.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (username, email, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        conn = sqlite3.connect('portfolio.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        # Verify the password
        if user and check_password_hash(user[3], password):  # Compare hashed password
            return "Logged in successfully!"  # Redirect to a protected page, for now, just a success message
        else:
            return "Invalid email or password"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
